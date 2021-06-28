import re


class Lexer(object):
    token = {"ЕСЛИ": "^if$", "ИНАЧЕ": "^else$", "ПОКА": "^while$", "ОПЕРАЦИЯ": "^[-+*/]$", "ЛОГИЧЕСКАЯ_ОПЕРАЦИЯ": r"^==|>|>=|<|<=|!=$",
              "ЛЕВАЯ_СКОБКА": "[(]", "ПРАВАЯ_СКОБКА": "[)]", 'ТОЧКА': r'\.', "ОКОНЧАНИЕ": "^;$", "ЛЕВАЯ_ФИГУРНАЯ": "^[{]$",
             'СВЯЗНЫЙ_СПИСОК': r'LinkedList', "ПРАВАЯ_ФИГУРНАЯ": "^[}]$", "ОПЕРАЦИЯ_ПРИСВАИВАНИЯ": "^=$",
              "КОНЕЦ": "^;$", "ЧИСЛО": r"^0|([1-9][0-9]*)$", "СТРОКА": r"'[^']*'", "ПЕРЕМЕННАЯ": "^[a-zA-Z0-9_]+$", "НЕ_ОПРЕДЕЛЕНО": r".*[^.]*"}

    def __init__(self):
        self.list_tokens = []

    def __set_token(self, item):
        for key in self.token.keys():
            if re.fullmatch(self.token[key], item):
                return key

    def get_term(self, file):
        with open(file) as file_handler:
            buffer = ''
            last_token = ''
            for line in file_handler:
                for char in line:
                    if not len(buffer) and char == "'":
                        buffer += char
                        continue
                    elif len(buffer) and not buffer.count("'") == 2:
                        if buffer[0] == "'":
                            buffer += char
                            continue

                    if last_token == 'ТОЧКА':
                        if not char == '(':
                            buffer += char
                            continue
                        else:
                            self.list_tokens.append({'МЕТОД': buffer})
                            buffer = ''

                    last_token = self.__set_token(buffer)
                    buffer += char
                    token = self.__set_token(buffer)

                    if token == "НЕ_ОПРЕДЕЛЕНО":
                        if len(buffer) and not last_token == "НЕ_ОПРЕДЕЛЕНО":
                            self.list_tokens.append({last_token: buffer[:-1]})
                        if not (buffer[-1] == ' ' or buffer[-1] == '\n'):
                            buffer = buffer[-1]
                        else:
                            buffer = ''

            token = self.__set_token(buffer)
            if not token == "НЕ_ОПРЕДЕЛЕНО":
                self.list_tokens.append({token: buffer[0]})
