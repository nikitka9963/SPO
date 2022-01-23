import re
from lexer import Lexer
from linkedList import LinkedList
from funcs import getKey


class StackMachine:
    pr = {'(': 0, ')': 1, '=': 1, '==': 3, '!=': 3, '>': 4, '>=': 4, '<': 4, '<=': 4, '+': 5, '-': 5, '*': 6, '/': 6,
          'contains': 7, 'remove': 7, 'push': 7, 'get': 7}
    log_op = ['==', '!=', '>', '>=', '<', '<=']
    op = ['+', '-', '*', '/']
    list_com = ['contains', 'remove', 'push', 'get']

    def __init__(self):
        self.stack = []
        self.output = []
        self.buf = []
        self.bufel = []
        self.nl = 0
        self.index = -1
        self.variables = {}
        self.triads = {}

    def __init__(self, inp):
        self.stack = []
        self.input = inp
        self.output = []
        self.buf = []
        self.bufel = []
        self.nl = 0
        self.index = -1
        self.variables = {}
        self.triads = {}

    @staticmethod
    def b_log_op(a, b, op):
        if op == '>':
            return a > b
        elif op == '<':
            return a < b
        elif op == '>=':
            return a >= b
        elif op == '<=':
            return a <= b
        elif op == '==':
            return a == b
        elif op == '!=':
            return a != b

    @staticmethod
    def b_op(a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b

    @staticmethod
    def methodList(a, b, op):
        if op == 'push':
            a.push(b)
        elif op == 'remove':
            a.remove(b)
        elif op == 'get':
            a.get(b)
        elif op == 'contains':
            a.contains(b)

    def assign(self, a, b):
        if re.fullmatch(r"0|([1-9][0-9]*)", str(b)):
            self.variables[a] = int(b)
        elif b == 'LinkedList':
            self.variables[a] = LinkedList()
        else:
            self.variables[a] = b

    def abs(self, item):
        if 'while_expr' in item.name:
            self.buf.append({self.nl: len(self.output)})

        if item.name not in Lexer.token and not item.name == 'МЕТОД':
            for i in item.children:
                self.abs(i)

            self.stack.reverse()
            for y in self.stack:
                if not y == '(':
                    self.output.append(y)

            self.stack = []

        else:
            if item.name == 'ИНАЧЕ':
                self.bufel.append(self.nl)
                # self.output.append('\t')

            if item.name == 'ПРАВАЯ_ФИГУРНАЯ':
                self.nl -= 1
                if '\n' in self.output:
                    self.output.reverse()
                    self.output.remove("\n")
                    self.output.reverse()

                # if len(self.buf):
                #     if self.nl in list(self.buf[-1].keys()):
                #         self.output.append('!' + str(self.buf[-1][self.nl]))
                #         self.buf.pop(-1)

            if item.name == 'ЛЕВАЯ_ФИГУРНАЯ':
                self.nl += 1
                if self.nl > 0:
                    self.output.append('\n')

           # if len(self.bufel) and not item.name == 'ИНАЧЕ':
           #     if self.nl == self.bufel[-1]:
           #         self.output.reverse()
           #         self.output[self.output.index('\t')] =\
           #             '!' + str(len(self.output))
           #         self.output.reverse()
           #         self.bufel.pop(-1)

            if item.name in ['ПЕРЕМЕННАЯ', 'ЧИСЛО', 'ЧИСЛО', 'СВЯЗНЫЙ_СПИСОК']:
                self.output.append(str(item.value))

            else:
                if not item.value == '':
                    k = 0
                    for i in range(len(self.stack) - 1, -1, -1):
                        k += 1
                        if item.value == ')':
                            if not self.stack[i] == '(':
                                self.output.append(self.stack[i])
                            else:
                                break
                        elif self.pr[item.value] <= self.pr[self.stack[i]] \
                                and not item.value == '(':
                            self.output.append(self.stack[i])
                        else:
                            break

                    for j in range(1, k):
                        self.stack.pop(-j)

                    if not item.value == ')':
                        self.stack.append(item.value)

    def start(self):
        for item in self.input:
            self.abs(item)
            self.stack = []
        print("\ntest\n")
        print(self.output)
        self.optTriad()
        self.convToPol()
        self.compilation()
        print(self.variables)

    def compilation(self):
        k = 0
        self.stack = []

        while k < len(self.output):
            if not self.output[k] in list(self.pr.keys()):
                if not (str(type(self.output[k])) == "<class 'int'>" or
                        list(self.output[k])[0] == '!'):
                    self.stack.append(self.output[k])
                    k += 1

                elif len(self.stack):
                    if not self.stack[-1] and\
                            not list(str(self.output[k]))[0] == '!':
                        if not self.stack[-1]:
                            if (self.output[k]) < len(self.output):
                                if isinstance(self.output[self.output[k]],
                                              int):
                                    k = int(self.output[k] + 1)
                                    self.stack.pop(-1)
                                    continue
                                elif list(str(self.output[self.output[k]]))[0]\
                                        == '!':
                                    k = int(self.output[k] + 1)
                                    self.stack.pop(-1)
                                    continue
                                else:
                                    k = int(self.output[k])
                                    self.stack.pop(-1)
                                    continue
                            else:
                                k = int(self.output[k] + 1)
                                self.stack.pop(-1)
                                continue

                    elif list(str(self.output[k]))[0] == '!':
                        k = int(self.output[k])
                        continue

                    else:
                        self.stack.pop(-1)

                elif list(str(self.output[k]))[0] == '!':
                    k = int(str(self.output[k])[1:])
                    continue

                else:
                    k += 1

            else:
                b = self.stack.pop(-1)
                a = self.stack.pop(-1)
                op = self.output[k]
                k += 1
                if op == '=':
                    self.assign(a, b)

                # elif op in self.log_op:
                #     self.stack.append(self.b_log_op(self.variables[a],
                #                                       self.variables[b], op))

                elif op in self.op:
                    if not re.fullmatch(r"0|([1-9][0-9]*)", a):
                        a = self.variables[a]
                    else:
                        a = int(a)
                    if not re.fullmatch(r"0|([1-9][0-9]*)", b):
                        b = int(self.variables[b])
                    else:
                        b = int(b)
                    self.stack.append(self.b_op(a, b, op))

                elif op in self.list_com:
                    self.stack.append(self.methodList(self.variables[a], b, op))

    def setTriad(self):
        stack = []
        i = 1

        for el in self.output:
            tmp = []

            if el in self.pr.keys():
                stack.append(el)
                for _ in range(3):
                    tmp.append(stack.pop())

                tmp = tmp[::-1]
                stack.append("^" + str(i))
                self.triads[i] = tmp
                i += 1
            else:
                stack.append(el)

    def printTriad(self, lst=[]):
        print("Триады:\n")
        if len(lst):
            for key, value in lst.items():
                print(f"{key}: {value}", end="\n")
        else:
            for key, value in self.triads.items():
                print(f"{key}: {value}", end="\n")

        print(end="\n")

    def toLst(self):
        res = []

        for key, value in self.triads.items():
            tmp1 = []
            tmp1.append(key)
            for el in value:
                tmp1.append(el)

            res.append(tmp1)

        return res

    def optTriad(self):
        self.setTriad()
        self.printTriad()
        res = {}

        lst = self.toLst()
        self.triads = {}
        # Убрать ненужные присваивания
        for i in range(len(lst)):
            flag = False
            for j in range(i + 1, len(lst)):
                if lst[i][1] == lst[j][1] and lst[i][3] == lst[j][3]:
                    for k in range(i, j):
                        if lst[k][1] != lst[i][1] and lst[k][3] != "=" or "^"  in lst[k][2]:
                            self.triads[i + 1] = lst[i][1:]
                            flag = True
                            break
                    if not flag:
                        if i + 1 in self.triads and lst[j][3] == "=" and lst[j][1] == list(self.triads[i+1])[0]:
                            # if list(self.triads.get(i + 1))[2] != 'push':
                            self.triads.pop(i + 1)
                        self.triads[j + 1] = lst[j][1:]
                        break
                else:
                    self.triads[i + 1] = lst[i][1:]

            if i == len(lst) - 1:
                self.triads[i + 1] = lst[i][1:]

        print("\nTriads1")
        self.printTriad()

        lst = self.toLst()
        self.triads = {}
        flag = False

        #Предвычислить константные выражения и уьрать содержащие их триады
        for el in lst:
            if flag:
                flag = False
                continue

            if el[1].isdigit() and el[2].isdigit():
                for j in range(0, len(lst)):
                    if lst[j][2] == f"^{el[0]}":
                        lst[j][2] = str(self.b_op(int(el[1]), int(el[2]), el[3]))
                        self.triads[lst[j][0]] = lst[j][1:]
                        flag = True

            elif el[0] not in res:
                self.triads[el[0]] = el[1:]

        self.printTriad()

        tmp = self.triads
        self.triads = {}
        ind = list(tmp.keys())
        ind1 = ind.copy()

        #Убрать ненужные переменные
        for j in range(len(ind)):
            flag = True
            if list(tmp[ind[j]])[1].isdigit():
                for i in range(j + 1, len(tmp), 1):
                    if list(tmp[ind[j]])[0] == list(tmp[ind[i]])[0]:
                        flag = False
                        break
                if not flag:
                    self.triads[ind[j]] = list(tmp[ind[j]])
            else:
                self.triads[ind[j]] = list(tmp[ind[j]])

        self.printTriad()
    # 'a', '25', '=', 'b', 'a', '10', '-', '=', 'c', 'b', '2', '-', '=',
    def convToPol(self):
        lst = self.toLst()
        res = []
        flag = False

        for i in range(len(lst)):
            if flag:
                flag = False
                continue

            if i == len(lst) - 1:
                break

            if "^" in lst[i + 1][2]:
                res.append(lst[i + 1][1])
                res.append(lst[i][1])
                res.append(lst[i][2])
                res.append(lst[i][3])
                res.append(lst[i + 1][3])
                flag = True
            else:
                for el in lst[i][1:]:
                    res.append(el)

        print(res)
        self.output = res

        self.compilation()
        print(self.variables)










