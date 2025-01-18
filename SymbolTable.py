class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):
    def __init__(self):
        self.scopes = [{}]

    def put(self, symbol):
        self.scopes[-1][symbol.name] = symbol

    def get(self, name):
        for scope in self.scopes:
            if name in scope:
                return scope[name]
        
        return None

    def pushScope(self):
        self.scopes.append({})

    def popScope(self):
        self.scopes.pop()
