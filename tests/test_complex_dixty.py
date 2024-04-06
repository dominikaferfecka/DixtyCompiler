from lexer import Lexer, TokenType
from source import SourceString, SourceFile

def test_arithmetic():
    lexer = Lexer(SourceString(
"""wynik = 2 - 3 * (1 + 8 / 2);
print(wynik);
"""
))

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "wynik")
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASSIGN)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 7)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 2)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 9)
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.MINUS)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 11)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 3)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 13)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASTERISK)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 15)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_OPENING)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 17)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 1)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 18)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.PLUS)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 20)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 8)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 22)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SLASH)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 24)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 2)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 26)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_CLOSING)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 27)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SEMICOLON)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 28)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "print")
    assert(token.get_position().get_row() == 2)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_OPENING)
    assert(token.get_position().get_row() == 2)
    assert(token.get_position().get_column() == 6)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "wynik")
    assert(token.get_position().get_row() == 2)
    assert(token.get_position().get_column() == 7)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_CLOSING)
    assert(token.get_position().get_row() == 2)
    assert(token.get_position().get_column() == 12)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SEMICOLON)
    assert(token.get_position().get_row() == 2)
    assert(token.get_position().get_column() == 13)

def test_for_in_list():
    lexer = Lexer(SourceString(
"""list = [1, 2]

for element in list
{
   print(element); # 12

}
"""
))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "list")
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASSIGN)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 6)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SQUARE_BRACKET_OPENING)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 8)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 1)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 9)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMA)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 10)


    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 2)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 12)


    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SQUARE_BRACKET_CLOSING)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 13)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FOR)
    assert(token.get_position().get_row() == 3)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "element")
    assert(token.get_position().get_row() == 3)
    assert(token.get_position().get_column() == 5)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IN)
    assert(token.get_position().get_row() == 3)
    assert(token.get_position().get_column() == 13)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "list")
    assert(token.get_position().get_row() == 3)
    assert(token.get_position().get_column() == 16)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACE_OPENING)
    assert(token.get_position().get_row() == 4)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "print")
    assert(token.get_position().get_row() == 5)
    assert(token.get_position().get_column() == 4)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_OPENING)
    assert(token.get_position().get_row() == 5)
    assert(token.get_position().get_column() == 9)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "element")
    assert(token.get_position().get_row() == 5)
    assert(token.get_position().get_column() == 10)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_CLOSING)
    assert(token.get_position().get_row() == 5)
    assert(token.get_position().get_column() == 17)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SEMICOLON)
    assert(token.get_position().get_row() == 5)
    assert(token.get_position().get_column() == 18)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMENT)
    assert(token.get_value() == " 12")
    assert(token.get_position().get_row() == 5)
    assert(token.get_position().get_column() == 20)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACE_CLOSING)
    assert(token.get_position().get_row() == 7)
    assert(token.get_position().get_column() == 1)