#!/usr/bin/python
from collections import defaultdict
import AST
from SymbolTable import SymbolTable, VariableSymbol

ttype = defaultdict(lambda: defaultdict(dict))

ttype['+']['int']['int'] = 'int'
ttype['-']['int']['int'] = 'int'
ttype['*']['int']['int'] = 'int'
ttype['/']['int']['int'] = 'float'
ttype['+=']['int']['int'] = 'int'
ttype['-=']['int']['int'] = 'int'
ttype['*=']['int']['int'] = 'int'
ttype['/=']['int']['int'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'

for op in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

ttype['+']['vector']['vector'] = 'vector'
ttype['-']['vector']['vector'] = 'vector'
ttype['+=']['vector']['vector'] = 'vector'
ttype['-=']['vector']['vector'] = 'vector'

ttype['*']['vector']['vector'] = 'vector'

for op in ['.+', '.-', '.*', './']:
    ttype[op]['vector']['vector'] = 'vector'
    ttype[op]['vector']['int'] = 'vector'
    ttype[op]['vector']['float'] = 'vector'
    ttype[op]['int']['vector'] = 'vector'
    ttype[op]['float']['vector'] = 'vector'
    
ttype['TRANSPOSE']['vector'][None] = 'vector'
ttype['-']['int'][None] = 'int'
ttype['-']['float'][None] = 'float'

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, 'Global')
        self.loop_nesting = 0

    def error(self, node, msg):
        line = getattr(node, 'lineno', '?')
        print(f"Line {line}: {msg}")

    def visit_Instructions(self, node):
        for instr in node.list:
            self.visit(instr)

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol:
            return symbol.type, symbol.size
        else:
            self.error(node, f"Variable '{node.name}' not defined.")
            return None, None

    def visit_BinaryExpr(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        
        if not r1 or not r2 or r1[0] is None or r2[0] is None:
            return None, None

        type1, size1 = r1
        type2, size2 = r2
        op = node.op

        result_type = ttype[op][type1].get(type2)
        if not result_type:
            self.error(node, f"Incompatible types for '{op}': {type1} and {type2}")
            return None, None

        if type1 == 'vector' and type2 == 'vector':
            if op in ['+', '-', '.+', '.-', '.*', './', '+=', '-=']:
                if size1 != size2:
                    self.error(node, f"Matrix dimensions mismatch in '{op}': {size1} vs {size2}")
                    return None, None
                return result_type, size1
            
            elif op == '*':
                if size1[1] != size2[0]:
                    self.error(node, f"Invalid matrix dimensions for multiplication: {size1} * {size2}")
                    return None, None
                return result_type, (size1[0], size2[1])

        if type1 == 'vector': return result_type, size1
        if type2 == 'vector': return result_type, size2

        return result_type, None

    def visit_AssignmentExpr(self, node):
        res = self.visit(node.assigning)
        if not res or res[0] is None: return
        rhs_type, rhs_size = res

        if isinstance(node.assigned, AST.Variable):
            name = node.assigned.name
            if node.op == '=':
                self.symbol_table.put(name, VariableSymbol(name, rhs_type, rhs_size))
            else:
                symbol = self.symbol_table.get(name)
                if not symbol:
                    self.error(node, f"Variable '{name}' undefined.")
                elif not ttype[node.op][symbol.type].get(rhs_type):
                    self.error(node, f"Cannot use '{node.op}' with {symbol.type} and {rhs_type}")

        elif isinstance(node.assigned, AST.MatrixVariable):
            self.visit(node.assigned) 
            if rhs_type not in ['int', 'float']:
                self.error(node, "Only numbers can be assigned to matrix elements.")

    def visit_Matrix(self, node):
        if not node.vec_list:
            return 'vector', (0,0)
        
        _, size0 = self.visit(node.vec_list[0])
        cols = size0[0]
        rows = len(node.vec_list)

        for vec in node.vec_list[1:]:
            _, size = self.visit(vec)
            if size[0] != cols:
                self.error(node, "Matrix rows must have same length.")
                return 'vector', None
        
        return 'vector', (rows, cols)

    def visit_MatrixVector(self, node):
        for val in node.val_list:
            t, _ = self.visit(val)
            if t not in ['int', 'float']:
                self.error(node, "Matrix elements must be numbers.")
        return 'vector', (len(node.val_list),)

    def visit_MatrixVariable(self, node):
        name = node.name
        indices = node.val_list

        symbol = self.symbol_table.get(name)
        if not symbol or symbol.type != 'vector':
            self.error(node, f"Variable '{name}' is not a matrix or not defined.")
            return None, None

        for i, idx in enumerate(indices):
            t, _ = self.visit(idx)
            if t != 'int':
                self.error(node, "Indices must be integers.")
            
            if symbol.size and isinstance(idx, AST.IntNum):
                limit = symbol.size[i] if i < len(symbol.size) else 0
                if idx.value < 0 or idx.value >= limit:
                    self.error(node, f"Index {idx.value} out of bounds (limit {limit}).")
        
        return 'float', None

    def visit_Instance(self, node):
        args = node.instance_list
        dims = []
        for arg in args:
            t, _ = self.visit(arg)
            if t != 'int': 
                self.error(node, f"Arguments for {node.name} must be integers.")
            if isinstance(arg, AST.IntNum):
                dims.append(arg.value)
        
        if len(dims) == len(args):
            return 'vector', tuple(dims * 2 if len(dims)==1 else dims)
        return 'vector', None

    def visit_If(self, node):
        self.visit(node.condition)
        self.symbol_table = self.symbol_table.pushScope('if')
        self.visit(node.instructions)
        self.symbol_table = self.symbol_table.popScope()
        if node.else_instructions:
            self.symbol_table = self.symbol_table.pushScope('else')
            self.visit(node.else_instructions)
            self.symbol_table = self.symbol_table.popScope()

    def visit_While(self, node):
        self.loop_nesting += 1
        self.symbol_table = self.symbol_table.pushScope('while')
        self.visit(node.condition)
        self.visit(node.instructions)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_nesting -= 1

    def visit_For(self, node):
        self.loop_nesting += 1
        self.symbol_table = self.symbol_table.pushScope('for')
        self.symbol_table.put(node.iterator.name, VariableSymbol(node.iterator.name, 'int'))
        
        self.visit(node.start)
        self.visit(node.end)
        self.visit(node.instructions)
        
        self.symbol_table = self.symbol_table.popScope()
        self.loop_nesting -= 1

    def visit_Break(self, node):
        if self.loop_nesting == 0:
            self.error(node, "Break instruction outside loop")

    def visit_Continue(self, node):
        if self.loop_nesting == 0:
            self.error(node, "Continue instruction outside loop")

    def visit_Return(self, node):
        if node.value:
            self.visit(node.value)
    
    def visit_Print(self, node):
        self.visit(node.list)

    def visit_IntNum(self, node):
        return 'int', None

    def visit_FloatNum(self, node):
        return 'float', None

    def visit_String(self, node):
        return 'string', None

    def visit_UnaryExpr(self, node):
        r = self.visit(node.right)
        if not r or not r[0]: return None, None
        t, size = r
        
        if node.op == 'TRANSPOSE':
            if t != 'vector':
                self.error(node, "Transpose only valid for matrices")
                return None, None
            if size and len(size) == 2:
                return 'vector', (size[1], size[0])
            return 'vector', size
        
        return t, size