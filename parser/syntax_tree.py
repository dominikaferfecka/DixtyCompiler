from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor, *args):
        pass    

class Program(Node):
    def __init__(self, statements, functions):
        super().__init__()
        self._statements = statements
        self._functions = functions
    
    def accept(self, visitor, *args):
        visitor.visit_program(self, *args)

class ForStatement(Node):
    def __init__(self, identifier, expression, block, position):
        super().__init__()
        self._identifier = identifier
        self._expression = expression
        self._block = block
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_for_statement(self, *args)


class WhileStatement(Node):
    def __init__(self, expression, block, position):
        self._expression = expression
        self._block = block
        self._position = position

    def accept(self, visitor, *args):
        visitor.visit_while_statement(self, *args)


class FunStatement(Node):
    def __init__(self, name, parameters, block, position):
        super().__init__()
        self._name = name
        self._parameters = parameters
        self._block = block
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_fun_def_statement(self, *args)
        


class ReturnStatement(Node):
    def __init__(self, expression, position):
        super().__init__()
        self._expression = expression
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_return_statement(self, *args)


class IfStatement(Node):
    def __init__(self, expression, block, else_if_statement, else_statement, position):
        super().__init__()
        self._expression = expression
        self._block = block
        self._else_if_statement = else_if_statement
        self._else_statement = else_statement
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_if_statement(self, *args)


class ElseIfStatement(Node):
    def __init__(self, expression, block, position):
        super().__init__()
        self._expression = expression
        self._block = block
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_else_if_statement(self, *args)


class ElseStatement(Node):
    def __init__(self, block, position):
        super().__init__()
        self._block = block
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_else_statement(self, *args)


class OrTerm(Node):
    def __init__(self, left_and_term, position, right_and_term):
        super().__init__()
        self._left_and_term = left_and_term
        self._position = position
        self._right_and_term = right_and_term
    
    def accept(self, visitor, *args):
        visitor.visit_or_term(self, *args)


class AndTerm(Node):
    def __init__(self, left_not_term, position, right_not_term):
        super().__init__()
        self._left_not_term = left_not_term
        self._position = position
        self._right_not_term = right_not_term
    
    def accept(self, visitor, *args):
        visitor.visit_and_term(self, *args)


class NotTerm(Node):
    def __init__(self, comparison_term, position):
        super().__init__()
        self._comparison_term = comparison_term
        self._position = position

    def accept(self, visitor, *args):
        visitor.visit_not_term(self, *args)

class ComparisonTerm(Node):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__()
        self._left_additive_term = left_additive_term
        self._position = position
        self._right_additive_term = right_additive_term

class EqualsTerm(ComparisonTerm):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__(left_additive_term, position, right_additive_term)

    def accept(self, visitor, *args):
        visitor.visit_equal_term(self, *args)
    

class NotEqualsTerm(ComparisonTerm):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__(left_additive_term, position, right_additive_term)

    def accept(self, visitor, *args):
        visitor.visit_not_equal_term(self, *args)


class LessTerm(ComparisonTerm):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__(left_additive_term, position, right_additive_term)
    
    def accept(self, visitor, *args):
        visitor.visit_less_term(self, *args)

class MoreTerm(ComparisonTerm):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__(left_additive_term, position, right_additive_term)

    def accept(self, visitor, *args):
        visitor.visit_more_term(self, *args)

class LessOrEqualTerm(ComparisonTerm):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__(left_additive_term, position, right_additive_term)

    def accept(self, visitor, *args):
        visitor.visit_less_or_equal_term(self, *args)

class MoreOrEqualTerm(ComparisonTerm):
    def __init__(self, left_additive_term, position, right_additive_term):
        super().__init__(left_additive_term, position, right_additive_term)
    
    def accept(self, visitor, *args):
        visitor.visit_more_or_equal_term(self, *args)

class AddTerm(Node):
    def __init__(self, left_mult_term, position, right_mult_term):
        super().__init__()
        self._left_mult_term = left_mult_term
        self._position = position
        self._right_mult_term = right_mult_term
    
    def accept(self, visitor, *args):
        visitor.visit_add_term(self, *args)


class SubTerm(Node):
    def __init__(self, left_mult_term, position, right_mult_term):
        super().__init__()
        self._left_mult_term = left_mult_term
        self._position = position
        self._right_mult_term = right_mult_term

    def accept(self, visitor, *args):
        visitor.visit_sub_term(self, *args)

class MultTerm(Node):
    def __init__(self, left_signed_factor, position, right_signed_factor):
        super().__init__()
        self._left_signed_factor = left_signed_factor
        self._position = position
        self._right_signed_factor = right_signed_factor

    def accept(self, visitor, *args):
        visitor.visit_mult_term(self, *args)


class DivTerm(Node):
    def __init__(self, left_signed_factor, position, right_signed_factor):
        super().__init__()
        self._left_signed_factor = left_signed_factor
        self._position = position
        self._right_signed_factor = right_signed_factor

    def accept(self, visitor, *args):
        visitor.visit_div_term(self, *args)


class SignedFactor(Node):
    def __init__(self, factor, position):
        super().__init__()
        self._factor = factor
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_signed_factor(self, *args)

class Number(Node):
    def __init__(self, value, position):
        super().__init__()
        self._value = value
        self._position = position

    def accept(self, visitor, *args):
        visitor.visit_number(self, *args)

class String(Node):
    def __init__(self, value, position):
        super().__init__()
        self._value = value
        self._position = position

    def accept(self, visitor, *args):
        visitor.visit_string(self, *args)


class Bool(Node):
    def __init__(self, value, position):
        super().__init__()
        self._value = value
        self._position = position

    def accept(self, visitor, *args):
        visitor.visit_bool(self, *args)


class List(Node):
    def __init__(self, values, position):
        super().__init__()
        self._values = values
        self._position = position

    def accept(self, visitor, *args):
        visitor.visit_list(self, *args)


class Pair(Node):
    def __init__(self, first, second, position):
        super().__init__()
        self._first = first
        self._second = second
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_pair(self, *args)


class Dict(Node):
    def __init__(self, values, position):
        super().__init__()
        self._values = values
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_dict(self, *args)


class ObjectAccess(Node):
    def __init__(self, left_item, position, right_item):
        super().__init__()
        self._left_item = left_item
        self._right_item = right_item
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_object_access(self, *args)


class Item(Node):
    def __init__(self, left, position):
        super().__init__()
        self._left = left
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_item_statement(self, *args)


class IndexAccess(Item):
    def __init__(self, left, position, index_object):
        super().__init__(left, position)
        self._index_object = index_object
    
    def accept(self, visitor, *args):
        visitor.visit_index_access(self, *args)


class FunCall(Item):
    def __init__(self, left, position, arguments):
        super().__init__(left, position)
        self._arguments = arguments
    
    def accept(self, visitor, *args):
        visitor.visit_fun_call(self, *args)


class Identifier(Node):
    def __init__(self, name, position):
        super().__init__()
        self._name = name
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_identifier(self, *args)


class Assignment(Node):
    def __init__(self, object_access, expression, position):
        super().__init__()
        self._object_access = object_access
        self._expression = expression
        self._position = position

    def accept(self, visitor, *args):
        visitor.visit_assign_statement(self, *args)


class Block(Node):
    def __init__(self, statements, position):
        super().__init__()
        self._statements = statements
        self._position = position
    
    def accept(self, visitor, *args):
        visitor.visit_block(self, *args)


class SelectTerm(Node):
    def __init__(self, select_expression, from_expression, position, where_expression = None, order_by_expression = None, asc_desc = "ASC"):
        super().__init__()
        self._select_expression = select_expression
        self._from_expression = from_expression
        self._position = position
        self._where_expression = where_expression
        self._order_by_expression = order_by_expression
        self._asc_desc = asc_desc
    
    def accept(self, visitor, *args):
        visitor.visit_select_term(self, *args)