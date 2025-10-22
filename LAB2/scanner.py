import sys
from sly import Lexer


class Scanner(Lexer):
    # Set of token names.   This is always required
    tokens = {
        'INTNUM', 'ID', 'WHILE', 'IF', 'ELSE', 'PRINT',
        'ADD', 'SUB', 'MUL', 'DIVIDE',
        'ASSIGN', 'MULASSIGN', 'DIVASSIGN', 'ADDASSIGN', 'SUBASSIGN',
        'EQ', 'LT', 'LE', 'GT', 'GE', 'NE',
        'FOR',
        'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
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
    ignore_comment = r'\#.*'

    # Regular expression rules for tokens
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='

    ADD    = r'\+'
    SUB   = r'-'
    MUL   = r'\*'
    DIVIDE  = r'/'
    
    DOTADD = r'\.\+'
    DOTSUB= r'\.-'
    DOTMUL= r'\.\*'
    DOTDIV  = r'\./'
    
    literals = { '(', ')', '{', '}', '[', ']', ':',"'", ',', ';', '=' }
    
    EQ = r'=='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='


    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    FLOAT = r'(0\.|[1-9][0-9]*\.|\.[0-9])[0-9]*(([Ee][+-]?)?[1-9][0-9]*)?'
    
    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'(".*?")|(\'.*?\')')
    def STRING(self, t):
        t.value = str(t.value)
        return t


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


  