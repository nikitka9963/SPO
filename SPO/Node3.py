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
            str_end += f'{child}' +"\n"
        return f'{self.name}\n{str_end}'
