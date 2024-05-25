
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


def test_for_list(setup_interpreter, capsys):
    setup_interpreter(SourceString("for element in [1, 2, 3, 4] {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n2\n3\n4\n")


def test_for_list_variable(setup_interpreter, capsys):
    setup_interpreter(SourceString("list = [1, 2, 3, 4]; for element in list {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n2\n3\n4\n")


def test_for_list_empty(setup_interpreter, capsys):
    setup_interpreter(SourceString("list = []; for element in list {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "")


def test_for_string(setup_interpreter, capsys):
    setup_interpreter(SourceString("for element in \"abcd\" {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "a\nb\nc\nd\n")


def test_for_string_variable(setup_interpreter, capsys):
    setup_interpreter(SourceString("text = \"abcd\"; for element in text {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "a\nb\nc\nd\n")


def test_for_string_empty(setup_interpreter, capsys):
    setup_interpreter(SourceString("text = ""; for element in text {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "")


def test_for_dict(setup_interpreter, capsys):
    setup_interpreter(SourceString("for element in {(\"one\",1),(\"two\",2)} {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "one\ntwo\n")


def test_for_dict_variable(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\",1),(\"two\",2)}; for element in dict {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "one\ntwo\n")


def test_for_dict_variable_items_tuple(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\",1)}; for element in dict {print((element, dict[element]));}"))
    captured = capsys.readouterr()
    assert (captured.out == "(one,1)\n(two,2)\n")


def test_for_dict_variable_items(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\",1),(\"two\",2)}; for element in dict {print(element); print(dict[element]); }"))
    captured = capsys.readouterr()
    assert (captured.out == "one\n1\ntwo\n2\n")