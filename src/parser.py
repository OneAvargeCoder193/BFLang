from lark import Lark, Transformer, v_args
from builder import Builder

@v_args(inline=True)
class Tree(Transformer):
    def __init__(self):
        self.builder = Builder()
    
    def statements(self, *args):
        print("statements", args)
    
    def statement(self, *args):
        print("statement", args)
    
    def sum(self, *args):
        print("sum", args)
    
    def product(self, *args):
        print("product", args)
    
    def atom(self, *args):
        print("atom", args)
    
    def number(self, *args):
        print("number", args)

with open("src/main.lark", "r") as file:
    parser = Lark(file, parser='lalr', start="statements")

with open("main.txt", "r") as f:
    tree = parser.parse(f.read())
    print(Tree().transform(tree))
