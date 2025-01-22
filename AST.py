class Node(object):
    pass

class Instructions(Node):
    def __init__(self, lineno, instr_first = None, instr_second = None):
        self.lineno = lineno
        self.instr_first = instr_first
        self.instr_second = instr_second

class IntNum(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class FloatNum(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class String(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class Variable(Node):
    def __init__(self, lineno, name):
        self.lineno = lineno
        self.name = name

class Assignment(Node):
    def __init__(self, lineno, variable, value):
        self.lineno = lineno
        self.variable = variable
        self.value = value

class BinExpr(Node):
    def __init__(self, lineno, operator, left, right):
        self.lineno = lineno
        self.operator = operator
        self.left = left
        self.right = right

class UnExpr(Node):
    def __init__(self, lineno, operator, arg):
        self.lineno = lineno
        self.operator = operator
        self.arg = arg

class IfStatement(Node):
    def __init__(self, lineno, condition, true_statement, false_statement = None):
        self.lineno = lineno
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement

class ForStatement(Node):
    def __init__(self, lineno, variable, for_range, statement):
        self.lineno = lineno
        self.variable = variable
        self.for_range = for_range
        self.statement = statement

class Range(Node):
    def __init__(self, lineno, begin, end):
        self.lineno = lineno
        self.begin = begin
        self.end = end

class WhileStatement(Node):
    def __init__(self, lineno, condition, statement):
        self.lineno = lineno
        self.condition = condition
        self.statement = statement

class Condition(Node):
    def __init__(self, lineno, operator, left, right):
        self.lineno = lineno
        self.operator = operator
        self.left = left
        self.right = right

class PrintStatement(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class ReturnStatement(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class BreakStatement(Node):
    def __init__(self, lineno):
        self.lineno = lineno

class ContinueStatement(Node):
    def __init__(self, lineno):
        self.lineno = lineno

class EyeStatement(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class OnesStatement(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class ZerosStatement(Node):
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value

class Vector(Node):
    def __init__(self, lineno, elements):
        self.lineno = lineno
        self.elements = elements

class Reference(Node):
    def __init__(self, lineno, name, elements):
        self.lineno = lineno
        self.name = name
        self.elements = elements

class Elements(Node):
    def __init__(self, lineno, element1, element2):
        self.lineno = lineno
        self.element1 = element1
        self.element2 = element2
