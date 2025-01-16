import AST
from SymbolTable import SymbolTable, Symbol, MatrixSymbol


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    # simpler version of generic_visit, not so general
    def generic_visit(self, node):
       for child in node.children:
           self.visit(child)

    # def generic_visit(self, node): # Called if no explicit visitor function exists for a node.
    #     if isinstance(node, list):
    #         for elem in node:
    #             self.visit(elem)
    #     else:
    #         for child in node.children:
    #             if isinstance(child, list):
    #                 for item in child:
    #                     if isinstance(item, AST.Node):
    #                         self.visit(item)
    #             elif isinstance(child, AST.Node):
    #                 self.visit(child)


class Result:
    def __init__(self, error = None, type = None, size = None):
        self.error = error
        self.type = type
        self.size = size


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.ASSIGNMENT = False

    def visit_Instructions(self, node):
        if node.instr_first is not None:
            self.visit(node.instr_first)
        if node.instr_second is not None:
            self.visit(node.instr_second)
    
    def visit_IntNum(self, node):
        return int
    
    def visit_FloatNum(self, node):
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
                print(f"{node.name} is not declared")
            return None
        
        self.ASSIGNMENT = False
        return symbol.type
    
    def visit_EyeStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")

    def visit_OnesStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")

    def visit_ZerosStatement(self, node):
        type = self.visit(node.value)

        if type is not int:
            print("int type expected")

        return list
    
    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

        if type_left is not None and type_right is not None:
            if type_left is list and type_right is list:
                pass
            elif type_left is not type_right:
                if not (type_left is int and type_right is float):
                    if not (type_left is float and type_right is int):
                        print(f"Incompatible types {type_left}")

    def visit_Vector(self, node):
        #symbol = self.visit(node.elements)
        #return Result()
        pass
    
    def visit_Elements(self, node):
        #symbol1 = self.visit(node.element1)
        #symbol2 = self.visit(node.element2)
        pass
    
    def visit_Reference(self, node):
        #symbol = self.symbol_table.get(node.name)
        pass
    
    def visit_Assignment(self, node):
        self.ASSIGNMENT = True
        symbol_id = self.visit(node.variable) # left
        symbol_val = self.visit(node.value)   # right

        if symbol_val is not None:
            if symbol_id is None:
                if symbol_val is list:
                    #self.symbol_table.put(MatrixSymbol(node.variable.name, symbol_val))
                    pass
                else:
                    self.symbol_table.put(Symbol(node.variable.name, symbol_val))
            else:
                if symbol_id is not symbol_val:
                    print("Incompatible types assignment")
