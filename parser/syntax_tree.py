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
    def __init__(self, name, parameters, block, position):
        super().__init__()
        self._name = name
        self._parameters = parameters
        self._block = block
        self._position = position


class ReturnStatement(Node):
    def __init__(self, expression, position):
        super().__init__()
        self._expression = expression
        self._position = position


class IfStatement(Node):
    def __init__(self, expression, block, else_if_statement, else_statement, position):
        super().__init__()
        self._expression = expression
        self._block = block
        self._else_if_statement = else_if_statement
        self._else_statement = else_statement
        self._position = position


class ElseIfStatement(Node):
    def __init__(self, expression, block, position):
        super().__init__()
        self._expression = expression
        self._block = block
        self._position = position


class ElseStatement(Node):
    def __init__(self, block, position):
        super().__init__()
        self._block = block
        self._position = position


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


class ComparisonTerm(Node):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__()
        self._left_additive_term = left_additive_term
        self._position = position
        self._right_additive_term = right_additive_term


class AdditiveTerm(Node):
    def __init__(self, left_mult_term, position, right_mult_term):
        super().__init__()
        self._left_mult_term = left_mult_term
        self._position = position
        self._right_mult_term = right_mult_term


class MultTerm(Node):
    def __init__(self, left_signed_factor, position, right_signed_factor):
        super().__init__()
        self._left_signed_factor = left_signed_factor
        self._position = position
        self._right_signed_factor = right_signed_factor


class SignedFactor(Node):
    def __init__(self, factor, position):
        super().__init__()
        self._factor = factor
        self._position = position


class Literal(Node):
    def __init__(self, factor, position):
        super().__init__()
        self._factor = factor
        self._position = position


class Number(Node):
    def __init__(self, value, position):
        super().__init__()
        self._value = value
        self._position = position


class String(Node):
    def __init__(self, value, position):
        super().__init__()
        self._value = value
        self._position = position


class Bool(Node):
    def __init__(self, value, position):
        super().__init__()
        self._value = value
        self._position = position


class List(Node):
    def __init__(self, values, position):
        super().__init__()
        self._values = values
        self._position = position


class Pair(Node):
    def __init__(self, first, second, position):
        super().__init__()
        self._first = first
        self._second = second
        self._position = position


class Dict(Node):
    def __init__(self, values, position):
        super().__init__()
        self._values = values
        self._position = position


class ObjectAccess(Node):
    def __init__(self, left_item, position, right_item):
        super().__init__()
        self._left_item = left_item
        self._right_item = right_item
        self._position = position


class Item(Node):
    def __init__(self, name, position): # expression, arguments?
        super().__init__()
        self._name = name
        self._position = position


class Identifier(Node):
    def __init__(self, name, position):
        super().__init__()
        self._name = name
        self._position = position


class Assignment(Node):
    def __init__(self, object_access, expression, position):
        super().__init__()
        self._object_access = object_access
        self._expression = expression
        self._position = position


class Block(Node):
    def __init__(self, statements, position):
        super().__init__()
        self._statements = statements
        self._position = position
