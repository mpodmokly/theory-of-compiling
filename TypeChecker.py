import AST
from SymbolTable import SymbolTable, Symbol, MatrixSymbol


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
        self.ASSIGNMENT = False
        self.VALUE = -1

    def visit_Instructions(self, node):
        if node.instr_first is not None:
            self.visit(node.instr_first)
        if node.instr_second is not None:
            self.visit(node.instr_second)
    
    def visit_IntNum(self, node):
        self.VALUE = int(node.value)
        return int
    
    def visit_FloatNum(self, node):
        self.VALUE = float(node.value)
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
        self.ASSIGNMENT = True
        symbol = self.visit(node.variable)

        if symbol is None:
            self.symbol_table.put(Symbol(node.variable.name, int))

        self.visit(node.for_range)
        self.visit(node.statement)

        self.symbol_table.popScope()

    def visit_Range(self, node):
        self.visit(node.begin)
        self.visit(node.end)
    
    def visit_WhileStatement(self, node):
        self.symbol_table.pushScope()

        self.visit(node.condition)
        self.visit(node.statement)

        self.symbol_table.popScope()

    def visit_ReturnStatement(self, node):
        self.visit(node.value)
    
    def visit_PrintStatement(self, node):
        self.visit(node.value)

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)

        if symbol is None:
            if not self.ASSIGNMENT:
                print(f"Identifier {node.name} is not declared")
            
            self.ASSIGNMENT = False
            return None
        
        self.ASSIGNMENT = False
        return symbol.type
    
    def visit_EyeStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")
        
        return self.VALUE

    def visit_OnesStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")
        
        return self.VALUE

    def visit_ZerosStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")

        return self.VALUE
    
    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

        if type_left is not None and type_right is not None:
            if type_left is list and type_right is list:
                # check dimensions compatibility
                pass
            elif type_left is not type_right:
                if not (type_left is int and type_right is float):
                    if not (type_left is float and type_right is int):
                        print(f"Incompatible types {type_left} and {type_right}")
        
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
        self.ASSIGNMENT = True
        symbol_id = self.visit(node.variable) # left
        symbol_val = self.visit(node.value)   # right

        if symbol_val is not None:
            if symbol_id is None:
                if type(node.value) is AST.Vector or\
                    type(node.value) is AST.ZerosStatement or\
                    type(node.value) is AST.OnesStatement or\
                    type(node.value) is AST.EyeStatement:
                    self.symbol_table.put(MatrixSymbol(node.variable.name, list, symbol_val))
                else:
                    self.symbol_table.put(\
                        Symbol(node.variable.name, symbol_val))
            else:
                if symbol_id is not symbol_val and not (symbol_id is\
                    list and type(node.value) is AST.Vector):
                    print("Incompatible types assignment")
