class LinkedList:
    def __init__(self):
        self.head = None

    def push(self, val):
        if self.head is None:
            self.head = Item(val)
            return

        lastItem = self.head

        while lastItem.nextValue:
            lastItem = lastItem.nextValue

        lastItem.nextValue = Item(val)

    def get(self, ind):
        lastItem = self.head
        boxIndex = 0

        while boxIndex <= ind:
            if boxIndex == ind:
                return lastItem.cat

            boxIndex += 1
            lastItem = lastItem.nextValue

    def remove(self, val):
        global lastItem
        headItem = self.head

        if headItem is not None:
            if headItem.value == val:
                self.head = headItem.nextValue
                return

        while headItem is not None:
            if headItem.value == val:
                break

            lastItem = headItem
            headItem = headItem.nextValue

        if headItem is None:
            return

        lastItem.nextValue = headItem.nextValue

    def __repr__(self):
        current = self.head
        str = '[ '

        while current is not None:
            str += f'{current.value},'
            current = current.nextValue

        str += ']'

        return str

    def contains(self, value):
        lastItem = self.head

        while lastItem:
            if value == lastItem.value:
                return True
            else:
                lastItem = lastItem.nextValue
                
        return False


class Item:
    def __init__(self, value=None):
        self.value = value
        self.nextValue = None
