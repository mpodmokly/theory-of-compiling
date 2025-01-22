import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory = Memory()

    @on('node')
    def visit(self, node):
        pass
    
    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)
    
    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)
    
    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Instructions)
    def visit(self, node):
        if node.instr_first is not None:
            self.visit(node.instr_first)
        if node.instr_second is not None:
            self.visit(node.instr_second)
    
    @when(AST.IfStatement)
    def visit(self, node):
        condition = self.visit(node.condition)
        
        if condition:
            self.visit(node.true_statement)
        elif node.false_statement is not None:
            self.visit(node.false_statement)

    @when(AST.Condition)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.operator == "==":
            return left == right
        if node.operator == "!=":
            return left != right
    
    @when(AST.Variable)
    def visit(self, node):
        if self.memory.contains(node.name):
            return self.memory.get(node.name)
        return None

    @when(AST.Assignment)
    def visit(self, node):
        self.visit(node.variable)
        value = self.visit(node.value)
        self.memory.put(node.variable.name, value)
    
    @when(AST.BinExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.operator == "+":
            return left + right
        elif node.operator == "-":
            return left - right
        elif node.operator == "*":
            return left * right
        elif node.operator == "/":
            return left / right
    
    @when(AST.PrintStatement)
    def visit(self, node):
        value = self.visit(node.value)
        print(value)
    
    @when(AST.WhileStatement)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r
