from lexer import Lexer, Reader, TokenType
import io

# different source

# lots of rows

# errors

# duże liczby poza limit

# INTEGER
def test_integer():
    lexer = Lexer(io.StringIO("12 0 03 232322"))
    
    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 12)
    assert(token._position._row == 1)
    assert(token._position._column == 1)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 0)
    assert(token._position._row == 1)
    assert(token._position._column == 4)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 0)
    assert(token._position._row == 1)
    assert(token._position._column == 6)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 3)
    assert(token._position._row == 1)
    assert(token._position._column == 7)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 232322)
    assert(token._position._row == 1)
    assert(token._position._column == 9)

# FLOAT
def test_float():
    lexer = Lexer(io.StringIO("1.5 0.23 5.0023202"))
    
    token = lexer.get_next_token()
    assert(token._token_type == TokenType.FLOAT)
    assert(token._value == 1.5)
    assert(token._position._row == 1)
    assert(token._position._column == 1)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.FLOAT)
    assert(token._value == 0.23)
    assert(token._position._row == 1)
    assert(token._position._column == 5)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.FLOAT)
    assert(token._value == 5.0023202)
    assert(token._position._row == 1)
    assert(token._position._column == 10)


def test_float_invalid():
    lexer = Lexer(io.StringIO("1.0.5.2"))

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.FLOAT)
    assert(token._value == 1.0)
    assert(token._position._row == 1)
    assert(token._position._column == 1)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.DOT)
    assert(token._position._row == 1)
    assert(token._position._column == 4)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.FLOAT)
    assert(token._value == 5.2)
    assert(token._position._row == 1)
    assert(token._position._column == 5)

def test_float_invalid_comma():
    lexer = Lexer(io.StringIO("1,2"))

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 1)
    assert(token._position._row == 1)
    assert(token._position._column == 1)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.COMMA)
    assert(token._position._row == 1)
    assert(token._position._column == 2)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 2)
    assert(token._position._row == 1)
    assert(token._position._column == 3)






# IDENTIFIER

def test_identifier():
    lexer = Lexer(io.StringIO("a bc334_dfs"))
    
    token = lexer.get_next_token()
    assert(token._token_type == TokenType.IDENTIFIER)
    assert(token._value == "a")
    assert(token._position._row == 1)
    assert(token._position._column == 1)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.IDENTIFIER)
    assert(token._value == "bc334_dfs")
    assert(token._position._row == 1)
    assert(token._position._column == 3)    

def test_identifier_starting_from_number():
    lexer = Lexer(io.StringIO("1sd2"))
    
    token = lexer.get_next_token()
    assert(token._token_type == TokenType.INT)
    assert(token._value == 1)
    assert(token._position._row == 1)
    assert(token._position._column == 1)

    token = lexer.get_next_token()
    assert(token._token_type == TokenType.IDENTIFIER)
    assert(token._value == "sd2")
    assert(token._position._row == 1)
    assert(token._position._column == 2)