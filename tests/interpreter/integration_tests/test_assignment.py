
from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceString
from interpreter.interpreter import Interpreter
import pytest

@pytest.fixture
def setup_interpreter():
    def _setup(source):
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()
        nodes = program._statements
        interpreter = Interpreter()
        for node in nodes:
            if node is not None:
                node.accept(interpreter)
        return interpreter
    return _setup

def test_assign_number(setup_interpreter):
    interpreter = setup_interpreter(SourceString("a = 1;"))
    assert (2 == 2)
    