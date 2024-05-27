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


def test_print_dict(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; print(dict);"))
    captured = capsys.readouterr()
    assert (captured.out == "{'value': 2, 'second_value': 0.5}\n")


def test_dict_add(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; dict.add_item(\"third_value\",3); print(dict[\"third_value\"]);"))
    captured = capsys.readouterr()
    assert (captured.out == "3\n")



def test_dict_change_value(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; dict[\"second_value\"] = 5; print(dict[\"second_value\"]);"))
    captured = capsys.readouterr()
    assert (captured.out == "5\n")


def test_dict_remove(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; dict.remove_item(\"second_value\"); print(dict);"))
    captured = capsys.readouterr()
    assert (captured.out == "{'value': 2}\n")


def test_dict_contains_key(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; print(dict.contains_key(\"second_value\"));"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


def test_dict_not_contains_key(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; print(dict.contains_key(\"third_value\"));"))
    captured = capsys.readouterr()
    assert (captured.out == "False\n")


def test_dict_iteration(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"value\", 2), (\"second_value\", 0.5)}; for key in dict {print(key);}"))
    captured = capsys.readouterr()
    assert (captured.out == "value\nsecond_value\n")


# LINQ
# SELECT
def test_dict_select_key(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT Key FROM dict; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "['one', 'two', 'three']\n")


def test_dict_select_value(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT Value FROM dict; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 2, 3]\n")


def test_dict_select_key_value(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT (Key, Value) FROM dict; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[('one', 1), ('two', 2), ('three', 3)]\n")


def test_dict_select_value_changed(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT (Value + 1) FROM dict; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[2, 3, 4]\n")


def test_dict_select_value_function(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun increase(x){return x*2; } dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT (increase(Value)) FROM dict; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[2, 4, 6]\n")

# WHERE
def test_dict_where_more(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT Value FROM dict WHERE Value > 1; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[2, 3]\n")


def test_dict_where_function(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT Value FROM dict WHERE Key.len() == 3; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 2]\n")

# ORDER_BY

def test_dict_orderby_value_asc_where(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"three\", 3), (\"two\", 2)}; result = SELECT Value FROM dict WHERE Value == 3 ORDER_BY (Value) ASC; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[3]\n")


def test_dict_orderby_value_asc(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"three\", 3), (\"two\", 2)}; result = SELECT Value FROM dict ORDER_BY (Value) ASC; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 2, 3]\n")


def test_dict_orderby_value_desc(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"three\", 3), (\"two\", 2)}; result = SELECT Value FROM dict ORDER_BY (Value) DESC; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "[3, 2, 1]\n")


def test_dict_orderby_key_asc(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT Key FROM dict ORDER_BY (Key) ASC; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "['one', 'three', 'two']\n")


def test_dict_orderby_key_desc(setup_interpreter, capsys):
    setup_interpreter(SourceString("dict = {(\"one\", 1), (\"two\", 2), (\"three\", 3)}; result = SELECT Key FROM dict ORDER_BY (Key) DESC; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "['two', 'three', 'one']\n")