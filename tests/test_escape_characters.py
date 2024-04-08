from lexer import Lexer, TokenType
from source import SourceString


def test_escape_character_newline():
    lexer = Lexer(SourceString(" \"\\n\" "))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == "\n")


def test_escape_character_slash():
    lexer = Lexer(SourceString(" \" \\\\ \" "))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == " \\ ")


def test_escape_character_r():
    lexer = Lexer(SourceString(" \" \\r \" "))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == " \r ")


def test_escape_character_t():
    lexer = Lexer(SourceString(" \" \\t \" "))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == " \t ")
