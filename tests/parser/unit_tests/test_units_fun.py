from parser.parser import Parser, Filter
from lexer.source import SourceString
from lexer.tokens import Token, TokenType, Position
from lexer_mock import LexerMock
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    ReturnStatement,
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
    Block
)

def test_fun_zero_parameter():
    #source = SourceString("fun assign() { x = 2; }")
    tokens = LexerMock([
        Token(TokenType.FUN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "assign"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._functions) == 1 )
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunStatement) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "assign" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 0 )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "x")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)


def test_fun_one_parameter():
    #source = SourceString("fun assign(x) { x = 2; }")
    tokens = LexerMock([
        Token(TokenType.FUN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "assign"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunStatement) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "assign" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 1 )
    assert ( isinstance(parameters[0], Identifier) )
    assert ( parameters[0]._name == "x" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "x")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)


def test_fun_two_parameter():
    source = SourceString("fun add(a, b) { x = a + b; }")
    tokens = LexerMock([
        Token(TokenType.FUN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "add"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.IDENTIFIER, Position(), "b"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "a"),
        Token(TokenType.PLUS, Position()),
        Token(TokenType.IDENTIFIER, Position(), "b"),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunStatement) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "add" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 2 )
    assert ( isinstance(parameters[0], Identifier) )
    assert ( parameters[0]._name == "a" )
    assert ( isinstance(parameters[0], Identifier) )
    assert ( parameters[1]._name == "b" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "x")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, AddTerm) )
    #assert ( expression._value == 2)

def test_fun_return():
    #source = SourceString("fun get(x) { return x; }")
    tokens = LexerMock([
        Token(TokenType.FUN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "get"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.RETURN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunStatement) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "get" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 1 )
    assert ( isinstance(parameters[0], Identifier) )
    assert ( parameters[0]._name == "x" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], ReturnStatement) )

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Identifier) )
    assert ( expression._name == "x")
