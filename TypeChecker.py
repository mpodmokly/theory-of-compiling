import AST
from SymbolTable import SymbolTable, Symbol


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        print(f"type {node} not handled")


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.error_handled = False
        self.symbol_table = SymbolTable()
        self.assignment = False
        self.value = -1
        self.loop = 0
        self.ref_bounds = [float("inf"), -float("inf")]

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
        self.ref_bounds[0] = min(self.ref_bounds[0], self.value)
        self.ref_bounds[1] = max(self.ref_bounds[1], self.value)
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
        self.symbol_table.popScope()

        if node.false_statement is not None:
            self.symbol_table.pushScope()
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
            print(f"line {node.lineno}: break statement outside the loop")
            self.error_handled = True

    def visit_ContinueStatement(self, node):
        if self.loop == 0:
            print(f"line {node.lineno}: continue statement outside the loop")
            self.error_handled = True

    def visit_ReturnStatement(self, node):
        self.visit(node.value)
    
    def visit_PrintStatement(self, node):
        self.visit(node.value)

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)

        if symbol is None:
            if not self.assignment:
                print(f"line {node.lineno}: identifier {node.name} is not declared")
                self.error_handled = True
            
            self.assignment = False
            return None
        
        self.assignment = False
        return symbol.type
    
    def visit_EyeStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print(f"line {node.lineno}: int type expected")
            self.error_handled = True
        
        return self.value

    def visit_OnesStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print(f"line {node.lineno}: int type expected")
            self.error_handled = True
        
        return self.value

    def visit_ZerosStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print(f"line {node.lineno}: int type expected")
            self.error_handled = True

        return self.value
    
    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

        if type_left is None or type_right is None:
            return type_left
        
        # check matrix dimensions compatibility
        if type(type_left) is int and type(type_right) is int:
            if type_left != type_right:
                print(f"line {node.lineno}: incompatible matrix sizes {\
                    type_left} and {type_right}")
                self.error_handled = True
            
            if node.operator == "/":
                print(f"line {node.lineno}: invalid / operator for matrix")
                self.error_handled = True
        elif node.operator in [".+", ".-", ".*", "./"]:
            print(f"line {node.lineno}: invalid {node.operator\
                } operator for scalar")
            self.error_handled = True

        if type_left is not type_right:
            if not (type_left in [int, float] and type_right in [int, float]):
                if not (type_left in [int, str] and type_right in [int, str] and\
                    node.operator in ["+", "*"]):
                    type_left_key = type_left
                    type_right_key = type_right

                    if type(type_left_key) is int:
                        type_left_key = list
                    if type(type_right_key) is int:
                        type_right_key = list
                    
                    print(f"line {node.lineno}: incompatible types {\
                        self.TYPES_DICT[type_left_key]} and {\
                        self.TYPES_DICT[type_right_key]}")
                    self.error_handled = True
        elif type_left is str and type_right is str and\
            node.operator in ["-", "*", "/"]:
            print(f"line {node.lineno}: invalid operator {\
                node.operator} for str")
            self.error_handled = True
        
        return type_left
    
    def visit_UnExpr(self, node):
        symbol = self.visit(node.arg)

        if symbol is str:
            print(f"line {node.lineno}: unary operator is not supported for type str")
            self.error_handled = True
        elif symbol in [int, float] and node.operator == "'":
            text = f"line {node.lineno}: transpose operator is not"
            text += f" supported for type {self.TYPES_DICT[symbol]}"
            print(text)
            self.error_handled = True
        
        return symbol

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
                print(f"line {node.lineno}: invalid matrix dimensions {\
                    symbol1} and {symbol2}")
                self.error_handled = True
                return None
            return symbol2

        if type(symbol1) is int:
            size += symbol1
        else:
            if symbol1 is str:
                print(f"line {node.lineno}: incompatible str in matrix")
                self.error_handled = True
            size += 1
        if type(symbol2) is int:
            size += symbol2
        else:
            if symbol1 is str or symbol2 is str:
                print(f"line {node.lineno}: incompatible str in matrix")
                self.error_handled = True
            
            size += 1
        
        return size
    
    def visit_Reference(self, node):
        self.ref_bounds = [float("inf"), -float("inf")]
        symbol = self.visit(node.name)

        if symbol is not None:
            ref_size = self.visit(node.elements)

            if ref_size is int:
                print(f"line {node.lineno}: matrix dimension 1 too low")
                self.error_handled = True
            elif ref_size != 2:
                print(f"line {node.lineno}: matrix dimension {\
                    ref_size} out of bounds")
                self.error_handled = True
            
            if self.ref_bounds[0] < 0:
                print(f"line {node.lineno}: matrix index {\
                    self.ref_bounds[0]} does not exist")
                self.error_handled = True
            
            if self.ref_bounds[1] >= symbol:
                print(f"line {node.lineno}: matrix index {\
                    self.ref_bounds[1]} does not exist")
                self.error_handled = True
        
        return int
    
    def visit_Assignment(self, node):
        self.assignment = True
        symbol_id = self.visit(node.variable) # left
        symbol_val = self.visit(node.value)   # right
        
        if symbol_val is not None:
            if symbol_id is None:
                self.symbol_table.put(Symbol(node.variable.name, symbol_val))
            else:
                if type(node.variable) is AST.Reference:
                    if symbol_val is str:
                        print(f"line {node.lineno}: incompatible str in matrix")
                        self.error_handled = True
                    elif type(symbol_val) is int:
                        print(f"line {node.lineno}: incompatible matrix in matrix")
                        self.error_handled = True
                else:
                    new_symbol = self.symbol_table.get(node.variable.name)
                    new_symbol.type = symbol_val
