import re


class Lexer():
    tokens = {"VAR": "^[а-яА-Яa-zA-Z0-9_]+$",
              "STRING":  "\"([^\"\n]|(\\\\\"))*\"",
              "STRING_BEG": "\"([^\"\n]|(\\\\\"))*",
              "ASSIGN": "^=$",
              "CONCAT": "^\,$",
              "OR": "^\|$",
              "END": "^\.$",
              "COND_OCC_L": "^\[$",
              "COND_OCC_R": "^\]$",
              "REPETITION_L": "^\{$",
              "REPETITION_R": "^\}$",
              "GROUPING_L": "^\($",
              "GROUPING_R" : "^\)$"}

    def __init__(self):
        self.tokensList = []

    def getNameToken(self, item):
        for key in self.tokens.keys():
            if re.fullmatch(self.tokens[key], item):
                return key

        return None

    def setTokens(self):
        with open("test.txt", encoding='utf-8') as f:
            buffer = ""
            lastToken = ""
            for line in f:
                for char in line.rstrip():
                    if char == " " or char == "\n" and buffer == "":
                        continue

                    buffer += char

                    if self.getNameToken(buffer) is None:
                        if buffer == "\n":
                            buffer = ""
                            continue

                        tmp = {}
                        tmp[self.getNameToken(buffer[:len(buffer) - 1])] = buffer[:len(buffer) - 1]
                        self.tokensList.append(tmp)
                        buffer = buffer[len(buffer) - 1:]

    def getTokens(self):
        return self.tokensList



