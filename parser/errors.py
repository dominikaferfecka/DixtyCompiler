
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


class MissingExpectedToken(Exception):
    def __init__(self, expected, received, position, extra_message=""):
        super().__init__(f'{extra_message}Expected token [{expected}], received token [{received}] at {position}')
        self.position = position
        self.expected = expected
        self.received = received

class InvalidFunctionDefinition(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)

class InvalidWhileLoop(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)

class InvalidForLoop(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)

class InvalidIfStatement(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidElseIfStatement(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidElseStatement(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)
    

class InvalidReturnStatement(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidAssignmentStatement(MissingExpectedToken):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)