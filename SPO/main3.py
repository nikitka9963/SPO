from Lexer import Lexer
from Parser import Parser


def main():
    lex = Lexer()
    lex.setTokens()
    print(lex.getTokens())

    par = Parser(lex.getTokens())
    Tree = par.Tree()


if __name__ == '__main__':
    main()
