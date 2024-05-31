
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


def test_assign_list( setup_interpreter):
    # a = [2, 4];
    nodes = [Assignment(Identifier("a",1), List([Number(2, 3), Number(4, 5)], 2), 1)]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : [2, 4]} )


def test_list_index_access( setup_interpreter):
    # a = [2, 4]; b = a[0];
    nodes = [Assignment(Identifier("a", 1), List([Number(2, 3), Number(4, 5)], 2), 1), Assignment(Identifier("b", 1), IndexAccess(Identifier("a", 1), 1, Number(0,1)), 2)]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : [2, 4], 'b' : 2} )


def test_list_append( setup_interpreter):
    # a = [2, 4]; a.append(5);
    nodes = [Assignment(Identifier("a",1), List([Number(2, 3), Number(4, 5)], 2), 1), ObjectAccess(Identifier("a", 1), 2, FunCall(Identifier("append", 1), 1, [Number(5, 6)] ) ) ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : [2, 4, 5]} )


def test_list_remove( setup_interpreter):
    # a = [2, 4]; a.remove(1);
    nodes = [Assignment(Identifier("a",1), List([Number(2, 3), Number(4, 5)], 2), 1), ObjectAccess(Identifier("a", 1), 2, FunCall(Identifier("remove", 1), 1, [Number(2, 6)] ) ) ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : [4]} )


def test_list_insert( setup_interpreter):
    # a = [2, 4]; a.insert(1, 5);
    nodes = [Assignment(Identifier("a",1), List([Number(2, 3), Number(4, 5)], 2), 1), ObjectAccess(Identifier("a", 1), 2, FunCall(Identifier("insert", 1), 1, [Number(1, 6), Number(5, 6)] ) ) ]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : [2, 5, 4]} )


def test_list_len( setup_interpreter):
    # a = [2, 4]; b = a.len();
    nodes = [Assignment(Identifier("a",1), List([Number(2, 3), Number(4, 5)], 2), 1), Assignment( Identifier("b", 1), ObjectAccess(Identifier("a", 1), 2, FunCall(Identifier("len", 1), 1, [] ) ), 1 )]
    interpreter = setup_interpreter(nodes)
    assert( interpreter._current_context._scopes[0]._variables == {'a' : [2, 4], 'b' : 2} )



