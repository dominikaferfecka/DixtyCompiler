
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


def test_while_less():
    # i = 0; while (i < 3) { print(i); i = i + 1; }
    nodes = [
        Assignment(Identifier("i",1), Number(0, 3), 1),
        WhileStatement(
            LessTerm(
                Identifier("i", 1), 1, Number(3, 1),
            ),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("i", 1)]),
                Assignment(Identifier("i", 1), AddTerm(Identifier("i",1), 1, Number(1, 1)), 1)
                ],
                1
            ),
            1
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 0} )
    interpreter.visit_while_statement(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 3} )


def test_while_less_equal():
    # i = 0; while (i <= 3) { print(i); i = i + 1; }
    nodes = [
        Assignment(Identifier("i",1), Number(0, 3), 1),
        WhileStatement(
            LessOrEqualTerm(
                Identifier("i", 1), 1, Number(3, 1),
            ),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("i", 1)]),
                Assignment(Identifier("i", 1), AddTerm(Identifier("i",1), 1, Number(1, 1)), 1)
                ],
                1
            ),
            1
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 0} )
    interpreter.visit_while_statement(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 4} )



def test_while_more():
    # i = 9; while (i > 5) { print(i); i = i - 1; }
    nodes = [
        Assignment(Identifier("i", 1), Number(9, 3), 1),
        WhileStatement(
            MoreTerm(
                Identifier("i", 1), 1, Number(5, 1),
            ),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("i", 1)]),
                Assignment(Identifier("i", 1), SubTerm(Identifier("i",1), 1, Number(1, 1)), 1)
                ],
                1
            ),
            1
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 9} )
    interpreter.visit_while_statement(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 5} )


def test_while_more_equal():
    # i = 9; while (i >= 5) { print(i); i = i - 1; }
    nodes = [
        Assignment(Identifier("i", 1), Number(9, 3), 1),
        WhileStatement(
            MoreOrEqualTerm(
                Identifier("i", 1), 1, Number(5, 1),
            ),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("i", 1)]),
                Assignment(Identifier("i", 1), SubTerm(Identifier("i",1), 1, Number(1, 1)), 1)
                ],
                1
            ),
            1
        )
    ]
    interpreter = Interpreter({}, BUILTINS)
    interpreter.visit_assign_statement(nodes[0])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 9} )
    interpreter.visit_while_statement(nodes[1])
    assert( interpreter._current_context._scopes[0]._variables == {'i' : 4} )

