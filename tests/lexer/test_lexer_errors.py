from lexer.lexer import Lexer
from lexer.source import SourceString
import pytest

from lexer.errors import (
   IntLimitExceeded,
   StringLimitExceeded,
   IdentifierLimitExceeded,
   StringNotFinished,
   TokenNotRecognized,
   UnexpectedEscapeCharacter,
   NotFinishedOperator
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


def test_integer_too_big_parameterize_exc_info():
    INT_MAX_LIMIT = 100
    with pytest.raises(IntLimitExceeded) as exc_info:
        lexer = Lexer(SourceString("101"), INT_MAX_LIMIT)
        lexer.get_next_token() 

    exception = exc_info.value
    assert exception.int_limit == INT_MAX_LIMIT
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 1

def test_float_too_big_defaut_limit():
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(SourceString("0.92233720368547758070"))
        lexer.get_next_token() 


def test_float_too_big_parameterize():
    INT_MAX_LIMIT = 100
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(SourceString("0.101"), INT_MAX_LIMIT)
        lexer.get_next_token() 


def test_float_too_big_parameterize_exc_info():
    INT_MAX_LIMIT = 100
    with pytest.raises(IntLimitExceeded) as exc_info:
        lexer = Lexer(SourceString("0.101"), INT_MAX_LIMIT)
        lexer.get_next_token() 
    
    exception = exc_info.value
    assert exception.int_limit == INT_MAX_LIMIT
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 1


def test_identifier_too_big_default_limit():
    with pytest.raises(IdentifierLimitExceeded):
        lexer = Lexer(SourceString("a" * 10 ** 8))
        lexer.get_next_token()


def test_identifier_too_big_parameterize():
    INT_MAX_LIMIT = 100
    STRING_MAX_LIMIT = 5
    IDENTIFIER_MAX_LIMIT = 5
    with pytest.raises(IdentifierLimitExceeded):
        lexer = Lexer(SourceString("a23456"), INT_MAX_LIMIT, STRING_MAX_LIMIT, IDENTIFIER_MAX_LIMIT)
        lexer.get_next_token()


def test_identifier_too_big_parameterize_exc_info():
    INT_MAX_LIMIT = 100
    STRING_MAX_LIMIT = 5
    IDENTIFIER_MAX_LIMIT = 5
    with pytest.raises(IdentifierLimitExceeded) as exc_info:
        lexer = Lexer(SourceString("a23456"), INT_MAX_LIMIT, STRING_MAX_LIMIT, IDENTIFIER_MAX_LIMIT)
        lexer.get_next_token()

    exception = exc_info.value
    assert exception.identifier_limit == IDENTIFIER_MAX_LIMIT
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 1


def test_string_too_big_default_limit():
    with pytest.raises(StringLimitExceeded):
        a = "a" * 10**5
        print(a)
        lexer = Lexer(SourceString(" \" " + "a" * 10**8 + "\" "))
        lexer.get_next_token()


def test_string_too_big_parameterize():
    INT_MAX_LIMIT = 100
    STRING_MAX_LIMIT = 5
    with pytest.raises(StringLimitExceeded):
        lexer = Lexer(SourceString(" \" 123456 \" "), INT_MAX_LIMIT, STRING_MAX_LIMIT)
        lexer.get_next_token()


def test_string_too_big_parameterize_exc_info():
    INT_MAX_LIMIT = 100
    STRING_MAX_LIMIT = 5
    with pytest.raises(StringLimitExceeded) as exc_info:
        lexer = Lexer(SourceString(" \" 123456 \" "), INT_MAX_LIMIT, STRING_MAX_LIMIT)
        lexer.get_next_token()
    
    exception = exc_info.value
    assert exception.string_limit == STRING_MAX_LIMIT
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 2


def test_string_not_finished():
    with pytest.raises(StringNotFinished):
        lexer = Lexer(SourceString(" \"test"))
        lexer.get_next_token()


def test_string_not_finished_exc_info():
    with pytest.raises(StringNotFinished) as exc_info:
        lexer = Lexer(SourceString(" \"test"))
        lexer.get_next_token()
    
    exception = exc_info.value
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 2


def test_unexpected_escape_character():
    with pytest.raises(UnexpectedEscapeCharacter):
        lexer = Lexer(SourceString(" \" \% \""))
        lexer.get_next_token()


def test_unexpected_escape_character_exc_info():
    with pytest.raises(UnexpectedEscapeCharacter) as exc_info:
        lexer = Lexer(SourceString(" \" \% \""))
        lexer.get_next_token()

    exception = exc_info.value
    assert exception.character == '%'
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 2


def test_invalid_token():
    with pytest.raises(TokenNotRecognized):
        lexer = Lexer(SourceString("$"))
        lexer.get_next_token()


def test_invalid_token_exc_info():
    with pytest.raises(TokenNotRecognized) as exc_info:
        lexer = Lexer(SourceString("$"))
        lexer.get_next_token()

    exception = exc_info.value
    assert exception.not_recognized == '$'
    assert exception.position.get_row() == 1
    assert exception.position.get_column() == 1


def test_invalid_not_equal():
    with pytest.raises(NotFinishedOperator):
        lexer = Lexer(SourceString("! a"))
        lexer.get_next_token()
