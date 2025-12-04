
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack()
        self.global_memory = Memory()

        self.operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,

            ".+": lambda a, b: a + b,
            ".-": lambda a, b: a - b,
            ".*": lambda a, b: a * b,
            "./": lambda a, b: a / b,

            "+=": lambda a, b: a + b,
            "-=": lambda a, b: a - b,
            "*=": lambda a, b: a * b,
            "/=": lambda a, b: a / b,

            "<": lambda a, b: a < b,
            ">": lambda a, b: a > b,
            "<=": lambda a, b: a <= b,
            ">=": lambda a, b: a >= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            
        }


    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value
    
    @when(AST.Variable)
    def visit(self, node):
        res = self.memory_stack.get(node.name)
        if res is None:
            return self.global_memory.get(node.name)
        else:
            return res

    @when(AST.String)
    def visit(self, node):
        return node.text



    @when(AST.BinaryExpr)
    def visit(self, node):
        op = node.op
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        #print(r1,r2, type(r1), type(r2))
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval
        return self.operations[op](r1, r2)


    @when(AST.Instance)
    def visit(self, node):
        res = None
        match node.name:
            case "eye":
                #print("====",self.visit(*node.instance_list))
                res = np.eye(self.visit(*node.instance_list))
            case "ones":
                res = np.ones(self.visit(*node.instance_list))
            case "zeros":
                res = np.zeros((self.visit(node.instance_list[0]), self.visit(node.instance_list[1])))
        return res

    @when(AST.UnaryExpr)
    def visit(self, node):
        op = node.op
        r2 = self.visit(node.right)
        return self.operations[op](0, r2)

    @when(AST.RelationExpr)
    def visit(self, node):
        op = node.op
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)

        return self.operations[op](r1, r2)

    @when(AST.AssignmentExpr)
    def visit(self, node):
        op = node.op
        # print(node.assigning)
        assigning = self.visit(node.assigning)
        # print(assigning)
        # print(self.memory_stack.stack[0].memo)
        #print(op, type(op), assigned, assigning)
        if isinstance(node.assigned,AST.MatrixVariable):
            assigned_name = node.assigned.name
            matrix = self.global_memory.get(assigned_name)
            x,y = map(self.visit,node.assigned.val_list)
            if op == "=":
                matrix[x,y] = assigning
                self.global_memory.put(assigned_name, matrix)

            elif op in ["+=", "-=", "*=", "/="]:
                assigned = self.visit(node.assigned)
                matrix[x,y] = self.operations[op](matrix[x,y], assigning)
                self.global_memory.put(assigned_name, matrix)

        else:
            assigned_name = node.assigned.name
            if op == "=":
                self.global_memory.put(assigned_name, assigning)
                # if not self.memory_stack.set(assigned, assigning):
                #     memory = Memory()
                #     memory.put(self, assigned, assigning)
                #     self.memory_stack.push(memory)
            elif op in ["+=", "-=", "*=", "/="]:
                #print("xd")
                assigned = self.visit(node.assigned)
                assigning_new = self.operations[op](assigned, assigning)
                #print(assigned, assigning_new, type(assigned), type(assigning_new))
                self.global_memory.put(assigned_name, assigning_new)
                # assigning_new = self.operations[op](assigned, assigning)
                # if not self.memory_stack.set(assigned, assigning_new):
                #     memory = Memory()
                #     memory.put(self, assigned, assigning_new)
                #     self.memory_stack.push(memory)



    @when(AST.If)
    def visit(self, node):
        if self.visit(node.condition):
            return self.visit(node.instructions)
        else:
            return self.visit(node.else_instructions)


# simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        memory = Memory()
        self.memory_stack.push(memory)
        while self.visit(node.condition):
            try:
                self.visit(node.instructions)
            except ContinueException:
                continue
            except BreakException:
                break
        self.memory_stack.pop()

    @when(AST.For)
    def visit(self, node):
        memory = Memory()
        self.memory_stack.push(memory)
        iterator_name = node.iterator.name
        start = self.visit(node.start)
        end = self.visit(node.end)
        instructions = node.instructions
        for i in range(start, end+1):
            if not self.memory_stack.set(iterator_name, i):
                self.memory_stack.insert(iterator_name, i)
            try:
                #print(self.memory_stack.stack[0].memo)
                self.visit(instructions)
            except ContinueException:
                continue
            except BreakException:
                break

        self.memory_stack.pop()


    @when(AST.Break)
    def visit(self, node):
        raise BreakException()


    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()


    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException()


    @when(AST.Print)
    def visit(self, node):
        for element in node.list:
            print(">" ,self.visit(element), end=" ")
        print()


    @when(AST.Instructions)
    def visit(self, node):
        for element in node.list:
            #print(self.visit(element))
            self.visit(element)


    @when(AST.MatrixVariable)
    def visit(self, node):
        # if self.memory_stack.get(node.name) is None:
        matrix = self.global_memory.get(node.name)
        x, y = map(self.visit, node.val_list)
        return matrix[x, y]



    @when(AST.MatrixVector)
    def visit(self, node):
        return np.array(self.visit(node.val_list))


    @when(AST.Matrix)
    def visit(self, node):
        return np.array([self.visit(element) for element in node.vec_list])


    @when(AST.Error)
    def visit(self, node):
        pass
      

