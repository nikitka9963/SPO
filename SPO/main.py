from lexer import Lexer
from stackMachine import StackMachine
from parser import Parser

lex = Lexer()
lex.get_term('db.txt')

par = Parser(lex.list_tokens)
Tree = par.S()

print('Tokens:', lex.list_tokens)
print(Tree)

sm = StackMachine(Tree.children)
sm.start()
