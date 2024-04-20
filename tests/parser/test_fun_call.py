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
    Identifier,
    Assignment,
    String,
    Bool,
    List,
    Pair,
    Dict,
    Block,
    FunCall
)

def test_fun_call_non_args():
    source = SourceString("start();")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "start" )

    assert ( program._statements[0]._parameters == [] )


def test_fun_call_one_args():
    source = SourceString("display(x);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "display" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 1 )
    assert ( isinstance(parameters[0], Identifier))
    assert( parameters[0]._name == "x")


def test_fun_call_three_args():
    source = SourceString("add(x, y, z);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "add" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 3 )
    assert ( isinstance(parameters[0], Identifier))
    assert( parameters[0]._name == "x")
    
    assert ( isinstance(parameters[1], Identifier))
    assert( parameters[1]._name == "y")
    
    assert ( isinstance(parameters[2], Identifier))
    assert( parameters[2]._name == "z")


def test_fun_call_three_args_numbers():
    source = SourceString("add(0, 1, 1.0);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._name, Identifier) )
    assert ( program._statements[0]._name._name == "add" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 3 )
    assert ( isinstance(parameters[0], Number))
    assert( parameters[0]._value == 0)
    
    assert ( isinstance(parameters[1], Number))
    assert( parameters[1]._value == 1)
    
    assert ( isinstance(parameters[2], Number))
    assert( parameters[2]._value == 1.0)