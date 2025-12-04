

class Memory:

    def __init__(self): # memory name
        self.memo = dict()

    def has_key(self, name):  # variable name
        if name in self.memo:
            return True
        return False

    def get(self, name):         # gets from memory current value of variable <name>
        return self.memo[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memo[name]=value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = [memory] if memory else []

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in self.stack[::-1]:
            if memory.has_key(name):
                return memory.get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        if self.stack:
            self.stack[-1].put(name, value)
            return True
        else:
            return False

    def set(self, name, value): # sets variable <name> to value <value>
        if self.stack:
            for memory in self.stack[::-1]:
                if memory.has_key(name):
                    memory.put(name, value)
                    return True
        return False
            

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        self.stack.pop()

