
import sys
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "control_transfer.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    if ast:
        try:
            typeChecker = TypeChecker()
            typeChecker.visit(ast)
        except Exception as e:
            import traceback
            traceback.print_exc()
    else:
        print("Błąd parsowania: nie wygenerowano AST.")
