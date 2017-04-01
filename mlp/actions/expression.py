import operator
from collections import deque
from .new_action import Property


class ExpressionError(Exception):
    pass


class Const(Property):

    def __init__(self, v):
        self.v = v

    def get(self, action):
        return self.v


class Oper(Property):

    def __init__(self, oper, left, right):
        self.oper = oper
        self.left = left
        self.right = right

    def get(self, action):
        return self.oper(self.left.get(action), self.right.get(action))


class Expression:

    OPERATORS = {
        '*': (operator.mul, 3),
        '+': (operator.add, 2),
        '-': (operator.sub, 2),
        '==': (operator.eq, 1),
        '!=': (operator.ne, 1),
    }

    UTILITY = {'+', '-', '*', '==', '!=', '(', ')'}

    def __init__(self, expression):
        self.expression = self.make_tree(self.inf_2_post(expression))

    def get(self, action):
        return self.expression.get(action)

    def inf_2_post(self, expression):
        OPERATORS = self.OPERATORS
        UTILITY = self.UTILITY

        stack = deque()
        output = deque()
        for token in expression:
            if token in UTILITY:
                if token == '(':
                    stack.append(token)
                elif token == ')':
                    for i in range(1000):
                        if stack[-1] == '(':
                            break
                        output.append(stack.pop())
                    else:
                        raise ExpressionError()
                    stack.pop()
                else:
                    while stack and stack[-1] in OPERATORS and OPERATORS[token][-1] <= OPERATORS[stack[-1]][-1]:
                        output.append(stack.pop())
                    stack.append(token)
            else:
                output.append(token)
        while stack:
            output.append(stack.pop())
        return list(output)

    def make_tree(self, post_tokens):
        OPERATORS = self.OPERATORS
        UTILITY = self.UTILITY

        stack = deque()

        for token in post_tokens:
            if token not in UTILITY:
                if isinstance(token, Property):
                    stack.append(token)
                else:
                    stack.append(Const(token))
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(Oper(OPERATORS[token][0], left, right))
        return stack.pop()

if __name__ == '__main__':
    a = [3, '+', 4, '*', '(', 2, '-', 1, ')']
    q = Expression(None)
    z = q.inf_2_post(a)
    print(q.make_tree(z).get(None))
