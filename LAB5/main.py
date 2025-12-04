
import sys
import ply.yacc as yacc
from parser import Mparser
from scanner import Scanner
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "m_file/primes.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # Mparser = Mparser()
    # parser = yacc.yacc(module=Mparser)
    # text = file.read()

    # ast = parser.parse(text, lexer=Mparser.scanner)

    # # Below code shows how to use visitor
    # typeChecker = TypeChecker()   
    # typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)

    # ast.accept(Interpreter())
    # # in future
    # # ast.accept(OptimizationPass1())
    # # ast.accept(OptimizationPass2())
    # # ast.accept(CodeGenerator())

    text = file.read()

    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    print(type(ast))

    if ast:
        try:
            typeChecker = TypeChecker()
            typeChecker.visit(ast)
        except Exception as e:
            import traceback
            traceback.print_exc()
        else:
            interpreter = Interpreter()
            interpreter.visit(ast)
    else:
        print("Błąd parsowania: nie wygenerowano AST.")
    