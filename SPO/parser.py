class Parser:
    def __init__(self, lexer):
        self.height = 0
        self.i = 0
        self.start = lexer
        self.LB = 0

    def S(self):
        S = Node('S')
        while self.i < len(self.start) - 1:
            self.height = 1
            expr = self.expr()
            if expr is not None:
                S.children.append(expr)
            self.i += 1

        return S

    def expr(self):
        try:
            expr = Node('expr', height=self.height)
            self.height += 1

            token = list(self.start[self.i].keys())[0]

            if token == "ПЕРЕМЕННАЯ":
                try:
                    assign_expr = self.assign_expr()
                    expr.children.append(assign_expr)
                    self.height -= 1
                    return expr

                except BaseException:
                    expr.children.append(List(list(self.start[self.i].keys())[0], list(self.start[self.i].values())[0],
                                              self.height))
                    self.check_next('ТОЧКА')
                    self.i += 1
                    method = self.method()
                    expr.children.append(method)
                    return expr

            elif token == 'ПОКА':
                while_expr = self.while_expr()
                expr.children.append(while_expr)
                self.height -= 1
                return expr

            elif token == 'ЕСЛИ':
                if_expr = self.if_expr()
                expr.children.append(if_expr)
                self.height -= 1
                return expr

            else:
                return None
        except BaseException:
            raise BaseException

    def method(self):
        method = Node('method', height=self.height)
        self.height += 1
        self.check_next('МЕТОД')
        self.i += 1
        method.children.append(List(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                               height=self.height))
        self.height += 1
        self.check_next('ЛЕВАЯ_СКОБКА')
        self.i += 1
        method.children.append(List(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                                    height=self.height))
        math_expr = self.math_expr()
        method.children.append(math_expr)

        if not list(self.start[self.i].keys())[0] == 'ОКОНЧАНИЕ':
            raise BaseException

        return method

    def if_expr(self):
        height = self.height
        if_expr = Node('if_expr', height=self.height)
        self.height += 1
        start_height = self.height
        self.check_next('ЛЕВАЯ_СКОБКА')
        if_expr.children.append(List('ЛЕВАЯ_СКОБКА', '(', height=self.height))
        self.i += 2
        self.height += 1
        token = list(self.start[self.i].keys())[0]

        if token == 'ПЕРЕМЕННАЯ' or token == 'ЧИСЛО' or token == 'ЛЕВАЯ_СКОБКА':
            math_logic = self.math_logic(ht=[start_height])
            if_expr.children.append(math_logic)

            self.height = start_height
            self.check_next('ЛЕВАЯ_ФИГУРНАЯ')
            if_expr.children.append(Node('ЛЕВАЯ_ФИГУРНАЯ', height=start_height))
            self.i += 1
            num_L = 1
            while num_L:
                if list(self.start[self.i].keys())[0] == 'ПРАВАЯ_ФИГУРНАЯ':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'ЛЕВАЯ_ФИГУРНАЯ':
                    num_L += 1
                if num_L:
                    self.i += 1
                    self.height = start_height
                    self.height += 1
                    if list(self.start[self.i].keys())[0] == 'ЛЕВАЯ_ФИГУРНАЯ':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'ПРАВАЯ_ФИГУРНАЯ':
                        num_L -= 1
                        break
                    expr = self.expr()
                    if expr is not None:
                        if_expr.children.append(expr)

            if_expr.children.append(Node('ПРАВАЯ_ФИГУРНАЯ', height=start_height))

            if self.i < len(self.start) - 1:
                self.check_next('ИНАЧЕ')
                self.i += 1
                self.check_next('ЛЕВАЯ_ФИГУРНАЯ')
                self.height = height
                if_expr.children.append(Node('ИНАЧЕ', height=self.height))
                self.height += 1
                start_height = self.height
                if_expr.children.append(Node('ЛЕВАЯ_ФИГУРНАЯ', height=self.height))
                num_L = 1

                while num_L:

                    if list(self.start[self.i].keys())[0] == 'ПРАВАЯ_ФИГУРНАЯ':
                        num_L -= 1
                    if list(self.start[self.i].keys())[0] == 'ЛЕВАЯ_ФИГУРНАЯ':
                        num_L += 1
                    if num_L:
                        self.i += 1
                        self.height = start_height
                        self.height += 1
                        if list(self.start[self.i].keys())[0] == 'ЛЕВАЯ_ФИГУРНАЯ':
                            num_L += 1
                        if list(self.start[self.i].keys())[0] == 'ПРАВАЯ_ФИГУРНАЯ':
                            num_L -= 1
                            break
                        expr = self.expr()
                        if expr is not None:
                            if_expr.children.append(expr)

                if_expr.children.append(Node('ПРАВАЯ_ФИГУРНАЯ', height=start_height))
            return if_expr

    def while_expr(self):
        while_expr = Node('while_expr', height=self.height)
        self.height += 1
        start_height = self.height
        self.check_next('ЛЕВАЯ_СКОБКА')
        while_expr.children.append(List('ЛЕВАЯ_СКОБКА', '(', height=self.height))
        self.i += 2
        self.height += 1
        token = list(self.start[self.i].keys())[0]
        if token == 'ПЕРЕМЕННАЯ' or token == 'ЧИСЛО' or token == 'ЛЕВАЯ_СКОБКА':
            math_logic = self.math_logic(ht=[start_height])
            while_expr.children.append(math_logic)

            self.height = start_height
            self.check_next('ЛЕВАЯ_ФИГУРНАЯ')
            self.i += 1
            while_expr.children.append(Node('ЛЕВАЯ_ФИГУРНАЯ', height=self.height))
            num_L = 1

            while num_L:
                if list(self.start[self.i].keys())[0] == 'ПРАВАЯ_ФИГУРНАЯ':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'ЛЕВАЯ_ФИГУРНАЯ':
                    num_L += 1

                if num_L:
                    self.i += 1
                    self.height = start_height
                    self.height += 1
                    if list(self.start[self.i].keys())[0] == 'ЛЕВАЯ_ФИГУРНАЯ':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'ПРАВАЯ_ФИГУРНАЯ':
                        num_L -= 1
                        break
                    expr = self.expr()
                    if expr is not None:
                        while_expr.children.append(expr)

            while_expr.children.append(Node('ПРАВАЯ_ФИГУРНАЯ', height=start_height))
            return while_expr
        else:
            raise BaseException

    def math_logic(self, ht=[]):
        token = list(self.start[self.i].keys())[0]

        if not token == 'ПРАВАЯ_СКОБКА' or not token == 'ЛОГИЧЕСКАЯ_ОПЕРАЦИЯ' \
                or not token == 'ОПЕРАЦИЯ':
            math_logic = Node('math_logic', height=self.height)
        else:
            math_logic = ''
        self.height += 1

        if token == 'ЛЕВАЯ_СКОБКА':
            ht.append(self.height)
            LBreaket = self.LBreaket()
            math_logic.children.append(LBreaket)

        elif token == 'ПРАВАЯ_СКОБКА':
            self.height = ht.pop(-1)
            math_logic = Node('ПРАВАЯ_СКОБКА',  height=self.height)

        elif token == 'ЧИСЛО':
            math_logic.children.append(List(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'ЛОГИЧЕСКАЯ_ОПЕРАЦИЯ':
                    self.i += 1
                    math_logic.children.append(List(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

                elif list(self.start[self.i + 1].keys())[0] == 'ОПЕРАЦИЯ':
                    self.i += 1
                    math_logic.children.append(List(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

        elif token == 'ПЕРЕМЕННАЯ':
            math_logic.children.append(List(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'ЛОГИЧЕСКАЯ_ОПЕРАЦИЯ':
                    self.i += 1
                    math_logic.children.append(List(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

                elif list(self.start[self.i + 1].keys())[0] == 'ОПЕРАЦИЯ':
                    self.i += 1
                    math_logic.children.append(List(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))

        elif token == 'ЛОГИЧЕСКАЯ_ОПЕРАЦИЯ':
            self.height -= 1
            math_logic = Node('ЛОГИЧЕСКАЯ_ОПЕРАЦИЯ' +
                              list(self.start[self.i].values())[0],
                              height=self.height)

        elif token == 'ОПЕРАЦИЯ':
            self.height -= 1
            math_logic = Node('ОПЕРАЦИЯ' + list(self.start[self.i].values())[0],
                              height=self.height)

        elif not token == 'ОКОНЧАНИЕ':
            raise BaseException

        if len(ht):
            self.i += 1
            me = self.math_logic(ht)
            math_logic.children.append(me)

        return math_logic

    def check_next(self, values):
        token = list(self.start[self.i + 1].keys())[0]
        if not token == values:
            raise BaseException

    def assign_expr(self):
        assign_expr = Node('НАЗНАЧИТЬ_ВЫРАЖЕНИЕ', '=', self.height)
        self.check_next("ОПЕРАЦИЯ_ПРИСВАИВАНИЯ")
        self.height += 1
        assign_expr.children.append(List(list(self.start[self.i].keys())[0],
                                         list(self.start[self.i].
                                              values())[0], self.height))
        self.i += 1
        assign_expr.children.append(List(list(self.start[self.i].keys())[0],
                                         list(self.start[self.i].
                                              values())[0], self.height))
        self.height -= 1
        self.i += 1
        token = list(self.start[self.i].keys())[0]
        if token == 'СТРОКА':
            self.height += 1
            assign_expr.children.append(List('СТРОКА', list(self.start[self.i].
                                                         values())[0],
                                             self.height))
            self.check_next('ОКОНЧАНИЕ')
            self.i += 1

        elif token == 'ЧИСЛО' or token == 'ЛЕВАЯ_СКОБКА' or token == 'ПЕРЕМЕННАЯ':
            self.height += 1
            math_expr = self.math_expr()
            assign_expr.children.append(math_expr)

        elif token == 'СВЯЗНЫЙ_СПИСОК':
            self.height += 1
            assign_expr.children.append(List('СВЯЗНЫЙ_СПИСОК', list(self.start[self.i].values())[0], self.height))

        return assign_expr

    def math_expr(self, ht=[]):
        token = list(self.start[self.i].keys())[0]
        if not token == 'ПРАВАЯ_СКОБКА' or not token == 'ОПЕРАЦИЯ' or not token == 'ТОЧКА':
            math_expr = Node('math_expr', height=self.height)
        else:
            math_expr = ''
        self.height += 1

        if token == 'ЛЕВАЯ_СКОБКА':
            ht.append(self.height)
            LBreaket = self.LBreaket()
            math_expr.children.append(LBreaket)

        elif token == 'ПРАВАЯ_СКОБКА':
            self.LB -= 1
            self.height = ht.pop(-1)
            if self.LB < 0:
                raise BaseException
            math_expr = Node('ПРАВАЯ_СКОБКА', value=')', height=self.height)

        elif token == 'ЧИСЛО':
            math_expr.children.append(List(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'ОПЕРАЦИЯ':
                    self.i += 1
                    math_expr.children.append(List(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.height))

        elif token == 'ОПЕРАЦИЯ':
            self.height -= 1
            math_expr = Node('ОПЕРАЦИЯ' + list(self.start[self.i].values())[0],
                             height=self.height)

        elif token == 'ПЕРЕМЕННАЯ':
            math_expr.children.append(List(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'ОПЕРАЦИЯ':
                    self.i += 1
                    math_expr.children.append(List(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.height))

        elif token == 'ТОЧКА':
            math_expr = self.method()
            self.i -= 1
        elif not token == 'ОКОНЧАНИЕ':
            raise BaseException

        self.i += 1
        if not list(self.start[self.i].keys())[0] == 'ОКОНЧАНИЕ':
            me = self.math_expr(ht)
            math_expr.children.append(me)

        return math_expr

    def LBreaket(self):
        self.LB += 1
        LBreaket = List('ЛЕВАЯ_СКОБКА', '(', height=self.height)

        return LBreaket


class List:
    def __init__(self, name='', value='', height=0):
        self.name = name
        self.value = value
        self.height = height

    def __repr__(self):
        return f'{self.name} {self.value}\n'


class Node:
    def __init__(self, name='', value='', height=0):
        self.children = []
        self.name = name
        self.value = value
        self.height = height
        self.buffer = []

    def __repr__(self):
        str_end = ''
        for child in self.children:
            str_end += "\t" * child.height + f'{child}'
        return f'{self.name}\n{str_end}'
