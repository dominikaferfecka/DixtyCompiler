from parser.parser import Parser
from lexer.tokens import Token, TokenType, Position
from lexer_mock import LexerMock
from parser.syntax_tree import (
    WhileStatement,
    EqualsTerm,
    Number,
    Identifier,
    Assignment,
    Block
)

def test_while_identifier():
    #source = SourceString("while (x) { a = 2; };")
    tokens = LexerMock([
        Token(TokenType.WHILE, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(),"x"),
        Token(TokenType.BRACKET_CLOSING, Position()),
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
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], WhileStatement) )

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


def test_while_identifier_equals():
    #source = SourceString("while (x == 1) { a = 2; };")
    tokens = LexerMock([
        Token(TokenType.WHILE, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(),"x"),
        Token(TokenType.EQUAL, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.BRACKET_CLOSING, Position()),
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
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], WhileStatement) )

    assert ( isinstance(program._statements[0]._expression, EqualsTerm) )

    left = program._statements[0]._expression._left_additive_term
    assert ( isinstance(left, Identifier) )
    assert ( left._name == "x" )

    right = program._statements[0]._expression._right_additive_term
    assert ( isinstance(right, Number) )
    assert ( right._value == 1 )

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