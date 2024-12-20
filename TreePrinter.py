import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    
    return decorator

class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent = 0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Instructions)
    def printTree(self, indent = 0):
        if self.instr_first is not None:
            self.instr_first.printTree(indent)
        if self.instr_second is not None:
            self.instr_second.printTree(indent)

    @addToClass(AST.IntNum)
    def printTree(self, indent = 0):
        print("|  " * indent + f"IntNum({self.value})")
    
    @addToClass(AST.FloatNum)
    def printTree(self, indent = 0):
        print("|  " * indent + f"FloatNum({self.value})")

    @addToClass(AST.String)
    def printTree(self, indent = 0):
        print("|  " * indent + f"String({self.value})")

    @addToClass(AST.Variable)
    def printTree(self, indent = 0):
        print("|  " * indent + str(self.name))

    @addToClass(AST.BinExpr)
    def printTree(self, indent = 0):
        print("|  " * indent + self.operator)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)
    
    @addToClass(AST.UnExpr)
    def printTree(self, indent = 0):
        print("|  " * indent + self.operator)
        self.arg.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent = 0):
        print("|  " * indent + "=")
        self.variable.printTree(indent + 1)
        self.value.printTree(indent + 1)
    
    @addToClass(AST.IfStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "IF")
        self.condition.printTree(indent + 1)
        self.true_statement.printTree(indent + 1)
        if self.false_statement is not None:
            self.false_statement.printTree(indent + 1)

    @addToClass(AST.ForStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "FOR")
        self.variable.printTree(indent + 1)
        self.begin.printTree(indent + 1)
        self.end.printTree(indent + 1)
        self.statement.printTree(indent + 1)

    @addToClass(AST.WhileStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.statement.printTree(indent + 1)

    @addToClass(AST.Condition)
    def printTree(self, indent = 0):
        print("|  " * indent + self.operator)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.ReturnStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "RETURN")
        self.value.printTree(indent + 1)
    
    @addToClass(AST.PrintStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "PRINT")
        self.value.printTree(indent + 1)

    @addToClass(AST.BreakStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "BREAK")
    
    @addToClass(AST.ContinueStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "CONTINUE")

    @addToClass(AST.EyeStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "eye")
        self.value.printTree(indent + 1)

    @addToClass(AST.OnesStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "ones")
        self.value.printTree(indent + 1)

    @addToClass(AST.ZerosStatement)
    def printTree(self, indent = 0):
        print("|  " * indent + "zeros")
        self.value.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent = 0):
        print("|  " * indent + "VECTOR")
        self.elements.printTree(indent + 1)
    
    @addToClass(AST.Elements)
    def printTree(self, indent = 0):
        self.element1.printTree(indent)
        self.element2.printTree(indent)

    @addToClass(AST.Reference)
    def printTree(self, indent = 0):
        print("|  " * indent + "REF")
        self.name.printTree(indent + 1)
        self.elements.printTree(indent + 1)



    @addToClass(AST.Error)
    def printTree(self, indent = 0):
        pass    
        # fill in the body
