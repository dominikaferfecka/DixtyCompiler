
from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceString
from interpreter.interpreter import Interpreter
from interpreter.builtins import BUILTINS
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    ReturnStatement,
    IfStatement,
    ElseIfStatement,
    ElseStatement,
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
    Block,
    FunCall,
    SelectTerm
)
import pytest


def test_assign_dict( ):
     # a = {("value", 1)};
    nodes = [Assignment(Identifier("a",1), Dict([Pair(String("value", 1), Number(1, 6), 1)], 1), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1} } )


def test_dict_add( ):
    # a = {("value", 1)}; a.add_item(("value2", 2))

    nodes = [
        Assignment(
            Identifier("a", 1), 
            Dict([Pair(String("value", 1), Number(1, 6), 1)], 1),
            1
        ),
        ObjectAccess(
            Identifier("a", 1),
            2,
            FunCall(Identifier("add_item", 1), 1, [String("value2", 1), Number(2, 6)] )
        )
        ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1} } )
    interpreter.visit_object_access(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1, "value2" : 2} } )



# def test_dict_change_value( ):
#     # a = {("value", 1)}; a["value"] =  2);
#     nodes = [Assignment(Identifier("a", 1), Dict([Pair(String("value", 1), Number(1, 6), 1)], 1), 1), Assignment(IndexAccess(Identifier("a", 1), Dict([Pair(String("value", 1), Number(1, 6), 1)], 1), 1)]
#     interpreter = setup_interpreter(nodes)
#     assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1} } )

    
#     setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; dict[\"second_value\"] = 5; print(dict[\"second_value\"]);"))
#     captured = capsys.readouterr()
#     assert (captured.out == "5\n")

def test_dict_remove():
    # a = {("value", 1)}; a.remove_item("value")
    nodes = [
        Assignment(
            Identifier("a", 1),
            Dict([Pair(String("value", 1), Number(1, 6), 1)], 1), 
            1
        ),
        ObjectAccess(
            Identifier("a", 1),
            2,
            FunCall(Identifier("remove_item", 1), 1, [String("value", 1)] ) 
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1} } )
    interpreter.visit_object_access(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {} } )


def test_dict_contains_key( ):
    # a = {("value", 1)}; b = a.contains_key("value");
    nodes = [
        Assignment(
            Identifier("a", 1),
            Dict([Pair(String("value", 1), Number(1, 6), 1)], 1),
            1
        ), 
        Assignment(
            Identifier("b",1),
            ObjectAccess(
                Identifier("a", 1),
                2,
                FunCall(Identifier("contains_key", 1), 1, [String("value", 1)] )
            ), 
            1
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1} } )
    interpreter.visit_assign_statement(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1}, 'b' : True } )


def test_dict_not_contains_key( ):
    # a = {("value", 1)}; b = a.contains_key("value");
    nodes = [
        Assignment(
            Identifier("a", 1), 
            Dict([Pair(String("value", 1), Number(1, 6), 1)], 1), 
            1
        ), 
        Assignment(
            Identifier("b",1), 
            ObjectAccess(
                Identifier("a", 1),
                2,
                FunCall(Identifier("contains_key", 1), 1, [String("value2", 1)] ) ),
                1
            )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1} } )
    interpreter.visit_assign_statement(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : {"value" : 1}, 'b' : False } )


