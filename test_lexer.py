from lexer import Lexer, Reader, TokenType
import io, sys
import pytest
from source import SourceString, SourceFile

from errors import (
   IntLimitExceeded, 
   StringLimitExceeded,
   IdentifierLimitExceeded,
   StringNotFinished,
   TokenNotRecognized
)

# TESTS FOR EACH TOKEN

# Keywords
def test_if():
    lexer = Lexer(SourceString("if"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IF)

def test_else():
    lexer = Lexer(SourceString("else"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ELSE)


def test_else_if():
    lexer = Lexer(SourceString("else_if"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ELSE_IF)

def test_while():
    lexer = Lexer(SourceString("while"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.WHILE)

def test_for():
    lexer = Lexer(SourceString("for"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FOR)

def test_in():
    lexer = Lexer(SourceString("in"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IN)

def test_fun():
    lexer = Lexer(SourceString("fun"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FUN)

def test_return():
    lexer = Lexer(SourceString("return"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.RETURN)

def test_select():
    lexer = Lexer(SourceString("SELECT"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SELECT)

def test_from():
    lexer = Lexer(SourceString("FROM"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FROM)

def test_where():
    lexer = Lexer(SourceString("WHERE"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.WHERE)

def test_order_by():
    lexer = Lexer(SourceString("ORDER_BY"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ORDER_BY)

def test_asc():
    lexer = Lexer(SourceString("ASC"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASC)

def test_desc():
    lexer = Lexer(SourceString("DESC"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.DESC)

def test_true():
    lexer = Lexer(SourceString("True"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.TRUE)

def test_false():
    lexer = Lexer(SourceString("False"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FALSE)

def test_and():
    lexer = Lexer(SourceString("And"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.AND)

def test_or():
    lexer = Lexer(SourceString("Or"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.OR)

def test_not():
    lexer = Lexer(SourceString("Not"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.NOT)

# operators

def test_plus():
    lexer = Lexer(SourceString("+"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.PLUS)

def test_minus():
    lexer = Lexer(SourceString("-"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.MINUS)

def test_asterisk():
    lexer = Lexer(SourceString("*"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASTERISK)

def test_slash():
    lexer = Lexer(SourceString("/"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SLASH)

def test_dot():
    lexer = Lexer(SourceString("."))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.DOT)

def test_comma():
    lexer = Lexer(SourceString(","))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMA)

def test_semicolon():
    lexer = Lexer(SourceString(";"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SEMICOLON)

def test_assign():
    lexer = Lexer(SourceString("="))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.ASSIGN)

# comparison operators

def test_less():
    lexer = Lexer(SourceString("<"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.LESS)

def test_more():
    lexer = Lexer(SourceString(">"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.MORE)

def test_less_or_equal():
    lexer = Lexer(SourceString("<="))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.LESS_OR_EQUAL)

def test_more_or_equal():
    lexer = Lexer(SourceString(">="))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.MORE_OR_EQUAL)

def test_equal():
    lexer = Lexer(SourceString("=="))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.EQUAL)

# brackets

def test_bracket_opening():
    lexer = Lexer(SourceString("("))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_OPENING)

def test_bracket_closing():
    lexer = Lexer(SourceString(")"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACKET_CLOSING)

def test_square_bracket_opening():
    lexer = Lexer(SourceString("["))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SQUARE_BRACKET_OPENING)

def test_square_bracket_closing():
    lexer = Lexer(SourceString("]"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.SQUARE_BRACKET_CLOSING)

def test_brace_opening():
    lexer = Lexer(SourceString("{"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACE_OPENING)

def test_brace_closing():
    lexer = Lexer(SourceString("}"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.BRACE_CLOSING)
    
def test_identifier():
    lexer = Lexer(SourceString("a123"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)
    assert(token.get_value() == "a123")

def test_end_ot_text():
    lexer = Lexer(SourceString(""))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.END_OF_TEXT)

def test_comment():
    lexer = Lexer(SourceString("# abc"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMENT)
    assert(token.get_value() == "abc")

def test_string():
    lexer = Lexer(SourceString("\"a\""))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.STRING)
    assert(token.get_value() == "a")

def test_integer():
    lexer = Lexer(SourceString("1"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.INT)
    assert(token.get_value() == 1)

def test_float():
    lexer = Lexer(SourceString("1.0"))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FLOAT)
    assert(token.get_value() == 1.0)


# lots of rows
def test_tokens_in_different_rows():
    lexer = Lexer(SourceString(
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
def test_integers():
    lexer = Lexer(SourceString("12 0 03 232322"))
    
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
def test_floats():
    lexer = Lexer(SourceString("1.5 0.23 5.0023202"))
    
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
        lexer = Lexer(SourceString("92233720368547758070"))
        token = lexer.get_next_token() 


def test_float_invalid():
    lexer = Lexer(SourceString("1.0.5.2"))

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
    lexer = Lexer(SourceString("1,2"))

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
        lexer = Lexer(SourceString("0.92233720368547758070"))
        token = lexer.get_next_token() 



# IDENTIFIER

def test_identifiers():
    lexer = Lexer(SourceString("a bc334_dfs"))
    
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
    lexer = Lexer(SourceString("1sd2"))
    
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

def test_keywords():
    lexer = Lexer(SourceString("if else else_if while for in fun return"))
    
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
    lexer = Lexer(SourceString("And Or Not"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.AND)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.OR)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.NOT)

def test_keyword_logical_operators():
    lexer = Lexer(SourceString("SELECT FROM WHERE ORDER_BY ASC DESC"))
    
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
    lexer = Lexer(SourceString("True False"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.TRUE)

    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.FALSE)


def test_strings():
    lexer = Lexer(SourceString("\"test\" \"1234\" "))
    
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
        lexer = Lexer(SourceString(" \"test"))
        lexer.get_next_token() 

def test_string_too_big():
    with pytest.raises(StringLimitExceeded):
        a = "a" * 10**5
        print(a)
        lexer = Lexer(SourceString(" \" "+ "a" * 10**8 + "\" "))
        token = lexer.get_next_token() 

def test_escape_character_newline():
    lexer = Lexer(SourceString(" \"\\n\" "))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.STRING)
    assert(token.get_value() == "\n")

def test_escape_character_slash():
    lexer = Lexer(SourceString(" \" \\\\ \" "))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.STRING)
    assert(token.get_value() == " \\ ")

def test_escape_character_r():
    lexer = Lexer(SourceString(" \" \\r \" "))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.STRING)
    assert(token.get_value() == " \r ")


def test_escape_character_t():
    lexer = Lexer(SourceString(" \" \\t \" "))
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.STRING)
    assert(token.get_value() == " \t ")




def test_operators_comparison():
    lexer = Lexer(SourceString("< > <= >= =="))
    
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
    lexer = Lexer(SourceString("= + - * / . , ;"))
    
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
    lexer = Lexer(SourceString("( ) [ ] { }"))
    
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
    lexer = Lexer(SourceString(""))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.END_OF_TEXT)


def test_comment():
    lexer = Lexer(SourceString("# some comment"))
    
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.COMMENT)    
    assert(token.get_value() == " some comment")    

def test_invalid_token():
    with pytest.raises(TokenNotRecognized):
        lexer = Lexer(SourceString("%"))
        token = lexer.get_next_token() 
    
def test_source_encoding():
    with open('test_file2.txt', 'w', encoding='utf-8') as f:
        f.write("Żółć")

    lexer = Lexer('test_file2.txt')
    token = lexer.get_next_token()
    assert(token.get_token_type() == TokenType.IDENTIFIER)    
    assert(token.get_value() == "Żółć")    
