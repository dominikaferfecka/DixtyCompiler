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

@pytest.fixture
def setup_interpreter():
    def _setup(nodes):
        interpreter = Interpreter({}, BUILTINS)
        for node in nodes:
            node.accept(interpreter)
        return interpreter
    return _setup


def test_for_list(setup_interpreter):
    # for element in [1, 2, 3, 4] {print(element);}
    nodes = [
        ForStatement(
            Identifier("element", 1),
            List([Number(1, 1), Number(2, 1), Number(3, 1), Number(4, 1)], 1),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("element", 1)])],
                1
            ),
            1
        )
    ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'element' : 4} )


def test_for_list_variable(setup_interpreter):
    # list = [1, 2, 3, 4]; for element in list {print(element);}
    nodes = [
        Assignment(Identifier("list",1), List([Number(1, 1), Number(2, 1), Number(3, 1), Number(4, 1)], 1), 1),
        ForStatement(
            Identifier("element", 1),
            Identifier("list", 1),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("element", 1)])],
                1
            ),
            1
        )
    ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'element' : 4, 'list' : [1, 2, 3, 4]} )



def test_for_list_empty(setup_interpreter):
    # list = []; for element in list {print(element);}
    nodes = [
        Assignment(Identifier("list",1), List([], 1), 1),
        ForStatement(
            Identifier("element", 1),
            Identifier("list", 1),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("element", 1)])],
                1
            ),
            1
        )
    ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'list' : []} )


def test_for_string(setup_interpreter):
    # for element in \"abcd\" {print(element);}
    nodes = [
        ForStatement(
            Identifier("element", 1),
            String("abcd", 1),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("element", 1)])],
                1
            ),
            1
        )
    ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'element' : 'd'} )


def test_for_string_variable(setup_interpreter):
    # text = \"abcd\"; for element in text {print(element);}
    nodes = [
        Assignment(Identifier("text",1), String("abcd", 1), 1),
        ForStatement(
            Identifier("element", 1),
            Identifier("text", 1),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("element", 1)])],
                1
            ),
            1
        )
    ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'element' : 'd', 'text' : 'abcd'} )


def test_for_dict(setup_interpreter):
    # for element in {(\"one\",1),(\"two\",2)} {print(element);}
    nodes = [
        ForStatement(
            Identifier("element", 1),
            Dict([ Pair(String("one", 1), Number(1, 1), 1), Pair(String("two", 2), Number(2, 2), 1)], 1),
            Block(
                [FunCall(Identifier("print", 1), 1, [Identifier("element", 1)])],
                1
            ),
            1
        )
    ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'element' : 'two'} )

