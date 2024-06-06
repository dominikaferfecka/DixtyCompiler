
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


def test_if(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 2; if (a == 2) {print(\"two\");} else_if (a < 2) {print(\"less\");} else {print(\"more\");}"))
    captured = capsys.readouterr()
    assert (captured.out == "two\n")


def test_if_else_if(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; if (a == 2) {print(\"two\");} else_if (a < 2) {print(\"less\");} else {print(\"more\");}"))
    captured = capsys.readouterr()
    assert (captured.out == "less\n")


def test_if_else_only(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 3; if (a == 2) {print(\"two\");} else {print(\"more\");}"))
    captured = capsys.readouterr()
    assert (captured.out == "more\n")


def test_if_else_if_some(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 4; if (a == 2) {print(\"two\");} else_if (a == 3) {print(\"three\");} else_if (a == 4) {print(\"four\");}"))
    captured = capsys.readouterr()
    assert (captured.out == "four\n")
