
from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceString
from interpreter.interpreter import Interpreter
from interpreter.builtins import BUILTINS
import pytest

@pytest.fixture
def setup_interpreter():
    def _setup(source):
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()

        nodes = program._statements
        interpreter = Interpreter(program._functions, BUILTINS)
        for node in nodes:
            if node is not None:
                node.accept(interpreter)
    return _setup


def test_while_less(setup_interpreter, capsys):
    setup_interpreter(SourceString("i = 0; while (i < 3) { print(i); i = i +1; }"))
    captured = capsys.readouterr()
    assert (captured.out == "0\n1\n2\n")


def test_while_more(setup_interpreter, capsys):
    setup_interpreter(SourceString("i = 9; while (i >= 5) { print(i); i = i - 1; }"))
    captured = capsys.readouterr()
    assert (captured.out == "9\n8\n7\n6\n5\n")


def test_while_fun(setup_interpreter, capsys):
    setup_interpreter(SourceString("i = 0; fun check(x){if (x <= 2){return True;} else {return False;}  } while (check(i)) { print(i); i = i + 1; }"))
    captured = capsys.readouterr()
    assert (captured.out == "0\n1\n2\n")

# variable scopes
def test_while_iterator_outside(setup_interpreter, capsys):
    setup_interpreter(SourceString("i = 3; while (i > 0) {a = 2; i = i - 1;} print(i);"))
    captured = capsys.readouterr()
    assert (captured.out == "0\n")