import sys
from scanner_sly import Scanner
from parser_sly import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()
    ast = parser.parse(lexer.tokenize(text))

    if lexer.error_handled or parser.error_handled:
        sys.exit(0)
    
    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    if typeChecker.error_handled:
        sys.exit(0)
    
    ast.accept(Interpreter())

    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
