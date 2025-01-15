import AST
from SymbolTable import SymbolTable, Symbol


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    # simpler version of generic_visit, not so general
    def generic_visit(self, node):
       for child in node.children:
           self.visit(child)

    # def generic_visit(self, node):       # Called if no explicit visitor function exists for a node.
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

    def visit_Instructions(self, node):
        self.visit(node.instr_first)
        self.visit(node.instr_second)
    
    def visit_IntNum(self, node):
        return node.value
    
    def visit_FloatNum(self, node):
        return node.value
    
    def visit_String(self, node):
        return node.value
    
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

        symbol = self.visit(node.variable, True)
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

    def visit_Variable(self, node, assignment = False):
        symbol = self.symbol_table.get(node.name)

        if symbol is None and not assignment:
            print(f"{node.name} is not declared")
        
        return symbol

    def visit_Vector(self, node):
        symbol = self.visit(node.elements)


        return Result()
    
    def visit_Elements(self, node):
        symbol1 = self.visit(node.element1)
        symbol2 = self.visit(node.element2)

    
    
    
    def visit_Reference(self, node):
        symbol = self.symbol_table.get(node.name)
        
    
    def visit_Assignment(self, node):
        symbol_id = self.visit(node.variable) # left
        symbol_val = self.visit(node.value) # right

        if symbol_val.error is not None:
            print(symbol_val.error)
        else:
            if isinstance(node.variable, AST.Variable):
                if symbol_id.error is not None:
                    self.symbol_table.put(Symbol(node.variable.name, symbol_id.type))
                
                self.symbol_table.get(node.variable.name).type = symbol_val.type
            elif isinstance(node.variable, AST.Reference):
                pass
            else:
                print("Assignment error")

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        # ... 
        #
