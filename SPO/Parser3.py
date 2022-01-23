from Node import Node

class Parser():
    def __init__(self, lexer):
        self.tokens = ["VAR", "STRING", "ASSIGN", "CONCAT", "OR", "END", "COND_OCC_L",
                       "COND_OCC_R", "REPETITION_L", "REPETITION_R", "GROUPING_L", "GROUPING_R"]

        self.height = 1
        self.count = 0
        self.counter = 0
        self.start = lexer
        self.LB = 0
        self.flag = False
        self.type = ""

    def Tree(self):
        Tree = Node('l')

        while self.count < len(self.start) - 1:
            expr = self.expr()

            if expr is not None:
                Tree.children.append(expr)
            else:
                break

        print(Tree.children)

    def expr(self):
        expr = Node('New expr', height=self.height)
        self.height += 1

        token = list(self.start[self.count].keys())[0]
        nextToken = list(self.start[self.count + 1].keys())[0]

        assign_expr = self.assign_expr()
        expr.children.append(assign_expr)

        return expr

    def assign_expr(self):
        ind = ""
        for i in range(self.height + 1, self.height + 5, 1):
            ind += str(i) + ", "

        expr = Node(f"{self.height} oper -> {ind}", ind, self.height)
        self.height += 1
        add = str(self.height) + " " + list(self.start[self.count].keys())[0] + " = " + list(self.start[self.count].values())[0]
        expr.children.append(add)
        self.height += 1
        self.count += 1

        add = str(self.height) + " " + list(self.start[self.count].keys())[0] + " = " + list(self.start[self.count].values())[0]
        expr.children.append(add)
        self.height += 1
        self.count += 1

        if list(self.start[self.count + 1].keys())[0] != "END":
            self.type = "NEW"
            end = self.height
            ind = self.countTok()

            add = str(end) + " expr = " + ind
            ind += str(self.count)
            expr.children.append(add)
            self.count = self.counter
            self.height = end + 1
        else:
            add = str(self.height) + " " + list(self.start[self.count].keys())[0] + " = " + list(self.start[self.count].values())[0]
            expr.children.append(add)
            self.height += 1
            self.count += 1

        add = str(self.height) + " " + list(self.start[self.count].keys())[0] + " = " + list(self.start[self.count].values())[0]
        expr.children.append(add)
        self.height += 1
        self.count += 1

        if self.type == "NEW":
            if_expr = self.add_expr(ind)
            expr.children.append(if_expr)
        else:
            self.height -= 1

        return expr

    def countTok(self):
        self.counter = self.count
        self.height += 2
        ind = ""

        while list(self.start[self.counter].keys())[0] != "END":
            if list(self.start[self.counter].values())[0] == "{" or \
                    list(self.start[self.counter].values())[0] == "[" or \
                    list(self.start[self.counter].values())[0] == "(":

                ind += str(self.height) + ", "

                while(list(self.start[self.counter].values())[0] != "}" and \
                        list(self.start[self.counter].values())[0] != "]" and \
                        list(self.start[self.counter].values())[0] != ")"):
                    self.counter += 1

                self.height += 1
                self.counter += 1
            else:
                ind += str(self.height) + ", "
                self.counter += 1
                self.height += 1

        return ind

    def add_expr(self, ind):
        lnk = ind.split(", ")
        i = int("".join(lnk[-1:]))
        lnk = lnk[:-1]
        counter = int("".join(lnk[-1:])) + 1
        counterR = ""
        add = ""
        ind = ""
        indG = ""
        self.type = ""
        remR = 0
        remC = 0
        remG = 0
        countL = self.height

        lnk = self.convToIn(lnk)

        expr = Node('\nadd_expr', height=self.height)

        for el in lnk:
            if list(self.start[i].values())[0] == "{":
                remR = i
                self.type += "one"

                while list(self.start[i].values())[0] != "}":
                    i += 1
                    ind += str(counter) + ", "
                    counter += 1

                ind += str(counter) + ", "
                counterR = ind
                add = str(el) + " expr = " + ind
                expr.children.append(add)
            elif list(self.start[i].values())[0] == "[":
                remC = i
                ind = ""
                self.type += " many"

                while list(self.start[i].values())[0] != "]":
                    counter += 1
                    i += 1
                    ind += str(counter) + ", "

                counter += 1
                ind += str(counter) + ", "
                add = str(el) + " expr = " + ind
                expr.children.append(add)
            elif list(self.start[i].values())[0] == "(":
                remG = i
                self.type += " group"

                while list(self.start[i].values())[0] != ")":
                    counter += 1
                    i += 1
                    indG += str(counter) + ", "

                counter += 1
                indG += str(counter) + ", "
                add = str(el) + " expr = " + indG
                expr.children.append(add)
            else:
                add = str(el) + " " + list(self.start[i].keys())[0] + " = " + list(self.start[i].values())[0]
                expr.children.append(add)
                countL += 1

            i += 1

        self.height = countL - 1

        if "one" in self.type:
            # one_expr = self.many_expr(remR, counterR)
            one_expr = self.staples_expr(remR, counterR, "{}_expr")
            expr.children.append(one_expr)

        if "many" in self.type:
            # more_expr = self.one_expr(remC, ind)
            more_expr = self.staples_expr(remC, ind, "[]_expr")
            expr.children.append(more_expr)

        if "group" in self.type:
            # more_expr = self.group_expr(remG, indG)
            group_expr = self.staples_expr(remG, indG, "()_expr")
            expr.children.append(group_expr)

        self.type = ""

        return expr

    def staples_expr(self, ind, count, text):
        expr = Node(f'\n{text}', height=self.height)
        count = self.convToIn(count.split(", ")[:-1])

        for el in count:
            add = str(el) + " " + list(self.start[ind].keys())[0] + " = " + list(self.start[ind].values())[0]
            expr.children.append(add)
            ind += 1

        self.height = int(count[-1])

        return expr

    def convToIn(self, lst):
        for el in lst:
            el = int(el)

        return lst







