from lexer import Lexer, TokenType
import pytest
from source import SourceString, SourceFile

from errors import (
   IntLimitExceeded, 
   StringLimitExceeded,
   IdentifierLimitExceeded,
   StringNotFinished,
   TokenNotRecognized
)

def test_integer_too_big_default_limit():
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(SourceString("92233720368547758070"))
        lexer.get_next_token() 


def test_integer_too_big_parameterize():
    INT_MAX_LIMIT = 100
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(SourceString("101"), INT_MAX_LIMIT)
        lexer.get_next_token() 


def test_float_too_big_defaut_limit():
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(SourceString("0.92233720368547758070"))
        lexer.get_next_token() 


def test_float_too_big_parameterize():
    INT_MAX_LIMIT = 100
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(SourceString("0.101"), INT_MAX_LIMIT)
        lexer.get_next_token() 


def test_identifier_too_big_default_limit():
    with pytest.raises(IdentifierLimitExceeded):
        lexer = Lexer(SourceString("a" * 10**8 ))
        lexer.get_next_token()


def test_identifier_too_big_parameterize():
    INT_MAX_LIMIT = 100
    STRING_MAX_LIMIT = 5
    IDENTIFIER_MAX_LIMIT = 5
    with pytest.raises(IdentifierLimitExceeded):
        lexer = Lexer(SourceString("a23456"), INT_MAX_LIMIT, STRING_MAX_LIMIT, IDENTIFIER_MAX_LIMIT)
        lexer.get_next_token() 
    

def test_string_too_big_default_limit():
    with pytest.raises(StringLimitExceeded):
        a = "a" * 10**5
        print(a)
        lexer = Lexer(SourceString(" \" "+ "a" * 10**8 + "\" "))
        lexer.get_next_token() 


def test_string_too_big_parameterize():
    INT_MAX_LIMIT = 100
    STRING_MAX_LIMIT = 5
    with pytest.raises(StringLimitExceeded):
        lexer = Lexer(SourceString(" \" 123456 \" "), INT_MAX_LIMIT, STRING_MAX_LIMIT)
        lexer.get_next_token() 


def test_string_not_finished():
    with pytest.raises(StringNotFinished):
        lexer = Lexer(SourceString(" \"test"))
        lexer.get_next_token() 


def test_invalid_token():
    with pytest.raises(TokenNotRecognized):
        lexer = Lexer(SourceString("%"))
        lexer.get_next_token() 