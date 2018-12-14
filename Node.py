class Node:
    def __init__(self, parent, content):
        self.parent = parent
        self.content = content
        self.son_list = []

    def add_son(self, son):
        self.son_list.append(son)