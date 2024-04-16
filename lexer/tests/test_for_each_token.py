from lexer import Lexer, TokenType
from source import SourceString

# TESTS FOR EACH TOKEN

# Keywords


def test_if():
    lexer = Lexer(SourceString("if"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IF)


def test_else():
    lexer = Lexer(SourceString("else"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.ELSE)


def test_else_if():
    lexer = Lexer(SourceString("else_if"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.ELSE_IF)


def test_while():
    lexer = Lexer(SourceString("while"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.WHILE)


def test_for():
    lexer = Lexer(SourceString("for"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.FOR)


def test_in():
    lexer = Lexer(SourceString("in"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IN)


def test_fun():
    lexer = Lexer(SourceString("fun"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.FUN)


def test_return():
    lexer = Lexer(SourceString("return"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.RETURN)


def test_select():
    lexer = Lexer(SourceString("SELECT"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.SELECT)


def test_from():
    lexer = Lexer(SourceString("FROM"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.FROM)


def test_where():
    lexer = Lexer(SourceString("WHERE"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.WHERE)


def test_order_by():
    lexer = Lexer(SourceString("ORDER_BY"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.ORDER_BY)


def test_asc():
    lexer = Lexer(SourceString("ASC"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.ASC)


def test_desc():
    lexer = Lexer(SourceString("DESC"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.DESC)


def test_true():
    lexer = Lexer(SourceString("True"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.TRUE)


def test_false():
    lexer = Lexer(SourceString("False"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.FALSE)


def test_and():
    lexer = Lexer(SourceString("And"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.AND)


def test_or():
    lexer = Lexer(SourceString("Or"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.OR)


def test_not():
    lexer = Lexer(SourceString("Not"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.NOT)

# operators


def test_plus():
    lexer = Lexer(SourceString("+"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.PLUS)


def test_minus():
    lexer = Lexer(SourceString("-"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.MINUS)


def test_asterisk():
    lexer = Lexer(SourceString("*"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.ASTERISK)


def test_slash():
    lexer = Lexer(SourceString("/"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.SLASH)


def test_dot():
    lexer = Lexer(SourceString("."))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.DOT)


def test_comma():
    lexer = Lexer(SourceString(","))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.COMMA)


def test_semicolon():
    lexer = Lexer(SourceString(";"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.SEMICOLON)


def test_assign():
    lexer = Lexer(SourceString("="))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.ASSIGN)

# comparison operators


def test_less():
    lexer = Lexer(SourceString("<"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.LESS)


def test_more():
    lexer = Lexer(SourceString(">"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.MORE)


def test_less_or_equal():
    lexer = Lexer(SourceString("<="))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.LESS_OR_EQUAL)


def test_more_or_equal():
    lexer = Lexer(SourceString(">="))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.MORE_OR_EQUAL)


def test_equal():
    lexer = Lexer(SourceString("=="))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.EQUAL)

# brackets


def test_bracket_opening():
    lexer = Lexer(SourceString("("))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.BRACKET_OPENING)


def test_bracket_closing():
    lexer = Lexer(SourceString(")"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.BRACKET_CLOSING)


def test_square_bracket_opening():
    lexer = Lexer(SourceString("["))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.SQUARE_BRACKET_OPENING)


def test_square_bracket_closing():
    lexer = Lexer(SourceString("]"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.SQUARE_BRACKET_CLOSING)


def test_brace_opening():
    lexer = Lexer(SourceString("{"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.BRACE_OPENING)


def test_brace_closing():
    lexer = Lexer(SourceString("}"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.BRACE_CLOSING)


def test_identifier():
    lexer = Lexer(SourceString("a123"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.IDENTIFIER)
    assert (token.get_value() == "a123")


def test_end_ot_text():
    lexer = Lexer(SourceString(""))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.END_OF_TEXT)


def test_comment():
    lexer = Lexer(SourceString("#abc"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.COMMENT)
    assert (token.get_value() == "abc")


def test_string():
    lexer = Lexer(SourceString("\"a\""))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.STRING)
    assert (token.get_value() == "a")


def test_integer():
    lexer = Lexer(SourceString("1"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.INT)
    assert (token.get_value() == 1)


def test_float():
    lexer = Lexer(SourceString("1.0"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.FLOAT)
    assert (token.get_value() == 1.0)


def test_tokens_in_two_rows():
    lexer = Lexer(SourceString("12\n34;"))
    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.INT)
    assert (token.get_value() == 12)
    assert (token.get_position().get_row() == 1)
    assert (token.get_position().get_column() == 1)

    # token = lexer.get_next_token()
    # assert (token.get_token_type() == TokenType.SEMICOLON)
    # assert (token.get_position().get_row() == 1)
    # assert (token.get_position().get_column() == 3)

    token = lexer.get_next_token()
    assert (token.get_token_type() == TokenType.INT)
    assert (token.get_value() == 34)
    assert (token.get_position().get_row() == 2)
    assert (token.get_position().get_column() == 1)
