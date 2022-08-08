

class Stack:

    def __init__(self):
        self.stack = []

    def push(self, obj):
        self.stack.append(obj)

    def pop(self):
        return self.stack.pop(-1)

    def head(self):
        return self.stack[-1]