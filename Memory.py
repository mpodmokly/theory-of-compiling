class Memory:
    def __init__(self):
        self.scope = {}

    def contains(self, name):  # variable name
        return name in self.scope

    def get(self, name):         # gets from memory current value of variable <name>
        return self.scope[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.scope[name] = value


class MemoryStack:
    def __init__(self, memory = None): # initialize memory stack with memory <memory>
        pass

    def get(self, name):     # gets from memory stack current value of variable <name>
        pass

    def insert(self, name, value):#inserts into memory stack variable <name> with value <value>
        pass

    def set(self, name, value): # sets variable <name> to value <value>
        pass

    def push(self, memory):     # pushes memory <memory> onto the stack
        pass

    def pop(self):              # pops the top memory from the stack
        pass
