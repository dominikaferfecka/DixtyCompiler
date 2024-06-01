
from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceString
from interpreter.interpreter import Interpreter
from interpreter.builtins import BUILTINS
import pytest
from interpreter.errors import (
    VariableNotExists,
    FunctionNotDeclared,
    IncorrectArgumentsNumber,
    UnsupportedTypesToMakeOperation,
    CannotAddUnsupportedTypes,
    CannotSubUnsupportedTypes,
    CannotMultUnsupportedTypes,
    CannotDivUnsupportedTypes,
    CannotCompareUnsupportedTypes,
    CannotConvertType,
    CannotMakeNotOnNotBoolTypes,
    CannotMakeAndOnNotBoolTypes,
    CannotMakeOrOnNotBoolTypes,
    CannotDivByZero,
    RecursionLimitExceeded
)


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


def test_equal_string_int(setup_interpreter):
    with pytest.raises(CannotCompareUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" == 2;"))


def test_less_string_float(setup_interpreter):
    with pytest.raises(CannotCompareUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" < 2.0;"))


def test_less_int_float(setup_interpreter):
    with pytest.raises(CannotCompareUnsupportedTypes):
        setup_interpreter(SourceString("a = 1 < 2.0;"))


def test_add_int_float(setup_interpreter):
    with pytest.raises(CannotAddUnsupportedTypes):
        setup_interpreter(SourceString("a = 1 + 2.0;"))
    
def test_add_str_float(setup_interpreter):
    with pytest.raises(CannotAddUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" + 2.0;"))

def test_add_str_int(setup_interpreter):
    with pytest.raises(CannotAddUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" + 2;"))

def test_sub_int_float(setup_interpreter):
    with pytest.raises(CannotSubUnsupportedTypes):
        setup_interpreter(SourceString("a = 1 - 2.0;"))
    
def test_sub_str_float(setup_interpreter):
    with pytest.raises(CannotSubUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" - 2.0;"))

def test_sub_str_int(setup_interpreter):
    with pytest.raises(CannotSubUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" - 2;"))

def test_sub_str_str(setup_interpreter):
    with pytest.raises(CannotSubUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" - \"d\";"))

def test_mult_int_float(setup_interpreter):
    with pytest.raises(CannotMultUnsupportedTypes):
        setup_interpreter(SourceString("a = 1 * 2.0;"))
    
def test_mult_str_float(setup_interpreter):
    with pytest.raises(CannotMultUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" * 2.0;"))

def test_mult_str_int(setup_interpreter):
    with pytest.raises(CannotMultUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" * 2;"))

def test_mult_str_str(setup_interpreter):
    with pytest.raises(CannotMultUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" * \"d\";"))

def test_div_int_float(setup_interpreter):
    with pytest.raises(CannotDivUnsupportedTypes):
        setup_interpreter(SourceString("a = 1 / 2.0;"))
    
def test_div_str_float(setup_interpreter):
    with pytest.raises(CannotDivUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" / 2.0;"))

def test_div_str_int(setup_interpreter):
    with pytest.raises(CannotDivUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" / 2;"))

def test_div_str_str(setup_interpreter):
    with pytest.raises(CannotDivUnsupportedTypes):
        setup_interpreter(SourceString("a = \"abc\" / \"d\";"))

def test_div_by_zero_int(setup_interpreter):
    with pytest.raises(CannotDivByZero):
        setup_interpreter(SourceString("a = 2 / 0;"))

def test_div_by_zero_float(setup_interpreter):
    with pytest.raises(CannotDivByZero):
        setup_interpreter(SourceString("a = 2 / 0.0;"))

def test_div_by_zero_variable(setup_interpreter):
    with pytest.raises(CannotDivByZero):
        setup_interpreter(SourceString("b = 0; a = 2 / b;"))


def test_or_int_int(setup_interpreter):
    with pytest.raises(CannotMakeOrOnNotBoolTypes):
        setup_interpreter(SourceString("a = 1 Or 1;"))


def test_and_int_int(setup_interpreter):
    with pytest.raises(CannotMakeAndOnNotBoolTypes):
        setup_interpreter(SourceString("a = 1 And 1;"))


def test_not_int_int(setup_interpreter):
    with pytest.raises(CannotMakeNotOnNotBoolTypes):
        setup_interpreter(SourceString("a = Not 1;"))


def test_not_existing_variable(setup_interpreter):
    with pytest.raises(VariableNotExists):
        setup_interpreter(SourceString("print(a);"))


def test_not_existing_function(setup_interpreter):
    with pytest.raises(FunctionNotDeclared):
        setup_interpreter(SourceString("A();"))


def test_too_more_arguments_number(setup_interpreter):
    with pytest.raises(IncorrectArgumentsNumber):
        setup_interpreter(SourceString("fun A(){print(1);} A(2);"))


def test_too_less_arguments_number(setup_interpreter):
    with pytest.raises(IncorrectArgumentsNumber):
        setup_interpreter(SourceString("fun A(a, b){print(a); print(b);} A(1);"))


def test_for_string_empty(setup_interpreter, capsys):
    setup_interpreter(SourceString("text = \"\"; for element in text {print(element);}"))
    captured = capsys.readouterr()
    assert (captured.out == "")


def test_string_to_int(setup_interpreter):
    with pytest.raises(CannotConvertType):
        setup_interpreter(SourceString("a = \"x\"; a.ToInt();"))


def test_string_to_float(setup_interpreter):
    with pytest.raises(CannotConvertType):
        setup_interpreter(SourceString("a = \"x\"; a.ToFloat();"))


def test_int_to_int(setup_interpreter):
    with pytest.raises(CannotConvertType):
        setup_interpreter(SourceString("a = 1; a.ToInt();"))



def test_fun_endless_recursive(setup_interpreter):
    with pytest.raises(RecursionLimitExceeded):
        setup_interpreter(SourceString("fun sth(n) { sth(n); } sth(1);"))


# def test_none_statement(setup_interpreter, capsys):
#     setup_interpreter(SourceString("2+3;"))
#     captured = capsys.readouterr()
#     assert (captured.out == 'a')