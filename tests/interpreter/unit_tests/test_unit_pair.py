
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


def test_assign_pair(setup_interpreter, capsys):
    # a = (2, 1);
    nodes = [Assignment(Identifier("a",1), Pair(Number(2, 1), Number(1, 1), 1), 1)]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : (2, 1)} )


def test_assign_pair_variables(setup_interpreter, capsys):
    # b = 2; c = "text"; a = (b, c);
    nodes = [Assignment(Identifier("b",1), Number(2, 3), 1), Assignment(Identifier("c",1), String("text", 3), 1), Assignment(Identifier("a",1), Pair(Identifier("b", 1), Identifier("c", 1), 1), 1)]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : (2, "text"), 'b' : 2, 'c' : "text"} )