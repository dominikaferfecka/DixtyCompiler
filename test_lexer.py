from lexer import Lexer, Reader, TokenType
import io, sys
import pytest

from errors import (
   IntLimitExceeded, 
   StringLimitExceeded,
   IdentifierLimitExceeded,
   StringNotFinished,
   TokenNotRecognized
)
# different source

# lots of rows
def test_tokens_in_different_rows():
    lexer = Lexer(io.StringIO(
""" And Or
123
12.02
fun
aaa89
"""))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.AND)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 2)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.OR)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 6)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 123)
    assert(token.get_position().get_row() == 2)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FLOAT)
    assert(token.get_value() == 12.02)
    assert(token.get_position().get_row() == 3)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FUN)
    assert(token.get_position().get_row() == 4)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "aaa89")
    assert(token.get_position().get_row() == 5)
    assert(token.get_position().get_column() == 1)


# INTEGER
def test_integer():
    lexer = Lexer(io.StringIO("12 0 03 232322"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 12)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 0)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 4)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 0)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 6)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 3)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 7)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 232322)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 9)

# FLOAT
def test_float():
    lexer = Lexer(io.StringIO("1.5 0.23 5.0023202"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FLOAT)
    assert(token.get_value() == 1.5)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FLOAT)
    assert(token.get_value() == 0.23)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 5)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FLOAT)
    assert(token.get_value() == 5.0023202)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 10)

def test_integer_to_big():
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(io.StringIO("92233720368547758070"))
        token = lexer.get_next_token() 


def test_float_invalid():
    lexer = Lexer(io.StringIO("1.0.5.2"))

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FLOAT)
    assert(token.get_value() == 1.0)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.DOT)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 4)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FLOAT)
    assert(token.get_value() == 5.2)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 5)

def test_float_invalid_comma():
    lexer = Lexer(io.StringIO("1,2"))

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 1)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMA)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 2)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 2)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 3)


def test_float_to_big():
    with pytest.raises(IntLimitExceeded):
        lexer = Lexer(io.StringIO("0.92233720368547758070"))
        token = lexer.get_next_token() 



# IDENTIFIER

def test_identifier():
    lexer = Lexer(io.StringIO("a bc334_dfs"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "a")
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "bc334_dfs")
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 3)    

def test_identifier_starting_from_number():
    lexer = Lexer(io.StringIO("1sd2"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 1)
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "sd2")
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 2)

def test_keyword():
    lexer = Lexer(io.StringIO("if else else_if while for in fun return"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IF)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ELSE)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ELSE_IF)
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.WHILE)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FOR)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IN)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FUN)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.RETURN)

def test_keyword_logical_operators():
    lexer = Lexer(io.StringIO("And Or Not"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.AND)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.OR)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.NOT)

def test_keyword_logical_operators():
    lexer = Lexer(io.StringIO("SELECT FROM WHERE ORDER_BY ASC DESC"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SELECT)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FROM)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.WHERE)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ORDER_BY)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASC)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.DESC)

def test_keyword_values():
    lexer = Lexer(io.StringIO("True False"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.TRUE)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FALSE)


def test_string():
    lexer = Lexer(io.StringIO("\"test\" \"1234\" "))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.STRING)
    assert(token.get_value() == "test")
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 1)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.STRING)
    assert(token.get_value() == "1234")
    assert(token.get_position().get_row() == 1)
    assert(token.get_position().get_column() == 8)

def test_string_not_finished():
    with pytest.raises(StringNotFinished):
        lexer = Lexer(io.StringIO(" \"test"))
        token = lexer.get_next_token() 

def test_string_to_big():
    with pytest.raises(StringLimitExceeded):
        a = "a" * 10**5
        print(a)
        lexer = Lexer(io.StringIO(" \" "+ "a" * 10**8 + "\" "))
        token = lexer.get_next_token() 

def test_operators_comparison():
    lexer = Lexer(io.StringIO("< > <= >= =="))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.LESS)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.MORE)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.LESS_OR_EQUAL)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.MORE_OR_EQUAL)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.EQUAL)

def test_operators():
    lexer = Lexer(io.StringIO("= + - * / . , ;"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASSIGN)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.PLUS)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.MINUS)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASTERISK)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SLASH)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.DOT)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMA)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SEMICOLON)

def test_brackets():
    lexer = Lexer(io.StringIO("( ) [ ] { }"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_OPENING)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_CLOSING)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SQUARE_BRACKET_OPENING)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SQUARE_BRACKET_CLOSING)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACE_OPENING)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACE_CLOSING)

def test_EOF_EOT():
    lexer = Lexer(io.StringIO(""))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.END_OF_TEXT)    

def test_comment():
    lexer = Lexer(io.StringIO("# some comment"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMENT)    
    assert(token.get_value() == " some comment")    

def test_invalid_token():
    with pytest.raises(TokenNotRecognized):
        lexer = Lexer(io.StringIO("%"))
        token = lexer.get_next_token() 
    
def test_source_encoding():
    with open('test_file2.txt', 'w', encoding='utf-8') as f:
        f.write("Żółć")

    lexer = Lexer('test_file2.txt')
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)    
    assert(token.get_value() == "Żółć")    
