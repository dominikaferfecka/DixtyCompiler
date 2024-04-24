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

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "start" )

    assert ( program._statements[0]._parameters == [] )


def test_fun_call_one_args():
    source = SourceString("display(x);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "display" )

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

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "add" )

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

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "add" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 3 )
    assert ( isinstance(parameters[0], Number))
    assert( parameters[0]._value == 0)
    
    assert ( isinstance(parameters[1], Number))
    assert( parameters[1]._value == 1)
    
    assert ( isinstance(parameters[2], Number))
    assert( parameters[2]._value == 1.0)


def test_fun_call_lists():
    source = SourceString("print(list[0][0][0]);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( isinstance(program._statements[0]._left, Identifier) )
    assert ( program._statements[0]._left._name == "print" )

    parameters = program._statements[0]._parameters
    assert ( len(parameters) == 1 )
    assert ( isinstance(parameters[0], Item))

    left = parameters[0]._left #list[0][0]
    assert( isinstance(left, Item) )
    assert( left._index_access._value == 0) 


def test_fun_call_two():
    source = SourceString("a()();")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    left = program._statements[0]._left # a()
    assert ( isinstance(left, FunCall) ) 
    assert ( left._left._name == "a" )


def test_fun_call_three_param():
    source = SourceString("a(1)(2)(3,4);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( program._statements[0]._parameters[0]._value == 3 )
    assert ( program._statements[0]._parameters[1]._value == 4 )

    left = program._statements[0]._left # a(1)(2)
    assert ( isinstance(left, FunCall) ) 


def test_fun_call_object_access():
    source = SourceString("print(pair.Key);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], FunCall) )

    assert ( program._statements[0]._left._name == "print" )
    parameters = program._statements[0]._parameters 

    assert ( isinstance(parameters[0], ObjectAccess) )
    assert ( parameters[0]._left_item._name == "pair" )
    assert ( parameters[0]._right_item._name == "Key" )
