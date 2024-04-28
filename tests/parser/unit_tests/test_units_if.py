from parser.parser import Parser, Filter
from lexer.source import SourceString
from lexer.tokens import Token, TokenType, Position
from lexer_mock import LexerMock
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
    Block
)

def test_if_identifier():
    #source = SourceString("if (x) { a = 2; };")
    tokens = LexerMock([
        Token(TokenType.IF, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], IfStatement) )

    assert ( isinstance(program._statements[0]._expression, Identifier) )
    assert ( program._statements[0]._expression._name == "x" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)


def test_if_bool():
    #source = SourceString("if (True) { a = 2; };")
    tokens = LexerMock([
        Token(TokenType.IF, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.TRUE, Position()),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], IfStatement) )

    assert ( isinstance(program._statements[0]._expression, Bool) )
    assert ( program._statements[0]._expression._value == True )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)


def test_if_else():
    #source = SourceString("if (x) { a = 2; } else { a = 3; }")
    tokens = LexerMock([
        Token(TokenType.IF, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),

        Token(TokenType.ELSE, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 3),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),

        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], IfStatement) )

    assert ( isinstance(program._statements[0]._expression, Identifier) )
    assert ( program._statements[0]._expression._name == "x" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)

    else_statement = program._statements[0]._else_statement
    assert ( isinstance(else_statement, ElseStatement) )
    assert ( isinstance(else_statement._block, Block) )


def test_if_else_if():
    #source = SourceString("if (x) { a = 2; } else_if (y) { a = 3; }")
    tokens = LexerMock([
        Token(TokenType.IF, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),

        Token(TokenType.ELSE_IF, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "y"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 3),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),

        Token(TokenType.END_OF_TEXT, Position())
    ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], IfStatement) )

    assert ( isinstance(program._statements[0]._expression, Identifier) )
    assert ( program._statements[0]._expression._name == "x" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)

    else_if_statement = program._statements[0]._else_if_statement[0]
    assert ( isinstance(else_if_statement, ElseIfStatement) )
    assert ( isinstance(else_if_statement._block, Block) )
