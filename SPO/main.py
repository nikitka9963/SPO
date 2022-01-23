from lexer import Lexer
from stackMachine import StackMachine
from parser import Parser

lex = Lexer()
lex.get_term('db.txt')

# par = Parser(lex.list_tokens)
tmp = lex.optTerm()
par = Parser(tmp)
Tree = par.S()

print('Tokens:', tmp)
print(Tree.children)

sm = StackMachine(Tree.children)
sm.start()

# sm.optTriad()
# sm.convToPol()
