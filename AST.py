class Node(object):
    pass

class Instructions(Node):
    def __init__(self, instr_first = None, instr_second = None):
        self.instr_first = instr_first
        self.instr_second = instr_second

class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinExpr(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class UnExpr(Node):
    def __init__(self, operator, arg):
        self.operator = operator
        self.arg = arg

class Assignment(Node):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

class IfStatement(Node):
    def __init__(self, condition, true_statement, false_statement = None):
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement

class ForStatement(Node):
    def __init__(self, variable, for_range, statement):
        self.variable = variable
        self.for_range = for_range
        self.statement = statement

class Range(Node):
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

class WhileStatement(Node):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

class Condition(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class ReturnStatement(Node):
    def __init__(self, value):
        self.value = value

class PrintStatement(Node):
    def __init__(self, value):
        self.value = value

class BreakStatement(Node):
    pass

class ContinueStatement(Node):
    pass

class EyeStatement(Node):
    def __init__(self, value):
        self.value = value

class OnesStatement(Node):
    def __init__(self, value):
        self.value = value

class ZerosStatement(Node):
    def __init__(self, value):
        self.value = value

class Vector(Node):
    def __init__(self, elements):
        self.elements = elements

class Reference(Node):
    def __init__(self, name, elements):
        self.name = name
        self.elements = elements

class Elements(Node):
    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2

class Error(Node):
    def __init__(self):
        pass
