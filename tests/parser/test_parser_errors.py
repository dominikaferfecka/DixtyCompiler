from parser.parser import Parser, Filter
from lexer.source import SourceString
import sys
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    IfStatement,
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
    SelectTerm
)


from parser.errors import (
    SemicolonMissing,
    MissingExpectedToken,
    InvalidFunctionDefinition,
    InvalidWhileLoop,
    InvalidForLoop,
    InvalidIfStatement,
    InvalidElseStatement,
    InvalidElseIfStatement,
    InvalidReturnStatement,
    InvalidAssignmentStatement
)

import pytest

def test_semicolon_assign():
    with pytest.raises(SemicolonMissing):
        source = SourceString("a = 1")
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()


def test_semicolon_function_call():
    with pytest.raises(SemicolonMissing):
        source = SourceString("a()")
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()


def test_semicolon_function_call():
    with pytest.raises(SemicolonMissing):
        source = SourceString("a()")
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()

def test_semicolon_return():
    with pytest.raises(SemicolonMissing):
        source = SourceString("return 1")
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()

def test_invalid_function_def():
    with pytest.raises(InvalidFunctionDefinition):
        source = SourceString("fun () {a;}")
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()

def test_invalid_function_def_bracket():
    with pytest.raises(InvalidFunctionDefinition):
        source = SourceString("fun a ) {a;}")
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()

