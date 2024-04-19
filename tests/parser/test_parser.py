from parser.parser import Parser, Filter
from lexer.source import SourceString
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    IfStatement,
    OrTerm,
    AndTerm,
    NotTerm,
    ComparisonTerm,
    AdditiveTerm,
    MultTerm,
    SignedFactor,
    Number,
    ObjectAccess,
    Item,
    Identifier,
    Assignment,
    String,
    Bool
)

def test_assign_number():
    source = SourceString("a = 1;")
    filter = Filter(source)
    parser = Parser(filter)
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
    source = SourceString("float = 1.0;")
    filter = Filter(source)
    parser = Parser(filter)
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
    source = SourceString("text = \"a\";")
    filter = Filter(source)
    parser = Parser(filter)
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
    source = SourceString("bool = True;")
    filter = Filter(source)
    parser = Parser(filter)
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
    source = SourceString("bool = False;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "bool")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Bool) )
    assert ( expression._value == False)