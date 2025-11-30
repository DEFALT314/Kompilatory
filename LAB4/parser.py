from sly import Parser
from scanner import Scanner
from AST import *

class Mparser(Parser):

    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", 'EQ', 'LT', 'LE', 'GT', 'GE', 'NE'),
        ("left", 'ADD', 'SUB'),
        ("left", 'MUL', 'DIVIDE'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("right", 'UMINUS'),
        ("left", '\'')
    )

    @_('instructions_opt')
    def program(self, p):
        return p.instructions_opt

    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')
    def instructions_opt(self, p):
        return Instructions([])

    @_('instructions instruction')
    def instructions(self, p):
        p.instructions.list.append(p.instruction)
        return p.instructions

    @_('instruction')
    def instructions(self, p):
        return Instructions([p.instruction])

    @_('assignment',
       'if_stmt',
       'while_stmt',
       'for_stmt',
       'flow_stmt',
       'print_stmt',
       'block_stmt',
       'expr ";"')
    def instruction(self, p):
        return p[0]
    
    @_('BREAK ";"')
    def flow_stmt(self, p):
        node = Break()
        node.lineno = p.lineno
        return node

    @_('CONTINUE ";"')
    def flow_stmt(self, p):
        node = Continue()
        node.lineno = p.lineno
        return node

    @_('RETURN ";"')
    def flow_stmt(self, p):
        node = Return(None)
        node.lineno = p.lineno
        return node

    @_('RETURN expr ";"')
    def flow_stmt(self, p):
        node = Return(p.expr)
        node.lineno = p.lineno
        return node


    @_('IF "(" expr ")" instruction ELSE instruction')
    def if_stmt(self, p):
        return If(p.expr, p.instruction0, p.instruction1)

    @_('IF "(" expr ")" instruction %prec IFX')
    def if_stmt(self, p):
        return If(p.expr, p.instruction, None)
    
    @_('WHILE "(" expr ")" instruction')
    def while_stmt(self, p):
        return While(p.expr, p.instruction)

    @_('ID')
    def for_interval(self, p):
        return Variable(p[0])

    @_('INTNUM')
    def for_interval(self, p):
        return IntNum(p[0])
    
    @_('FOR ID "=" for_interval ":" for_interval instruction')
    def for_stmt(self, p):
        return For(Variable(p.ID), p.for_interval0, p.for_interval1, p.instruction)
    
    @_('"{" instructions "}"')
    def block_stmt(self, p):
        return p.instructions
    
    @_('PRINT expr_list ";"')
    def print_stmt(self, p):
        return Print(p.expr_list)
    
    @_('lvalue "=" expr ";"',
       'lvalue ADDASSIGN expr ";"',
       'lvalue SUBASSIGN expr ";"',
       'lvalue MULASSIGN expr ";"',
       'lvalue DIVASSIGN expr ";"')
    def assignment(self, p):
        node = AssignmentExpr(p[1], p.lvalue, p.expr)
        node.lineno = p.lineno
        return node
    
    @_('ID')
    def lvalue(self, p):
        return Variable(p.ID)

    @_('ID "[" expr_list "]"')
    def lvalue(self, p):
        return MatrixVariable(p.ID, p.expr_list)
    @_('expr ADD expr',
       'expr SUB expr',
       'expr MUL expr',
       'expr DIVIDE expr',
       'expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr',
       'expr EQ expr',
       'expr NE expr',
       'expr LT expr',
       'expr LE expr',
       'expr GT expr',
       'expr GE expr')
    def expr(self, p):
        node = BinaryExpr(p[1], p.expr0, p.expr1)
        node.lineno = p.lineno
        return node
    

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr 
    
    @_('ID "[" expr_list "]"')
    def expr(self, p):
        node = MatrixVariable(p.ID, p.expr_list)
        node.lineno = p.lineno
        return node
    
    @_('ID')
    def expr(self, p):
        node = Variable(p.ID)
        node.lineno = p.lineno
        return node
      
    @_('INTNUM')
    def expr(self, p):
        return IntNum(p.INTNUM)

    @_('FLOAT')
    def expr(self, p):
        return FloatNum(p.FLOAT)

    @_('STRING')
    def expr(self, p):
        return String(p.STRING)

    @_('expr "\'"')
    def expr(self, p):
        return UnaryExpr("TRANSPOSE", p.expr)
      

       
    @_('EYE "(" expr_list ")"',
       'ZEROS "(" expr_list ")"',
       'ONES "(" expr_list ")"')
    def expr(self, p):
        return Instance(p[0], p.expr_list)

    
    @_('SUB expr %prec UMINUS')
    def expr(self, p):
        return UnaryExpr(p.SUB, p.expr)
    
    @_('expr')
    def expr_list(self, p):
        return [p.expr]

    @_('expr_list "," expr')
    def expr_list(self, p):
        p.expr_list.append(p.expr)
        return p.expr_list
    
    @_('matrix')
    def expr(self, p):
        return p.matrix

    @_('"[" expr_list "]"')
    def matrix(self, p):
        if p.expr_list and isinstance(p.expr_list[0], Matrix):
            
            real_rows = []
            for elem in p.expr_list:
                if isinstance(elem, Matrix):

                    if elem.vec_list:
                        real_rows.append(elem.vec_list[0])
                else:
                    node = Matrix([MatrixVector(p.expr_list)])
                    node.lineno = p.lineno
                    return node
            
            node = Matrix(real_rows)
            node.lineno = p.lineno
            return node
        vector = MatrixVector(p.expr_list)
        node = Matrix([vector])
        node.lineno = p.lineno
        return node