import sys
from sly import Lexer


class Scanner(Lexer):
    # Set of token names.   This is always required
    tokens = {
        'NUMBER', 'ID', 'WHILE', 'IF', 'ELSE', 'PRINT',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'ASSIGN', 'MULASSIGN', 'DIVASSIGN', 'ADDASSIGN', 'SUBASSIGN',
        'EQ', 'LT', 'LE', 'GT', 'GE', 'NE',
        'FOR',
        'DOTPLUS', 'DOTMINUS', 'DOTTIMES', 'DOTDIV',
        'IF', 'ELSE', 'FOR', 'WHILE',
        'BREAK', 'CONTINUE', 'RETURN',
        'EYE', 'ZEROS', 'ONES',
        'PRINT',
        'INT',
        'FLOAT',
        "STRING",
        }



    # String containing ignored characters
    ignore = '  \t'

    # Regular expression rules for tokens
    #ASSIGN  = r'='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='

    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    
    DOTPLUS = r'\.\+'
    DOTMINUS= r'\.-'
    DOTTIMES= r'\.\*'
    DOTDIV  = r'\./'
    
    literals = { '(', ')', '{', '}', '[', ']', ':',"'", ',', ';', '=' }
    
    
    
    EQ = r'=='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    IF = r'if'
    ELSE = r'else'
    FOR = r'for'
    WHILE = r'while'

    BREAK = r'break'
    CONTINUE = r'continue'
    RETURN = r'return'

    EYE = r'eye'
    ZEROS = r'zeros'
    ONES = r'ones'

    PRINT = r'print'

    FLOAT = r'([0-9]?|[1-9][0-9]*)\.[0-9]*(E-?[1-9][0-9]*)?'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    INT = r'[1-9][0-9]*(E-?[1-9][0-9]*)?'

    STRING = r'"'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    # ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    # ID['for'] = FOR
    # ID['else'] = ELSE
    # ID['while'] = WHILE
    # ID['print'] = PRINT

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type}({tok.value})")


  