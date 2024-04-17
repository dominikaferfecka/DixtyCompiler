class Node:
    def __init__(self):
        pass

class Program(Node):
    def __init__(self, statements):
        super().__init__()
        self._statements = statements
        # functions ?

class ForStatement(Node):
    def __init__(self, identifier, expression, block, position):
        super().__init__()
        self._identifier = identifier
        self._expression = expression
        self._block = block
        self._position = position


class WhileStatement(Node):
    def __init__(self):
        super().__init__()


class FunStatement(Node):
    def __init__(self):
        super().__init__()


class ReturnStatement(Node):
    def __init__(self):
        super().__init__()


class IfStatement(Node):
    def __init__(self):
        super().__init__()