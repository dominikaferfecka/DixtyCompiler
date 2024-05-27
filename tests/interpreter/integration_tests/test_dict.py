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


def test_assign_dict(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; print(dict[\"second_value\"]);"))
    captured = capsys.readouterr()
    assert (captured.out == "0.5\n")


def test_dict_add(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; dict.add(\"third_value\",3); print(dict[\"third_value\"]);"))
    captured = capsys.readouterr()
    assert (captured.out == "3\n")