import sys
from sly import Lexer

class Scanner(Lexer):
    ignore = " \t"
    literals = "=();':,{}[]+-*/<>"
    tokens = {ID, DOTADD, DOTSUB, DOTMUL, DOTDIV, ADDASSIGN,
              SUBASSIGN, MULASSIGN, DIVASSIGN, EQ, NOTEQ, LESSEQ,
              MOREEQ, IF, ELSE, FOR, WHILE, BREAK, CONTINUE,
              RETURN, EYE, ZEROS, ONES, PRINT, INTNUM, FLOATNUM,
              STRING}
    
    DOTADD = r".\+"
    DOTSUB = r".-"
    DOTMUL = r".\*"
    DOTDIV = r"./"
    ADDASSIGN = r"\+="
    SUBASSIGN = r"-="
    MULASSIGN = r"\*="
    DIVASSIGN = r"/="
    EQ = r"=="
    NOTEQ = r"!="
    LESSEQ = r"<="
    MOREEQ = r">="

    STRING = r"(\".*?\")|(\'.*?\')"
    FLOATNUM = r"-?()"
    INTNUM = r"-?\d+"

    ID = r"[a-zA-Z_][a-zA-Z0-9]*"
    ID["if"] = IF
    ID["else"] = ELSE
    ID["for"] = FOR
    ID["while"] = WHILE
    ID["break"] = BREAK
    ID["continue"] = CONTINUE
    ID["return"] = RETURN
    ID["eye"] = EYE
    ID["zeros"] = ZEROS
    ID["ones"] = ONES
    ID["print"] = PRINT

    ignore_comment = r"#.*"

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' in line {t.lineno}")
        self.index += 1


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    
    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type}({tok.value})")
