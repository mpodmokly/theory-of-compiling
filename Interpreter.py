import AST
import SymbolTable
from Memory import MemoryStack
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack()

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
            self.memory_stack.push()
            self.visit(node.true_statement)
            self.memory_stack.pop()
        elif node.false_statement is not None:
            self.memory_stack.push()
            self.visit(node.false_statement)
            self.memory_stack.pop()
    
    @when(AST.Condition)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.operator == "==":
            return left == right
        if node.operator == "!=":
            return left != right
        if node.operator == "<=":
            return left <= right
        if node.operator == ">=":
            return left >= right
        if node.operator == "<":
            return left < right
        if node.operator == ">":
            return left > right
    
    @when(AST.ForStatement)
    def visit(self, node):
        begin, end = self.visit(node.for_range)
        self.memory_stack.push()

        for i in range(begin, end + 1):
            self.memory_stack.put(node.variable.name, i)
            self.visit(node.statement)
        
        self.memory_stack.pop()
    
    @when(AST.Range)
    def visit(self, node):
        begin = self.visit(node.begin)
        end = self.visit(node.end)
        return begin, end

    @when(AST.WhileStatement)
    def visit(self, node):
        self.memory_stack.push()

        while self.visit(node.condition):
            self.visit(node.statement)
        
        self.memory_stack.pop()
    
    # return
    # continue
    # break
    
    @when(AST.PrintStatement)
    def visit(self, node):
        value = self.visit(node.value)
        print(value)
    
    @when(AST.Variable)
    def visit(self, node):
        if self.memory_stack.contains(node.name):
            return self.memory_stack.get(node.name)
        return None

    @when(AST.Assignment)
    def visit(self, node):
        #self.visit(node.variable)
        value = self.visit(node.value)
        self.memory_stack.put(node.variable.name, value)
    
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
