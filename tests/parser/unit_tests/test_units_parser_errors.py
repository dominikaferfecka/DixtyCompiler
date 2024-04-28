from parser.parser import Parser, Filter
from lexer.source import SourceString
from lexer.lexer import TokenType
from lexer.tokens import Token, TokenType, Position
from lexer_mock import LexerMock
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
    FunctionAlreadyExists,
    DictInvalidElement
)

import pytest

def test_semicolon_assign():
    with pytest.raises(SemicolonMissing):
        #source = SourceString("a = 1")
        tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.END_OF_TEXT, Position())
        ])

        parser = Parser(tokens)
        parser.parse_program()


def test_semicolon_function_call():
    with pytest.raises(SemicolonMissing):
        #source = SourceString("a()")
        tokens = LexerMock([
            Token(TokenType.IDENTIFIER, Position(),"a"),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.END_OF_TEXT, Position())
        ])
        parser = Parser(tokens)
        parser.parse_program()


def test_semicolon_return():
    with pytest.raises(SemicolonMissing):
        source = SourceString("return 1")
        tokens = LexerMock([
            Token(TokenType.RETURN, Position()),
            Token(TokenType.INT, Position(), 1),
            Token(TokenType.END_OF_TEXT, Position())
        ])
        parser = Parser(tokens)
        parser.parse_program()

def test_invalid_function_def():
    with pytest.raises(InvalidFunctionDefinition):
        #source = SourceString("fun () {a;}")
        tokens = LexerMock([
            Token(TokenType.FUN, Position()),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.BRACE_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.BRACE_CLOSING, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        parser.parse_program()


def test_invalid_function_def_bracket():
    with pytest.raises(InvalidFunctionDefinition):
        #source = SourceString("fun a ) {a;}")
        tokens = LexerMock([
            Token(TokenType.FUN, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.BRACE_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.BRACE_CLOSING, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        parser.parse_program()


def test_invalid_function_def_bracket_exc_info():
    with pytest.raises(InvalidFunctionDefinition) as exc_info:
        #source = SourceString("fun a ) {a;}")
        tokens = LexerMock([
            Token(TokenType.FUN, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.BRACE_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.BRACE_CLOSING, Position()),
            Token(TokenType.END_OF_TEXT, Position())
        ])
        parser = Parser(tokens)
        parser.parse_program()

    exception = exc_info.value
    assert exception.expected == TokenType.BRACKET_OPENING
    assert exception.received == TokenType.BRACKET_CLOSING
    assert exception.position.get_row() == 1


def test_invalid_for_identifier():
    with pytest.raises(InvalidForLoop) as exc_info:
        #source = SourceString("for in list {}")
        tokens = LexerMock([
            Token(TokenType.FOR, Position()),
            Token(TokenType.IN, Position()),
            Token(TokenType.IDENTIFIER, Position(),"list"),
            Token(TokenType.BRACE_OPENING, Position()),
            Token(TokenType.BRACE_CLOSING, Position()),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == TokenType.IDENTIFIER
    assert exception.received == TokenType.IN
    assert exception.position.get_row() == 1

def test_invalid_for_block():
    with pytest.raises(MissingExpectedStatement) as exc_info:
        source = SourceString("for a in list {a = 1;")
        tokens = LexerMock([
            Token(TokenType.FOR, Position()),
            Token(TokenType.IDENTIFIER, Position(),"a"),
            Token(TokenType.IN, Position()),
            Token(TokenType.IDENTIFIER, Position(), "list"),
            Token(TokenType.BRACE_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.ASSIGN, Position()),
            Token(TokenType.INT, Position(), 1),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == TokenType.BRACE_CLOSING
    assert exception.received == TokenType.END_OF_TEXT
    assert exception.position.get_row() == 1


def test_invalid_while_identifier():
    with pytest.raises(InvalidWhileLoop) as exc_info:
        #source = SourceString("while x {a=1;}")
        tokens = LexerMock([
            Token(TokenType.WHILE, Position()),
            Token(TokenType.IDENTIFIER, Position(),"x"),
            Token(TokenType.BRACE_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(),"a"),
            Token(TokenType.ASSIGN, Position()),
            Token(TokenType.INT, Position(), 2),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.BRACE_CLOSING, Position()),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == TokenType.BRACKET_OPENING
    assert exception.received == TokenType.IDENTIFIER
    assert exception.position.get_row() == 1


def test_invalid_while_block():
    with pytest.raises(InvalidWhileLoop) as exc_info:
        #source = SourceString("while (x);")
        tokens = LexerMock([
            Token(TokenType.WHILE, Position()),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(),"x"),
             Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.expected == "Loop block"
    assert exception.received == TokenType.SEMICOLON
    assert exception.position.get_row() == 1

def test_function_redefinition():
    with pytest.raises(FunctionAlreadyExists) as exc_info:
        #source = SourceString("fun print(a) { return a; } fun print(b) { return 1; }")
        tokens = LexerMock([
            Token(TokenType.FUN, Position()),
            Token(TokenType.IDENTIFIER, Position(), "print"),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.RETURN, Position()),
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.SEMICOLON, Position()),

            Token(TokenType.FUN, Position()),
            Token(TokenType.IDENTIFIER, Position(), "print"),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.IDENTIFIER, Position(), "b"),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.RETURN, Position()),
            Token(TokenType.INT, Position(), 1),
            Token(TokenType.SEMICOLON, Position()),

            Token(TokenType.END_OF_TEXT, Position())
        ])
        parser = Parser(tokens)
        parser.parse_program()
    
    exception = exc_info.value
    assert exception.name == "print"
    assert exception.position.get_row() == 1

# czy parser powinien już to wywalić?
def test_assign_dict_non_dict():
    with pytest.raises(DictInvalidElement) as exc_info:
        #source = SourceString("dict = {1};")
        tokens = LexerMock([
            Token(TokenType.IDENTIFIER, Position(),"dict"),
            Token(TokenType.ASSIGN, Position()),
            Token(TokenType.BRACE_OPENING, Position()),
            Token(TokenType.INT, Position(), 1),
            Token(TokenType.BRACE_CLOSING, Position()),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        
        program = parser.parse_program()
    
    exception = exc_info.value
    assert exception.element._value == 1
    assert exception.position.get_row() == 1


def test_assign_fun_call_two():
    with pytest.raises(SemicolonMissing):
        #source = SourceString(" a = b()();")
        tokens = LexerMock([
            Token(TokenType.IDENTIFIER, Position(),"a"),
            Token(TokenType.ASSIGN, Position()),
            Token(TokenType.IDENTIFIER, Position(), "b"),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        program = parser.parse_program()


def test_assign_to_fun_call():
    with pytest.raises(SemicolonMissing):
        #source = SourceString(" a() = 2;")
        tokens = LexerMock([
            Token(TokenType.IDENTIFIER, Position(), "a"),
            Token(TokenType.BRACKET_OPENING, Position()),
            Token(TokenType.BRACKET_CLOSING, Position()),
            Token(TokenType.ASSIGN, Position()),
            Token(TokenType.INT, Position(), 2),
            Token(TokenType.SEMICOLON, Position()),
            Token(TokenType.END_OF_TEXT, Position())
            ])
        parser = Parser(tokens)
        program = parser.parse_program()

