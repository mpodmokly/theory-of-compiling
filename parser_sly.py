from sly import Parser
from scanner_sly import Scanner
import AST

class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        #('nonassoc', IFX),
        #('nonassoc', ELSE),
        ('left', "+", "-", DOTADD, DOTSUB),
        ('left', "*", "/", DOTMUL, DOTDIV),
        ('right', UMINUS),
        ('left', "\'"),
    )

    @_('instructions_opt')
    def program(self, p):
        return AST.Instructions(p.instructions_opt)

    @_('instructions')
    def instructions_opt(self, p):
        return AST.Instructions(p.instructions)

    @_('')
    def instructions_opt(self, p):
        return AST.Instructions()

    @_('instructions instruction_if')
    def instructions(self, p):
        return AST.Instructions(p.instructions, p.instruction_if)

    @_('instructions instruction_rek')
    def instructions(self, p):
        return AST.Instructions(p.instructions, p.instruction_rek)

    @_('instructions instruction')
    def instructions(self, p):
        return AST.Instructions(p.instructions, p.instruction)

    @_('instruction_if')
    def instructions(self, p):
        return AST.Instructions(p.instruction_if)

    @_('instruction_rek')
    def instructions(self, p):
        return AST.Instructions(p.instruction_rek)

    @_('instruction')
    def instructions(self, p):
        return AST.Instructions(p.instruction)
    
    @_('IF "(" condition ")" instruction')# %prec IFX
    def instruction_if(self, p):
        return AST.IfStatement(p.condition, p.instruction)
    
    @_('IF "(" condition ")" instruction ELSE instruction_if')
    def instruction_if(self, p):
        return AST.IfStatement(p.condition, p.instruction, p.instruction_if)
    
    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction_if(self, p):
        return AST.IfStatement(p.condition, p.instruction0, p.instruction1)
    
    @_('FOR ID "=" expr ":" expr instruction')
    def instruction_rek(self, p):
        return AST.ForStatement(AST.Variable(p.ID), AST.Range(p.expr0, p.expr1), p.instruction)

    @_('WHILE "(" condition ")" instruction')
    def instruction_rek(self, p):
        return AST.WhileStatement(p.condition, p.instruction)

    @_('"{" instructions "}"')
    def instruction(self, p):
        return AST.Instructions(p.instructions)

    @_('BREAK ";"')
    def instruction(self, p):
        return AST.BreakStatement()
    
    @_('CONTINUE ";"')
    def instruction(self, p):
        return AST.ContinueStatement()

    @_('RETURN expr ";"')
    def instruction(self, p):
        return AST.ReturnStatement(p.expr)
    
    @_('PRINT elements ";"')
    def instruction(self, p):
        return AST.PrintStatement(p.elements)
    
    @_('ID "=" expr ";"')
    def instruction(self, p):
        return AST.Assignment(AST.Variable(p.ID), p.expr)
    
    @_('ID "[" elements "]" "=" expr ";"')
    def instruction(self, p):
        return AST.Assignment(AST.Reference(AST.Variable(p.ID), p.elements), p.expr)

    @_('ID ADDASSIGN expr ";"')
    def instruction(self, p):
        return AST.BinExpr("+=", AST.Variable(p.ID), p.expr)

    @_('ID SUBASSIGN expr ";"')
    def instruction(self, p):
        return AST.BinExpr("-=", AST.Variable(p.ID), p.expr)

    @_('ID MULASSIGN expr ";"')
    def instruction(self, p):
        return AST.BinExpr("*=", AST.Variable(p.ID), p.expr)

    @_('ID DIVASSIGN expr ";"')
    def instruction(self, p):
        return AST.BinExpr("/=", AST.Variable(p.ID), p.expr)

    @_('expr "\'"')
    def expr(self, p):
        return AST.UnExpr("\'", p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return AST.BinExpr("+", p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return AST.BinExpr("-", p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return AST.BinExpr("*", p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return AST.BinExpr("/", p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return AST.UnExpr("-", p.expr)

    @_('expr DOTADD expr')
    def expr(self, p):
        return AST.BinExpr(".+", p.expr0, p.expr1)

    @_('expr DOTSUB expr')
    def expr(self, p):
        return AST.BinExpr(".-", p.expr0, p.expr1)

    @_('expr DOTMUL expr')
    def expr(self, p):
        return AST.BinExpr(".*", p.expr0, p.expr1)

    @_('expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr("./", p.expr0, p.expr1)
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('EYE "(" expr ")"')
    def expr(self, p):
        return AST.EyeStatement(p.expr)

    @_('ONES "(" expr ")"')
    def expr(self, p):
        return AST.OnesStatement(p.expr)

    @_('ZEROS "(" expr ")"')
    def expr(self, p):
        return AST.ZerosStatement(p.expr)

    @_('"[" elements "]"')
    def expr(self, p):
        return AST.Vector(p.elements)

    @_('ID "[" elements "]"')
    def expr(self, p):
        pass

    @_('FLOATNUM')
    def expr(self, p):
        return AST.FloatNum(p.FLOATNUM)

    @_('INTNUM')
    def expr(self, p):
        return AST.IntNum(p.INTNUM)

    @_('STRING')
    def expr(self, p):
        return AST.String(p.STRING)

    @_('ID')
    def expr(self, p):
        return AST.Variable(p.ID)
    
    @_('elements "," expr')
    def elements(self, p):
        return AST.Elements(p.elements, p.expr)

    @_('expr')
    def elements(self, p):
        return p.expr

    @_('expr EQ expr')
    def condition(self, p):
        return AST.Condition("==", p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def condition(self, p):
        return AST.Condition("!=", p.expr0, p.expr1)

    @_('expr LESSEQ expr')
    def condition(self, p):
        return AST.Condition("<=", p.expr0, p.expr1)

    @_('expr MOREEQ expr')
    def condition(self, p):
        return AST.Condition(">=", p.expr0, p.expr1)

    @_('expr "<" expr')
    def condition(self, p):
        return AST.Condition("<", p.expr0, p.expr1)

    @_('expr ">" expr')
    def condition(self, p):
        return AST.Condition(">", p.expr0, p.expr1)
