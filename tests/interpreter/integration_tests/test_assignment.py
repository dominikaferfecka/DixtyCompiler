
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
        return interpreter
    return _setup

def test_assign_number(setup_interpreter, capsys):
    interpreter = setup_interpreter(SourceString("a=2; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")
    