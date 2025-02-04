
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


def test_fun_zero_arguments(setup_interpreter, capsys):
    setup_interpreter(SourceString("x=2; fun display() { x = 2; print(x);} display();"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")

def test_fun_one_argument(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun display(x) { print(x);} display(1);"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n")

def test_fun_one_argument_variable(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun display(x) { print(x);} a = \"test\"; display(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "test\n")


def test_fun_two_arguments_variable(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun add_numbers(a, b){return a + b;} a = 2; b = 3; result = add_numbers(a,b); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "5\n")


def test_fun_four_arguments_variable(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun add_numbers(a, b, c, d){return a + b + c + d;} a = 2; b = 3; c=4; d=5; result = add_numbers(a,b,c,d); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "14\n")


# variables scope - by value
def test_fun_variables_scope(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun increase(x){x = x + 1; return x;} my_x = 2; new_x = increase(my_x); print(new_x); print(my_x);"))
    captured = capsys.readouterr()
    assert (captured.out == "3\n2\n")

# variables scope - same name
def test_fun_variables_scope(setup_interpreter, capsys):
    setup_interpreter(SourceString("a = 1; b = 2; c = 3; fun add_numbers(a, b) { c = 10; return a + b + c;} result = add_numbers(a, b); print(result); "))
    captured = capsys.readouterr()
    assert (captured.out == "13\n")

# recursive
def test_fun_recursive(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun factorial(n) { if (n == 0) { return 1; } else { return n * factorial( n - 1 );}} result = factorial(5); print(result);"))
    captured = capsys.readouterr()
    assert (captured.out == "120\n")


# return none
def test_fun_return_empty(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun increase(x){x = x + 1; return;} increase(1);"))
    captured = capsys.readouterr()
    assert (captured.out == "")

# variable scopes
def test_fun_outside(setup_interpreter, capsys):
    setup_interpreter(SourceString("x=2; fun change() { x = 3;} change(); print(x);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")


def test_fun_modify_list(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun run(x){x.append(4); return x;} a = [1, 2, 3]; run(a); print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 2, 3]\n")

# return
def test_fun_return_variable(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun run(x){x = x + 1; return x;} a = run(1); print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "2\n")


def test_fun_return_list(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun run(x){x.append(4); return x; print(\"NOT\");} a = run([1, 2, 3]); print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "[1, 2, 3, 4]\n")


def test_fun_return_nested_if(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun run(x){x = x + 1; if (1 == 1) { if (1 == 1) {return 1; print(\"NOT\");} print(\"NOT\");} print(\"NOT\");} a = run(1); print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n")


def test_fun_return_nested_while(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun run(x){i = 10; while (i > 0) {i = i - 1; return 1; print(i);} return 1;} a = run(1); print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n")


def test_fun_return_nested_while_some(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun run(x){i = 10; while (i > 0) { while (i > 0) {return 1; print(\"NOT\"); i = i - 1;} print(\"NOT\"); i = i - 1;} print(\"NOT\"); i = i - 1;} a = run(1); print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n")


def test_fun_return_nested_for(setup_interpreter, capsys):
    setup_interpreter(SourceString("fun run(x){for i in [1, 2, 3, 4] {print(1); return 1; print(i);} } a = run(1); print(a);"))
    captured = capsys.readouterr()
    assert (captured.out == "1\n1\n")
