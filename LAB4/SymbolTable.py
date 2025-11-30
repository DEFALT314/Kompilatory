#!/usr/bin/python


class Symbol(object):
    def __init__(self, name, type, size=None):
        self.name = name
        self.type = type
        self.size = size

class VariableSymbol(Symbol):
    def __init__(self, name, type, size=None):
        super().__init__(name, type, size)

class SymbolTable(object):

    def __init__(self, parent, name): 
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol): 
        self.symbols[name] = symbol

    def get(self, name): 
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent