
from lexer.filter import Filter
from lexer.lexer import Lexer
from lexer.tokens import Token, TokenType
import sys
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    ReturnStatement,
    IfStatement,
    ElseIfStatement,
    ElseStatement,
    OrTerm,
    AndTerm,
    NotTerm,
    LessTerm,
    MoreTerm,
    EqualsTerm,
    LessOrEqualTerm,
    MoreOrEqualTerm,
    AddTerm,
    SubTerm,
    MultTerm,
    DivTerm,
    SignedFactor,
    Number,
    ObjectAccess,
    Item,
    Identifier,
    Assignment,
    String,
    Bool,
    List,
    Pair,
    Dict,
    Block,
    FunCall,
    SelectTerm
)

class SemicolonMissing(Exception):
    def __init__(self, _, __, position):
        super().__init__(f'Missing semicolon after end of statement at position: {position}')
        self.position = position


class MissingExpectedStatement(Exception):
    def __init__(self, expected, received, position, extra_message=""):
        super().__init__(f'{extra_message}Expected token [{expected}], received token [{received}] at {position}')
        self.position = position
        self.expected = expected
        self.received = received

class InvalidFunctionDefinition(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)

class InvalidWhileLoop(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)

class InvalidForLoop(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)

class InvalidIfStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidElseIfStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidElseStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)
    

class InvalidReturnStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidAssignmentStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class FunctionAlreadyExists(Exception):
    def __init__(self, name, position):
        super().__init__(f'Function with name {name} is already defined. Tried to define again at position: {position}')
        self.position = position
        self.name = name


class DictInvalidElement(Exception):
    def __init__(self, element, position):
        super().__init__(f'Elements in Dict must be Pair type. Object with invalid type {element} at {position}')
        self.position = position
        self.element = element
