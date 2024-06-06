
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

def test_print_number(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")


# len
def test_len_str(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=\"abc\"; b = a.len(); print(b);"))
    captured = capsys.readouterr()
    assert (captured.out == "3\n")

def test_len_list(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=[1, 2, 3, 4, 5]; b = a.len(); print(b);"))
    captured = capsys.readouterr()
    assert (captured.out == "5\n")


def test_comment(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=1; #comment;"))
    captured = capsys.readouterr()
    assert (captured.out == "")

def test_empty(setup_interpreter, capsys):
    setup_interpreter(SourceString("  "))
    captured = capsys.readouterr()
    assert (captured.out == "")

def test_enter_after_statement(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2; \n"))
    captured = capsys.readouterr()
    assert (captured.out == "")

def test_enter(setup_interpreter, capsys):
    setup_interpreter(SourceString("\n"))
    captured = capsys.readouterr()
    assert (captured.out == "")


def test_two_enters(setup_interpreter, capsys):
    setup_interpreter(SourceString("\n\n"))
    captured = capsys.readouterr()
    assert (captured.out == "")