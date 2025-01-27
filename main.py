import sys
from scanner_sly import Scanner
from parser_sly import Mparser
from tree_printer import TreePrinter
from type_checker import TypeChecker
from interpreter import Interpreter


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()

    try:
        ast = parser.parse(lexer.tokenize(text))
    except SyntaxError as err:
        print(err)
        sys.exit(0)

    if lexer.error_handled:
        sys.exit(0)
    
    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    if typeChecker.error_handled:
        sys.exit(0)
    
    interpreter = Interpreter()
    try:
        interpreter.visit(ast)
    except ZeroDivisionError as err:
        print(err)
