from parser.parser import Parser, Filter
from lexer.source import SourceString
import sys
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    IfStatement,
    OrTerm,
    AndTerm,
    NotTerm,
    LessTerm,
    MoreTerm,
    EqualsTerm,
    LessOrEqualTerm,
    MoreOrEqualTerm,
    AddTerm,
    SubTerm,
    MultTerm,
    DivTerm,
    SignedFactor,
    Number,
    ObjectAccess,
    Item,
    IndexAccess,
    Identifier,
    Assignment,
    String,
    Bool,
    List,
    Pair,
    Dict,
    SelectTerm
)
from lexer.tokens import Token, TokenType, Position
from lexer_mock import LexerMock

def test_assign_number():  
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 1)


def test_assign_float():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"float"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.FLOAT, Position(), 1.0),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "float")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 1.0)


def test_assign_string():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"text"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.STRING, Position(), "a"),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "text")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, String) )
    assert ( expression._value == "a")


def test_assign_bool_true():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"bool"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.TRUE, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "bool")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Bool) )
    assert ( expression._value == True)


def test_assign_bool_false():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"bool"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.FALSE, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()

    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "bool")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Bool) )
    assert ( expression._value == False)


def test_assign_list_empty():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"list"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.SQUARE_BRACKET_OPENING, Position()),
        Token(TokenType.SQUARE_BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "list")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, List) )
    assert ( expression._values == [])


def test_assign_list_one_value():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"list"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.SQUARE_BRACKET_OPENING, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.SQUARE_BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)

    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "list")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, List) )

    values = expression._values
    assert ( len(values) == 1)
    assert ( values[0]._value == 1)


def test_assign_list_three_values():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"list"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.SQUARE_BRACKET_OPENING, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.INT, Position(), 3),
        Token(TokenType.SQUARE_BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)

    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "list")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, List) )

    values = expression._values
    assert ( len(values) == 3)
    assert ( values[0]._value == 1)
    assert ( values[1]._value == 2)
    assert ( values[2]._value == 3)


def test_assign_pair_empty():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"pair"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "pair")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Pair) )
    # assert ( expression._first = 1 )
    # assert ( expression._second = 1 )


def test_assign_dict_empty():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"dict"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "dict")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Dict) )
    assert ( expression._values == None)


def test_assign_dict_one():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"dict"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.STRING, Position(), "one"),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "dict")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Dict) )
    values = expression._values
    assert ( isinstance(values[0], Pair))

    first = values[0]._first
    assert ( isinstance(first, String ))
    assert ( first._value == "one" )

    second = values[0]._second
    assert ( isinstance(second, Number ))
    assert ( second._value == 1 )

def test_assign_dict_two():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"dict"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.BRACE_OPENING, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.STRING, Position(), "one"),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.STRING, Position(), "two"),
        Token(TokenType.COMMA, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.BRACE_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "dict")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Dict) )

    values = expression._values
    assert ( isinstance(values[0], Pair))

    first = values[0]._first
    assert ( isinstance(first, String ))
    assert ( first._value == "one" )

    second = values[0]._second
    assert ( isinstance(second, Number ))
    assert ( second._value == 1 )

    assert ( isinstance(values[1], Pair))

    first = values[1]._first
    assert ( isinstance(first, String ))
    assert ( first._value == "two" )

    second = values[1]._second
    assert ( isinstance(second, Number ))
    assert ( second._value == 2 )


def test_assign_select():
    #source = SourceString("select = SELECT Key FROM dict;")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"select"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.SELECT, Position()),
        Token(TokenType.IDENTIFIER, Position(), "Key"),
        Token(TokenType.FROM, Position()),
        Token(TokenType.IDENTIFIER, Position(), "dict"),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )
    select_term = program._statements[0]._expression
    assert ( isinstance(select_term, SelectTerm ))

    assert ( isinstance(select_term._select_expression, Identifier))
    assert (select_term._select_expression._name == "Key")

    assert ( isinstance(select_term._from_expression, Identifier))
    assert (select_term._from_expression._name == "dict")


def test_assign_add_two():
    #source = SourceString("sum = 1 + 2;")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"sum"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.PLUS, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)

    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "sum")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, AddTerm) )
    assert ( expression._left_mult_term._value == 1)

    expression = program._statements[0]._expression
    assert ( isinstance(expression, AddTerm) )
    assert ( expression._right_mult_term._value == 2)


def test_assign_mult_div():
    #source = SourceString("result = 1 * 2 / 3;")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"result"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.ASTERISK, Position()),
        Token(TokenType.INT, Position(), 2),
        Token(TokenType.SLASH, Position()),
        Token(TokenType.INT, Position(), 3),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)

    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "result")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, DivTerm) )
    
    left = expression._left_signed_factor
    assert ( isinstance(left, MultTerm) )
    assert ( left._left_signed_factor._value == 1)
    assert ( left._right_signed_factor._value == 2)

    assert ( expression._right_signed_factor._value == 3)


def test_assign_comparison_equals():
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"result"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.EQUAL, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "result")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, EqualsTerm) )
    assert ( expression._left_additive_term._name == "x")
    assert ( expression._right_additive_term._value == 1)


def test_assign_comparison_less_or_equals():
    source = SourceString("result = x <= 1;")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"result"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "x"),
        Token(TokenType.LESS_OR_EQUAL, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "result")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, LessOrEqualTerm) )
    assert ( expression._left_additive_term._name == "x")
    assert ( expression._right_additive_term._value == 1)


def test_assign_fun_call():
    #source = SourceString(" a = b();")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "b"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Item) )
    assert (expression._parameters == None)


def test_assign_fun_call_dot():
    #source = SourceString(" a = b(1).c;")
    tokens = LexerMock([
        Token(TokenType.IDENTIFIER, Position(),"a"),
        Token(TokenType.ASSIGN, Position()),
        Token(TokenType.IDENTIFIER, Position(), "b"),
        Token(TokenType.BRACKET_OPENING, Position()),
        Token(TokenType.INT, Position(), 1),
        Token(TokenType.BRACKET_CLOSING, Position()),
        Token(TokenType.DOT, Position()),
        Token(TokenType.IDENTIFIER, Position(), "c"),
        Token(TokenType.SEMICOLON, Position()),
        Token(TokenType.END_OF_TEXT, Position())
        ])
    parser = Parser(tokens)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, ObjectAccess) )
    assert (expression._right_item._name == "c")
