from lexer import Lexer
from stackMachine import StackMachine
from parser import Parser

lex = Lexer()
lex.get_term('db.txt')
print('Tokens:', lex.list_tokens)

par = Parser(lex.list_tokens)
Tree = par.S()
print('Tree:\n', Tree)

StackMachine = StackMachine(Tree.children)
StackMachine.start()
