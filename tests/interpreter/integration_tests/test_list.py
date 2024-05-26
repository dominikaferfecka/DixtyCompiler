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

def test_assign_list(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 3; b = 5; text = \"some_text\"; fun increase(a) {a = a + 1; return a;} list = [a, b, text, 1, increase(2)]; print(list);"))
    captured = capsys.readouterr()
    assert (captured.out == "[3, 5, 'some_text', 1, 3]\n")


def test_list_index_access(setup_interpreter, capsys):
    setup_interpreter(SourceString("list_int = [1, 2, 3, 4, 5]; print(list_int[1]);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")


def test_list_append(setup_interpreter, capsys):
    setup_interpreter(SourceString("list_int = [1, 2, 3, 4, 5]; list_int.append(6); print(list_int);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 2, 3, 4, 5, 6]\n")


def test_list_remove(setup_interpreter, capsys):
    setup_interpreter(SourceString("list_int = [1, 2, 3, 4, 5]; list_int.remove(2); print(list_int);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 3, 4, 5]\n")


def test_list_insert(setup_interpreter, capsys):
    setup_interpreter(SourceString("list_int = [1, 2, 3, 4, 5]; list_int.insert(3, 9); print(list_int);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 2, 3, 9, 4, 5]\n")


def test_list_len(setup_interpreter, capsys):
    setup_interpreter(SourceString("list_int = [1, 2, 3, 4, 5]; print(list_int.len());"))
    captured = capsys.readouterr()
    assert (captured.out == "5\n")


def test_list_iterating(setup_interpreter, capsys):
    setup_interpreter(SourceString("list_int = [1, 2, 3, 4, 5]; for i in list_int {print(i);}"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n2\n3\n4\n5\n")

# list in list

def test_list_in_list(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 5; my_list = [[a, 2, 3], [4, b, 6], [7, 8, 9]]; print(my_list[1]); print(my_list[0][1]);"))
    captured = capsys.readouterr()
    assert (captured.out == "[4, 5, 6]\n2\n")

def test_list_in_list_append(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 5; my_list = [[a, 2, 3], [4, b, 6], [7, 8, 9]]; my_list[0].append(1); print(my_list);"))
    captured = capsys.readouterr()
    assert (captured.out == "[[1, 2, 3, 1], [4, 5, 6], [7, 8, 9]]\n")


def test_list_in_list_append_list(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 5; my_list = [[a, 2, 3], [4, b, 6], [7, 8, 9]]; my_list.append([9, 8, 7]); print(my_list);"))
    captured = capsys.readouterr()
    assert (captured.out == "[[1, 2, 3], [4, 5, 6], [7, 8, 9], [9, 8, 7]]\n")


def test_list_in_list_append_remove(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 5; my_list = [[a, 2, 3], [4, b, 6], [7, 8, 9]]; my_list[0].remove(1); print(my_list);"))
    captured = capsys.readouterr()
    assert (captured.out == "[[2, 3], [4, 5, 6], [7, 8, 9]]\n")


def test_list_in_list_len(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 5; my_list = [[a, 2, 3], [4, b, 6], [7, 8, 9]]; print(my_list.len());"))
    captured = capsys.readouterr()
    assert (captured.out == "3\n")


def test_list_in_list_iteration(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 5; my_list = [[a, 2, 3], [4, b, 6], [7, 8, 9]]; for list in my_list {for element in list { print(element);}}"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n2\n3\n4\n5\n6\n7\n8\n9\n")

def test_list_in_list_index_access(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 5; my_list = [[a, 2, 3], [4, b, 6], [7, 8, 9]]; print(my_list[0][0]);"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n")
