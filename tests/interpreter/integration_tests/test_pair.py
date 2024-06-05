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


def test_print_pair(setup_interpreter, capsys):
    setup_interpreter(SourceString("pair = (\"value\", 2); print(pair[0]); print(pair[1]); print(pair);"))
    captured = capsys.readouterr()
    assert (captured.out == "value\n2\n('value', 2)\n")


def test_assign_pair_variables(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 3; text = \"some_text\"; pair = (a, text); print(pair);"))
    captured = capsys.readouterr()
    assert (captured.out == "(3, 'some_text')\n")
