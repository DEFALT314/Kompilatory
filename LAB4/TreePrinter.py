import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

INDENT = "|  "


class TreePrinter:

    # @addToClass(AST.Node)
    # def printTree(self, indent=0):
    #     raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(INDENT * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(INDENT * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(INDENT * indent + f'{self.text}')

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(INDENT * indent + self.name)

    @addToClass(AST.BinaryExpr)
    def printTree(self, indent=0):
        print(INDENT * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.AssignmentExpr)
    def printTree(self, indent=0):
        print(INDENT * indent + self.op)
        self.assigned.printTree(indent + 1)
        self.assigning.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(INDENT * indent + "IF")
        self.condition.printTree(indent + 1)
        print(INDENT * indent + "THEN")
        self.instructions.printTree(indent + 1)
        if self.else_instructions:
            print(INDENT * indent + "ELSE")
            self.else_instructions.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print(INDENT * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.instructions.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(INDENT * indent + "FOR")
        self.iterator.printTree(indent + 1)
        print(INDENT * (indent + 1) + "RANGE")
        self.start.printTree(indent + 2)
        self.end.printTree(indent + 2)
        self.instructions.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(INDENT * indent + "PRINT")
        for e in self.list:
            e.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print(INDENT * indent + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print(INDENT * indent + "CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(INDENT * indent + "RETURN")
        if self.value:
            self.value.printTree(indent + 1)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instr in self.list:
            instr.printTree(indent)

    @addToClass(AST.Instance)
    def printTree(self, indent=0):
        print(INDENT * indent + self.name)
        for instance in self.instance_list:
            instance.printTree(indent + 1)

    # @addToClass(AST.Reference)
    # def printTree(self, indent=0):
    #     print(INDENT * indent + "REF")
    #     print(INDENT * (indent + 1) + self.name)
    #     for instance in self.instance_list:
    #         instance.printTree(indent + 1)


    @addToClass(AST.MatrixVariable)
    def printTree(self, indent=0):
        print(INDENT * indent + "REF")
        print(INDENT * (indent + 1) + self.name)
        for instance in self.val_list:
            instance.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        print(INDENT * indent + self.op)
        self.right.printTree(indent + 1)


    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        for instance in self.vec_list:
            instance.printTree(indent)


    @addToClass(AST.MatrixVector)
    def printTree(self, indent=0):
        print(INDENT * indent + "VECTOR")
        for instance in self.val_list:
            instance.printTree(indent + 1)