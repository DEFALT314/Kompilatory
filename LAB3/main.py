import sys
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter

if __name__ == "__main__":
    lexer = Scanner()
    parser = Mparser()

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example3.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    tree = parser.parse(lexer.tokenize(text))
    if tree:
        tree.printTree()

