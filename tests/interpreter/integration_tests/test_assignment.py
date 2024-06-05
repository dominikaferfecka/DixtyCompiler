
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

def test_assign_number(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")

def test_assign_float(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2.0; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "2.0\n")

def test_assign_string(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=\"test\"; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "test\n")


def test_assign_string_empty(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=\"\"; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "\n")


def test_assign_string_complicated(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=\"!@'/#\\\\*%\\\"^ \"; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "!@'/#\\*%\"^ \n")


def test_assign_bool(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=True; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")

# ARITHMETIC
def test_assign_arithmetic_add(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 10 + 2 + 3 + 5; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "20\n")

def test_assign_arithmetic_sub(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 10 - 2 - 3 - 5; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "0\n")

def test_assign_arithmetic_times(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 10 * 2 * 3; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "60\n")

def test_assign_arithmetic_div(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 20 / 2 / 5; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")

def test_assign_arithmetic(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 10 + 2 + 3 + 5 - 8 - 2; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "10\n")

def test_assign_arithmetic_brackets(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = (2 * (3 + 3) - 6) / 3; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")

def test_assign_arithmetic_float(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 10.5 + 2.0 + 3.0 + 5.0 - 8.0 - 2.0; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "10.5\n")

def test_assign_add_strings(setup_interpreter, capsys):
    setup_interpreter(SourceString("a =  \"abc\" + \"123\"; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "abc123\n")


def test_assign_add_strings_variables(setup_interpreter, capsys):
    setup_interpreter(SourceString("b = \"!?\"; a =  \"abc\" + \"123\" + b; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "abc123!?\n")

# on variables
def test_assign_arithmetic_add_variables(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2; b=3; c=5; d=10; result = d - ((c - b) - a); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "10\n")

def test_assign_arithmetic_variables_float(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2.0; b=0.5; c=3.0; result = c + a - b; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "4.5\n")


# RZUTOWANIE
def test_assign_arithmetic_float_to_int(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2.5; b=1; result = a.ToInt() + b; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "3\n")

def test_assign_arithmetic_str_to_int(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=\"2\"; b=1; result = a.ToInt() + b; print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "3\n")

def test_assign_arithmetic_int_to_float(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2.5; b=1; result = a + b.ToFloat(); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "3.5\n")

def test_assign_arithmetic_str_to_float(setup_interpreter, capsys):
    setup_interpreter(SourceString("a=2.5; b=\"1\"; result = a + b.ToFloat(); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "3.5\n")

def test_assign_arithmetic_int_to_str(setup_interpreter, capsys):
    setup_interpreter(SourceString("b=1; c=\"text\"; result = c + b.ToString(); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "text1\n")

def test_assign_arithmetic_float_to_str(setup_interpreter, capsys):
    setup_interpreter(SourceString("b=1.0; c=\"text\"; result = c + b.ToString(); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "text1.0\n")


# COMPARISON
def test_assign_arithmetic_brackets(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 2 * 4 == 16 / 2; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


def test_assign_arithmetic_equals(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1 == 1; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


def test_assign_arithmetic_not_equals(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1 != 1; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "False\n")


def test_assign_arithmetic_less_equal(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = \"ab\"; c = a.len() <= 1 + 1; print(c);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


def test_assign_arithmetic_less(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = \"ab\"; c = a.len() < 1 + 1; print(c);"))
    captured = capsys.readouterr()
    assert (captured.out == "False\n")


def test_assign_arithmetic_less_equal(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = \"ab\"; c = a.len() <= 1 + 1; print(c);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


def test_assign_arithmetic_more(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = \"ab\"; c = a.len() > 1 + 1; print(c);"))
    captured = capsys.readouterr()
    assert (captured.out == "False\n")


def test_assign_arithmetic_more_equal(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = \"ab\"; c = a.len() >= 1 + 1; print(c);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


# Logical

def test_assign_comparison_or_and(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = True Or False == True And True; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")

def test_assign_comparison_or_and_false(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = False Or False == False And True; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


def test_assign_logical(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = True Or False And True; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "True\n")


def test_assign_logical_not(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = Not True Or False; print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "False\n")


