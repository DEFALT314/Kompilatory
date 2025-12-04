

class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class String(Node):
    def __init__(self, text):
        self.text = text


class BinaryExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

###



class Instance(Node):
    def __init__(self, name, instance_list):
        self.name = name
        self.instance_list = instance_list


# class Reference(Node):
#     def __init__(self, name, instance_list):
#         self.name = name
#         self.instance_list = instance_list


class UnaryExpr(Node):
    def __init__(self, op, right):
        self.op = op
        self.right = right


class RelationExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssignmentExpr(Node):
    def __init__(self, op, assigned, assigning):
        self.op = op
        self.assigned = assigned
        self.assigning = assigning


class If(Node):
    def __init__(self, condition, instructions, else_instructions):
        self.condition = condition
        self.instructions = instructions
        self.else_instructions = else_instructions


class While(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions


class For(Node):
    def __init__(self, iterator, start, end, instructions):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.instructions = instructions


class Break(Node):
    def __init__(self):
        pass


class Continue(Node):
    def __init__(self):
        pass


class Return(Node):
    def __init__(self, value):
        self.value = value


class Print(Node):
    def __init__(self, list):
        self.list = list


class Instructions(Node):
    def __init__(self, list):
        self.list = list


class MatrixVariable(Node):
    def __init__(self, name, val_list):
        self.name = name
        self.val_list = val_list


class MatrixVector(Node):
    def __init__(self, val_list):
        self.val_list = val_list


class Matrix(Node):
    def __init__(self, vec_list):
        self.vec_list = vec_list


class Error(Node):
    def __init__(self):
        pass
      
