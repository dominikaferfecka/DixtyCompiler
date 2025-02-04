from lexer.lexer import Lexer, TokenType
from lexer.source import SourceString

def test_n_newline():
    lexer = Lexer(SourceString("a\n a"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 1)
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 2)


def test_first_n_newline():
    lexer = Lexer(SourceString("\n a"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 2)


def test_n_newline_two_second():
    lexer = Lexer(SourceString("a\n\n a"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 1)
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 3)


def test_n_newline_two():
    lexer = Lexer(SourceString("\n\n a"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 3)


def test_n_newline_five():
    lexer = Lexer(SourceString("\n\n\n\n\n a"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 6)


def test_n_r_newline():
    lexer = Lexer(SourceString("\n\ra"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 2)


def test_n_r_newline_two():
    lexer = Lexer(SourceString("\n\r\n\ra"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 3)


def test_n_r_newline_five():
    lexer = Lexer(SourceString("\n\r\n\r\n\r \n\r \n\ra"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 6)


def test_r_n_newline():
    lexer = Lexer(SourceString("\r\na"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 2)


def test_r_n_newline_two():
    lexer = Lexer(SourceString("\r\n\r\na"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 3)


def test_r_n_newline_five():
    lexer = Lexer(SourceString("\r\n \r\n \r\n \r\n \r\n a"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 6)


def test_r_not_newline():
    lexer = Lexer(SourceString("\r a"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 1)


def test_r_not_newline_two():
    lexer = Lexer(SourceString("\r\ra"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 1)
    assert (token.get_position().get_column() == 3)


def test_n_n_r_newline():
    lexer = Lexer(SourceString("\n\na"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 3)

def test_n_n_r_newline():
    lexer = Lexer(SourceString("\n\n\ra"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 3)

def test_n_n_r_n_newline():
    lexer = Lexer(SourceString("\n\n\r\na"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 4)

def test_n_n_r_col_newline():
    lexer = Lexer(SourceString("\n\n\ra"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a")
    assert (token.get_position().get_row() == 3)
    assert (token.get_position().get_column() == 2)