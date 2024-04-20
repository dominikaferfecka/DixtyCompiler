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
    Bool,
    List,
    Pair,
    Dict,
    Block
)

def test_fun():
    source = SourceString("fun assign(x) { x = 2; }")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunStatement) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "assign" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 1 )
    assert ( isinstance(parameters[0], Identifier) )
    assert ( parameters[0]._name == "x" )

    block = program._statements[0]._block
    assert ( isinstance(block, Block) )
    assert ( len(block._statements) == 1 )
    assert ( isinstance(block._statements[0], Assignment) )

    object_access = block._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "x")

    expression = block._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 2)


