from parser.parser import Parser, Filter
from lexer.source import SourceString
from lexer.lexer import TokenType
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
    MissingExpectedStatement,
    InvalidFunctionDefinition,
    InvalidWhileLoop,
    InvalidForLoop,
    InvalidIfStatement,
    InvalidElseStatement,
    InvalidElseIfStatement,
    InvalidReturnStatement,
    InvalidAssignmentStatement,
    FunctionAlreadyExists
)

import pytest

def test_semicolon_assign():
    with pytest.raises(SemicolonMissing):
        source = SourceString("a = 1")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_semicolon_function_call():
    with pytest.raises(SemicolonMissing):
        source = SourceString("a()")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_semicolon_function_call():
    with pytest.raises(SemicolonMissing):
        source = SourceString("a()")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()

def test_semicolon_return():
    with pytest.raises(SemicolonMissing):
        source = SourceString("return 1")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()

def test_invalid_function_def():
    with pytest.raises(InvalidFunctionDefinition):
        source = SourceString("fun () {a;}")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_invalid_function_def_bracket():
    with pytest.raises(InvalidFunctionDefinition):
        source = SourceString("fun a ) {a;}")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_invalid_function_def_bracket_exc_info():
    with pytest.raises(InvalidFunctionDefinition) as exc_info:
        source = SourceString("fun a ) {a;}")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()

    exception = exc_info.value
    assert exception.expected == TokenType.BRACKET_OPENING
    assert exception.received == TokenType.BRACKET_CLOSING
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 7


def test_invalid_for_identifier():
    with pytest.raises(InvalidForLoop) as exc_info:
        source = SourceString("for in list {}")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == TokenType.IDENTIFIER
    assert exception.received == TokenType.IN
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 5


def test_invalid_for_block():
    with pytest.raises(MissingExpectedStatement) as exc_info:
        source = SourceString("for a in list {a = 1;")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == TokenType.BRACE_CLOSING
    assert exception.received == TokenType.END_OF_TEXT
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 21


def test_invalid_while_identifier():
    with pytest.raises(InvalidWhileLoop) as exc_info:
        source = SourceString("while x==2 {a=1;}")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == TokenType.BRACKET_OPENING
    assert exception.received == TokenType.IDENTIFIER
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 7


def test_invalid_while_block():
    with pytest.raises(InvalidWhileLoop) as exc_info:
        source = SourceString("while (x==2);")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == "Loop block"
    assert exception.received == TokenType.SEMICOLON
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 13


def test_function_redefinition():
    with pytest.raises(FunctionAlreadyExists) as exc_info:
        source = SourceString("fun print(a) { return a; } fun print(a) { return 1; }")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.name == "print"
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 28

