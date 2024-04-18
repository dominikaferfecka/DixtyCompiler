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
    def __init__(self, expression, block, position):
        self._expression = expression
        self._block = block
        self._position = position


class FunStatement(Node):
    def __init__(self):
        super().__init__()


class ReturnStatement(Node):
    def __init__(self):
        super().__init__()


class IfStatement(Node):
    def __init__(self):
        super().__init__()


class OrTerm(Node):
    def __init__(self, left_and_term, position, right_and_term):
        super().__init__()
        self._left_and_term = left_and_term
        self._position = position
        self._right_and_term = right_and_term


class AndTerm(Node):
    def __init__(self, left_not_term, position, right_not_term):
        super().__init__()
        self._left_not_term = left_not_term
        self._position = position
        self._right_not_term = right_not_term


class NotTerm(Node):
    def __init__(self, comparison_term, position):
        super().__init__()
        self._comparision_term = comparison_term
        self._position = position



