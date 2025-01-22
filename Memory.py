class MemoryStack:
    def __init__(self):
        self.stack = [{}]

    def contains(self, name):
        for memory in self.stack:
            if name in memory:
                return True
        
        return False

    def get(self, name):
        for memory in reversed(self.stack):
            if name in memory:
                return memory[name]

    def put(self, name, value):
        self.stack[-1][name] = value
    
    def push(self):
        self.stack.append({})
    
    def pop(self):
        self.stack.pop()


# class MemoryStack:
#     def __init__(self, memory = None): # initialize memory stack with memory <memory>
#         pass

#     def get(self, name):     # gets from memory stack current value of variable <name>
#         pass

#     def insert(self, name, value):#inserts into memory stack variable <name> with value <value>
#         pass

#     def set(self, name, value): # sets variable <name> to value <value>
#         pass

#     def push(self, memory):     # pushes memory <memory> onto the stack
#         pass

#     def pop(self):              # pops the top memory from the stack
#         pass
