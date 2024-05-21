from parser.parser import Parser
from lexer.tokens import Token, TokenType, Position
from lexer_mock import LexerMock
from parser.syntax_tree import (
    Number,
    ObjectAccess,
    Identifier,
    FunCall
)

def test_fun_call_non_args():
    #source = SourceString("start();")

    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"start"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)

    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "start" )

    assert ( program._statements[0]._arguments == None )


def test_fun_call_one_args():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"display"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "display" )

    parameters = program._statements[0]._arguments
    assert ( len(parameters) == 1 )
    assert ( isinstance(parameters[0], Identifier))
    assert( parameters[0]._name == "x")


def test_fun_call_three_args_numbers():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"add"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.INT, Position(), 0),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.FLOAT, Position(), 1.0),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "add" )

    parameters = program._statements[0]._arguments
    assert ( len(parameters) == 3 )
    assert ( isinstance(parameters[0], Number))
    assert( parameters[0]._value == 0)
    
    assert ( isinstance(parameters[1], Number))
    assert( parameters[1]._value == 1)
    
    assert ( isinstance(parameters[2], Number))
    assert( parameters[2]._value == 1.0)


def test_fun_call_object_access():
    #source = SourceString("print(pair.Key);")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"print"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.IDENTIFIER, Position(), "pair"),
        Token(TokenType.DOT, Position()),
        Token(TokenType.IDENTIFIER, Position(), "Key"),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( program._statements[0]._left._name == "print" )
    parameters = program._statements[0]._arguments

    assert ( isinstance(parameters[0], ObjectAccess) )
    assert ( parameters[0]._left_item._name == "pair" )
    assert ( parameters[0]._right_item._name == "Key" )


def test_fun_method_call():
    #source = SourceString("a.b();")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"a"),
        Token(TokenType.DOT, Position()),
        Token(TokenType.IDENTIFIER, Position(), "b"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], ObjectAccess) )
    method_call = program._statements[0]._right_item
    assert ( isinstance(method_call, FunCall) )

    assert ( method_call._left._name == "b" )
    assert ( program._statements[0]._left_item._name == "a" )
