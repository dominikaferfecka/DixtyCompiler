
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


def test_assign_number():
    # a = 2;
    nodes = [
        Assignment(
            Identifier("a",1), 
            Number(2, 3), 
            1
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : 2} )


def test_assign_float():
    # a = 2.0;
    nodes = [
        Assignment(
            Identifier("a",1), 
            Number(2.0, 3),
            1
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : 2.0} )
    

def test_assign_string():
    # a = "test";
    nodes = [Assignment(Identifier("a",1), String("test", 3), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : "test"} )


def test_assign_string_empty():
    # a = "";
    nodes = [Assignment(Identifier("a",1), String("", 3), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : ""} )


def test_assign_string_complicated():
    # a = "!@'/#\\\\*%\\";
    nodes = [Assignment(Identifier("a",1), String("!@'/#\\\\*%\\", 3), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : "!@'/#\\\\*%\\"} )


def test_assign_bool():
    # a = "True";
    nodes = [Assignment(Identifier("a",1), Bool("True", 3), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : "True"} )

# ARITHMETIC
def test_assign_arithmetic_add():
    # a = 3 + 2 + 1;
    nodes = [Assignment(Identifier("a",1), AddTerm(Number(3, 5), 5, AddTerm(Number(2,7), 7, Number(1, 9))), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : 6} )

def test_assign_arithmetic_sub():
    # a = 10 - 2 - 3;
    nodes = [Assignment(Identifier("a",1), SubTerm(SubTerm(Number(10, 5), 5, Number(2,7)), 5, Number(3, 9)), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : 5} )


def test_assign_arithmetic_times():
    # a = 10 * 2 * 3;
    nodes = [Assignment(Identifier("a",1), MultTerm(MultTerm(Number(10, 5), 5, Number(2,7)), 5, Number(3, 9)), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : 60} )

def test_assign_arithmetic_div():
    # a = 20 / 2 / 5;
    nodes = [Assignment(Identifier("a",1), DivTerm(DivTerm(Number(20, 5), 5, Number(2,7)), 5, Number(5, 9)), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : 2} )


def test_assign_add_strings():
    # a = "abc" + "def";
    nodes = [Assignment(Identifier("a",1), AddTerm(String("abc", 5), 5, String("def", 9)), 1)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : "abcdef"} )
    


# RZUTOWANIE
def test_assign_arithmetic_float_to_int():
    # b = 2.0; a = b.ToInt();
    nodes = [
        Assignment(
            Identifier("b", 1), 
            Number(2.0, 5), 
            3
        ), 
        Assignment(
            Identifier("a",1),
            ObjectAccess(
                Identifier("b", 5),
                5,
                FunCall(Identifier("ToInt", 5), 9, [])),
                1
            )
        ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'b' : 2.0} )
    interpreter.visit_assign_statement(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : 2, 'b' : 2.0} )


# COMPARISON
def test_assign_equal_term():
    # a = 2 == 2;
    nodes = [Assignment(Identifier("a",1), EqualsTerm(Number(2, 3), 3, Number(2, 6)), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : True} )
     

def test_assign_less_term():
    # a = 3 < 2;
    nodes = [Assignment(Identifier("a",1), LessTerm(Number(3, 3), 3, Number(2, 6)), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : False} )


def test_assign_more_term():
    # a = 3 > 2;
    nodes = [Assignment(Identifier("a",1), MoreTerm(Number(3, 3), 3, Number(2, 6)), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : True} )


def test_assign_less_or_equal_term():
    # a = 3 <= 2;
    nodes = [Assignment(Identifier("a",1), LessOrEqualTerm(Number(3, 3), 3, Number(2, 6)), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : False} )


def test_assign_more_or_equal_term():
    # a = 3 >= 2;
    nodes = [Assignment(Identifier("a",1), MoreOrEqualTerm(Number(3, 3), 3, Number(2, 6)), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : True} )


# Logical

def test_assign_comparison_or():
    # a = True Or False;
    nodes = [Assignment(Identifier("a",1), OrTerm(Bool(True, 3), 3, Bool(False, 6)), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : True} )


def test_assign_comparison_and():
    # a = True And False;
    nodes = [Assignment(Identifier("a",1), AndTerm(Bool(True, 3), 3, Bool(False, 6)), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : False} )


def test_assign_logical_not():
    # a = Not True;
    nodes = [Assignment(Identifier("a",1), NotTerm(Bool(True, 3), 3), 6)]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'a' : False} )

     


