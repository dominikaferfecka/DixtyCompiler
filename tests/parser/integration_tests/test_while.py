from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceString
from parser.syntax_tree import (
    WhileStatement,
    EqualsTerm,
    Number,
    Identifier,
    Assignment,
    Block
)

def test_while_identifier():
    source = SourceString("while (x) { a = 2; };")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], WhileStatement) )

    assert ( isinstance(program._statements[0]._expression, Identifier) )
    assert ( program._statements[0]._expression._name == "x" )

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


def test_while_identifier_equals():
    source = SourceString("while (x == 1) { a = 2; };")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], WhileStatement) )

    assert ( isinstance(program._statements[0]._expression, EqualsTerm) )

    left = program._statements[0]._expression._left_additive_term
    assert ( isinstance(left, Identifier) )
    assert ( left._name == "x" )

    right = program._statements[0]._expression._right_additive_term
    assert ( isinstance(right, Number) )
    assert ( right._value == 1 )

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