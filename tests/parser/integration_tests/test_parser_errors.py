from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceString
from lexer.lexer import TokenType
import pytest

from parser.errors import (
    SemicolonMissing,
    MissingExpectedStatement,
    InvalidFunctionDefinition,
    InvalidWhileLoop,
    InvalidForLoop,
    FunctionAlreadyExists,
    DictInvalidElement,
    InvalidIfStatement,
    UsedNotRecognizedStatement
)

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

# czy parser powinien już to wywalić?
def test_assign_dict_non_dict():
    with pytest.raises(DictInvalidElement) as exc_info:
        source = SourceString("dict = {1};")
        filter = Filter(source)
        parser = Parser(filter)
        
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.element._value == 1
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 8


def test_assign_fun_call_two():
    with pytest.raises(SemicolonMissing):
        source = SourceString(" a = b()();")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_assign_to_fun_call():
    with pytest.raises(SemicolonMissing):
        source = SourceString(" a() = 2;")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_assign_instead_equal():
    with pytest.raises(InvalidIfStatement):
        source = SourceString("if (2 = 2) {}")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_missing_FROM():
    with pytest.raises(MissingExpectedStatement):
        source = SourceString("result = SELECT (Key,Value) WHERE (Key.Length() == 3);")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()


def test_unrecognized_statement():
    with pytest.raises(UsedNotRecognizedStatement):
        source = SourceString("2 + 3;")
        filter = Filter(source)
        parser = Parser(filter)
        parser.parse_program()
