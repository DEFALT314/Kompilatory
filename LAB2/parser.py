from sly import Parser
from scanner import Scanner


class Mparser(Parser):

    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        # ("right", '=', 'MULASSIGN', 'DIVASSIGN', 'ADDASSIGN', 'SUBASSIGN'),
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", 'EQ', 'LT', 'LE', 'GT', 'GE', 'NE'),
        ("left", 'ADD', 'SUB'),
        ("left", 'MUL', 'DIVIDE'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("right", 'UMINUS')
    )

    @_('instructions_opt')
    def program(self, p):
        pass

    @_('instructions')
    def instructions_opt(self, p):
        pass

    @_('')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction')
    def instructions(self, p):
        pass

    @_('instruction')
    def instructions(self, p):
        pass

    @_('assignment',
       'if_stmt',
       'while_stmt',
       'for_stmt',
       'flow_stmt',
       'print_stmt',
       'block_stmt',
       'expr ";"')
    def instruction(self, p):
        pass
    
    @_('BREAK ";"',
       'CONTINUE ";"',
       'RETURN ";"',
       'RETURN expr ";"')
    def flow_stmt(self, p):
        pass

    @_('IF "(" expr ")" instruction ELSE instruction',
       'IF "(" expr ")" instruction %prec IFX')
    def if_stmt(self, p):
        pass
    
    @_('WHILE "(" expr ")" instruction')
    def while_stmt(self, p):
        pass
    
    @_('FOR ID "=" INTNUM ":" INTNUM instruction')
    def for_stmt(self, p):
        pass
    
    @_('"{" instructions "}"')
    def block_stmt(self, p):
        pass
    
    @_('PRINT expr_list ";"')
    def print_stmt(self, p):
        pass
    
    @_('lvalue "=" expr ";"',
       'lvalue ADDASSIGN expr ";"',
       'lvalue SUBASSIGN expr ";"',
       'lvalue MULASSIGN expr ";"',
       'lvalue DIVASSIGN expr ";"')
    def assignment(self, p):
        pass
    
    @_('ID',
       'ID "[" expr_list "]"')
    def lvalue(self, p):
        pass


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
        pass

    
    
    @_('expr "\'"',
       'ID',
       'INTNUM',
       'FLOAT',
       'STRING',
       'matrix',
       'EYE "(" expr_list ")"',
       'ZEROS "(" expr_list ")"',
       'ONES "(" expr_list ")"',
       'ID "[" expr_list "]"',
       '"(" expr ")"',
       'SUB expr %prec UMINUS')
    def expr(self, p):
        pass
    
    @_('expr')
    def expr_list(self, p):
        pass

    @_('expr_list "," expr')
    def expr_list(self, p):
        pass
        
    @_('"[" row_list "]"')
    def matrix(self, p):
        pass
    
    @_('row_list ";" row', 'row')
    def row_list(self, p):
        pass
    
    @_('expr_list')
    def row(self, p):
        pass