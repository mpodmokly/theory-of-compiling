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
        for memory in reversed(self.stack):
            if name in memory:
                memory[name] = value
                return
        
        self.stack[-1][name] = value
    
    def push(self):
        self.stack.append({})
    
    def pop(self):
        self.stack.pop()
