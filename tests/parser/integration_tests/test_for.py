from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceString
from parser.syntax_tree import (
    ForStatement,
    Number,
    Identifier,
    Assignment,
    String,
    List,
    Block
)

def test_for_in_identifier():
    source = SourceString("for i in list { a = 2; };")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], ForStatement) )

    assert ( isinstance(program._statements[0]._identifier, Identifier) )
    assert ( program._statements[0]._identifier._name == "i" )

    assert ( isinstance(program._statements[0]._expression, Identifier) )
    assert ( program._statements[0]._expression._name == "list" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)


def test_for_in_list():
    source = SourceString("for i in [1, 2, 3] { a = 2; };")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], ForStatement) )

    assert ( isinstance(program._statements[0]._identifier, Identifier) )
    assert ( program._statements[0]._identifier._name == "i" )

    assert ( isinstance(program._statements[0]._expression, List) )
    values = program._statements[0]._expression._values
    assert ( len(values) == 3 )
    assert ( values[0]._value == 1 )
    assert ( values[1]._value == 2 )
    assert ( values[2]._value == 3 )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)


def test_for_in_string():
    source = SourceString("for i in \"abc\" { a = 2; };")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], ForStatement) )

    assert ( isinstance(program._statements[0]._identifier, Identifier) )
    assert ( program._statements[0]._identifier._name == "i" )

    assert ( isinstance(program._statements[0]._expression, String) )
    values = program._statements[0]._expression._value
    assert ( len(values) == 3 )
    assert ( values[0] == "a" )
    assert ( values[1] == "b" )
    assert ( values[2] == "c" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)