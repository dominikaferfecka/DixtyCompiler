from lexer import Lexer, TokenType
from source import SourceString, SourceFile


def test_char_not_english():
    lexer = Lexer(SourceString("象"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "象")


def test_chinese_characters():
    lexer = Lexer(SourceString("\"假\" 借 字"))

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == "假")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "借")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "字")


def test_cyrillic_characters():
    lexer = Lexer(SourceString("\"Б\" Ё Л"))

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == "Б")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "Ё")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "Л")


def test_chars_not_english_from_file():
    lexer = Lexer(SourceFile("test_file2.txt"))

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == "假")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "借")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "字")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == "Б")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "Ё")

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "Л")
