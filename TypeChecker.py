import AST
from SymbolTable import SymbolTable, Symbol


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
       for child in node.children:
           self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.assignment = False
        self.value = -1
        self.loop = 0
        self.TYPES_DICT = {
            int: "int",
            float: "float",
            str: "string",
            list: "matrix"
        }

    def visit_Instructions(self, node):
        if node.instr_first is not None:
            self.visit(node.instr_first)
        if node.instr_second is not None:
            self.visit(node.instr_second)
    
    def visit_IntNum(self, node):
        self.value = int(node.value)
        return int
    
    def visit_FloatNum(self, node):
        self.value = float(node.value)
        return float
    
    def visit_String(self, node):
        return str
    
    def visit_IfStatement(self, node):
        self.symbol_table.pushScope()
        self.visit(node.condition)
        self.visit(node.true_statement)

        if node.false_statement is not None:
            self.visit(node.false_statement)
        
        self.symbol_table.popScope()
    
    def visit_Condition(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_ForStatement(self, node):
        self.symbol_table.pushScope()
        self.loop += 1

        self.assignment = True
        symbol = self.visit(node.variable)

        if symbol is None:
            self.symbol_table.put(Symbol(node.variable.name, int))

        self.visit(node.for_range)
        self.visit(node.statement)

        self.loop -= 1
        self.symbol_table.popScope()

    def visit_Range(self, node):
        self.visit(node.begin)
        self.visit(node.end)
    
    def visit_WhileStatement(self, node):
        self.symbol_table.pushScope()
        self.loop += 1

        self.visit(node.condition)
        self.visit(node.statement)

        self.loop -= 1
        self.symbol_table.popScope()
    
    def visit_BreakStatement(self, node):
        if self.loop == 0:
            print("break statement outside the loop")

    def visit_ContinueStatement(self, node):
        if self.loop == 0:
            print("continue statement outside the loop")

    def visit_ReturnStatement(self, node):
        self.visit(node.value)
    
    def visit_PrintStatement(self, node):
        self.visit(node.value)

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)

        if symbol is None:
            if not self.assignment:
                print(f"Identifier {node.name} is not declared")
            
            self.assignment = False
            return None
        
        self.assignment = False
        return symbol.type
    
    def visit_EyeStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")
        
        return self.value

    def visit_OnesStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")
        
        return self.value

    def visit_ZerosStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")

        return self.value
    
    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

        if type_left is not None and type_right is not None:
            # check dimensions compatibility - direct matrix
            if type(type_left) is int and type(type_right) is int:
                if type_left != type_right:
                    print(f"Incompatible matrix sizes {type_left} and {type_right}")
            
            # check dimensions compatibility - matrix symbol
            elif type_left is list and type_right is list:
                symbol_left = self.symbol_table.get(node.left.name)
                symbol_right = self.symbol_table.get(node.right.name)

                if symbol_left.size != symbol_right.size:
                    print(f"Incompatible matrix sizes {symbol_left.size} and {\
                        symbol_right.size}")

            elif type_left is not type_right:
                if not (type_left is int and type_right is float):
                    if not (type_left is float and type_right is int):
                        type_left_key = type_left
                        type_right_key = type_right

                        if type(type_left_key) is int:
                            type_left_key = list
                        if type(type_right_key) is int:
                            type_right_key = list
                        
                        print(f"Incompatible types {self.TYPES_DICT[type_left_key]} and {\
                            self.TYPES_DICT[type_right_key]}")
        
        return type_left
    
    def visit_UnExpr(self, node):
        type = self.visit(node.arg)

        if type is str:
            print("Unary operator is not supported for type str")
        
        return type

    def visit_Vector(self, node):
        return self.visit(node.elements)
    
    def visit_Elements(self, node):
        size = 0
        symbol1 = self.visit(node.element1)
        symbol2 = self.visit(node.element2)

        if type(node.element2) is AST.Vector:
            if symbol1 is None:
                return None
            elif symbol1 != symbol2:
                print(f"Invalid matrix dimensions {symbol1} and {symbol2}")
                return None
            return symbol2

        if type(symbol1) is int:
            size += symbol1
        else:
            if symbol1 is str:
                print("Incompatible str in matrix")
            size += 1
        if type(symbol2) is int:
            size += symbol2
        else:
            if symbol2 is str:
                print("Incompatible str in matrix")
            size += 1
        
        return size
    
    def visit_Reference(self, node):
        #symbol = self.symbol_table.get(node.name)
        pass
    
    def visit_Assignment(self, node):
        self.assignment = True
        symbol_id = self.visit(node.variable) # left
        symbol_val = self.visit(node.value)   # right

        if symbol_val is not None:
            if symbol_id is None:
                if type(node.value) in [AST.Vector, AST.ZerosStatement,\
                                        AST.OnesStatement, AST.EyeStatement]:
                    self.symbol_table.put(Symbol(node.variable.name, list, symbol_val))
                else:
                    self.symbol_table.put(\
                        Symbol(node.variable.name, symbol_val))
            else:
                new_symbol = self.symbol_table.get(node.variable.name)

                if type(symbol_val) is int:
                    new_symbol.type = list
                    new_symbol.size = symbol_val
                else:
                    new_symbol.type = symbol_val

                # if symbol_id is not symbol_val and not (symbol_id is\
                #     list and type(node.value) is AST.Vector):
                #     print("Incompatible types assignment")
                #     print(symbol_id, symbol_val, node.value)
