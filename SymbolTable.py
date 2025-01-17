class Symbol:
    def __init__(self, name, type, size = 0):
        self.name = name
        self.type = type
        self.size = size


# class MatrixSymbol(Symbol):
#     def __init__(self, name, type, size):
#         super().__init__(name, type)
#         self.size = size


class SymbolTable(object):
    def __init__(self): # parent scope and symbol table name
        self.scopes = [{}]

    def put(self, symbol): # put variable symbol or fundef under <name> entry
        self.scopes[-1][symbol.name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        for scope in self.scopes:
            if name in scope:
                return scope[name]
        
        return None

    def pushScope(self):
        self.scopes.append({})

    def popScope(self):
        self.scopes.pop()
