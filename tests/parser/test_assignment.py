from parser.parser import Parser, Filter
from lexer.source import SourceString
import sys
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    IfStatement,
    OrTerm,
    AndTerm,
    NotTerm,
    LessTerm,
    MoreTerm,
    EqualsTerm,
    LessOrEqualTerm,
    MoreOrEqualTerm,
    AddTerm,
    SubTerm,
    MultTerm,
    DivTerm,
    SignedFactor,
    Number,
    ObjectAccess,
    Item,
    IndexAccess,
    Identifier,
    Assignment,
    String,
    Bool,
    List,
    Pair,
    Dict,
    SelectTerm
)

def test_assign_number():
    source = SourceString("a = 1;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 1)


def test_assign_float():
    source = SourceString("float = 1.0;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "float")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Number) )
    assert ( expression._value == 1.0)


def test_assign_string():
    source = SourceString("text = \"a\";")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "text")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, String) )
    assert ( expression._value == "a")


def test_assign_bool_true():
    source = SourceString("bool = True;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "bool")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Bool) )
    assert ( expression._value == True)


def test_assign_bool_false():
    source = SourceString("bool = False;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()

    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "bool")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Bool) )
    assert ( expression._value == False)


def test_assign_list_empty():
    source = SourceString("list = [];")
    filter = Filter(source)
    parser = Parser(filter)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "list")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, List) )
    assert ( expression._values == [])


def test_assign_list_one_value():
    source = SourceString("list = [1];")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "list")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, List) )

    values = expression._values
    assert ( len(values) == 1)
    assert ( values[0]._value == 1)


def test_assign_list_three_values():
    source = SourceString("list = [1, 2, 3];")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "list")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, List) )

    values = expression._values
    assert ( len(values) == 3)
    assert ( values[0]._value == 1)
    assert ( values[1]._value == 2)
    assert ( values[2]._value == 3)


def test_assign_pair_empty():
    source = SourceString("pair = (1, 1);")
    filter = Filter(source)
    parser = Parser(filter)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "pair")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Pair) )
    # assert ( expression._first = 1 )
    # assert ( expression._second = 1 )


def test_assign_dict_empty():
    source = SourceString("dict = {};")
    filter = Filter(source)
    parser = Parser(filter)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "dict")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Dict) )
    assert ( expression._values == {})


def test_assign_dict_one():
    source = SourceString("dict = { (\"one\", 1)};" ) 
    filter = Filter(source)
    parser = Parser(filter)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "dict")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Dict) )
    values = expression._values
    assert ( isinstance(values[0], Pair))

    first = values[0]._first
    assert ( isinstance(first, String ))
    assert ( first._value == "one" )

    second = values[0]._second
    assert ( isinstance(second, Number ))
    assert ( second._value == 1 )

def test_assign_dict_two():
    source = SourceString("dict = { (\"one\", 1), (\"two\", 2)};" ) 
    filter = Filter(source)
    parser = Parser(filter)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "dict")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Dict) )

    values = expression._values
    assert ( isinstance(values[0], Pair))

    first = values[0]._first
    assert ( isinstance(first, String ))
    assert ( first._value == "one" )

    second = values[0]._second
    assert ( isinstance(second, Number ))
    assert ( second._value == 1 )

    assert ( isinstance(values[1], Pair))

    first = values[1]._first
    assert ( isinstance(first, String ))
    assert ( first._value == "two" )

    second = values[1]._second
    assert ( isinstance(second, Number ))
    assert ( second._value == 2 )


def test_assign_dict_complex():
    source = SourceString("dict = { (a, 1), (b, [1, 2]), (c, {(1,2)}) };" ) 
    filter = Filter(source)
    parser = Parser(filter)
    
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "dict")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Dict) )

    values = expression._values

    assert ( isinstance(values[0], Pair))
    first = values[0]._first
    assert ( isinstance(first, Identifier ))
    assert ( first._name == "a" )
    second = values[0]._second
    assert ( isinstance(second, Number ))
    assert ( second._value == 1 )

    assert ( isinstance(values[1], Pair))
    first = values[1]._first
    assert ( isinstance(first, Identifier ))
    assert ( first._name == "b" )
    second = values[1]._second
    values = second._values
    assert ( values[0]._value == 1 )
    assert ( values[1]._value == 2 )


def test_assign_select():
    source = SourceString("select = SELECT Key FROM dict;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )
    select_term = program._statements[0]._expression
    assert ( isinstance(select_term, SelectTerm ))

    assert ( isinstance(select_term._select_expression, Identifier))
    assert (select_term._select_expression._name == "Key")

    assert ( isinstance(select_term._from_expression, Identifier))
    assert (select_term._from_expression._name == "dict")


def test_assign_select_where():
    source = SourceString("select = SELECT Key FROM dict WHERE Value == 2;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )
    select_term = program._statements[0]._expression
    assert ( isinstance(select_term, SelectTerm ))

    assert ( isinstance(select_term._select_expression, Identifier))
    assert (select_term._select_expression._name == "Key")

    assert ( isinstance(select_term._from_expression, Identifier))
    assert (select_term._from_expression._name == "dict")

    assert ( isinstance(select_term._where_expression, EqualsTerm))

    left = select_term._where_expression._left_additive_term
    right = select_term._where_expression._right_additive_term
    assert (left._name == "Value")
    assert (right._value == 2)


def test_assign_select_where_order():
    source = SourceString("select = SELECT Key FROM dict WHERE Value == 2 ORDER_BY Key;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )
    select_term = program._statements[0]._expression
    assert ( isinstance(select_term, SelectTerm ))

    assert ( isinstance(select_term._select_expression, Identifier))
    assert (select_term._select_expression._name == "Key")

    assert ( isinstance(select_term._from_expression, Identifier))
    assert (select_term._from_expression._name == "dict")

    assert ( isinstance(select_term._where_expression, EqualsTerm))

    left = select_term._where_expression._left_additive_term
    right = select_term._where_expression._right_additive_term
    assert (left._name == "Value")
    assert (right._value == 2)

    assert ( isinstance(select_term._order_by_expression, Identifier))
    assert ( select_term._order_by_expression._name == "Key")
    assert ( select_term._asc_desc == "ASC")


def test_assign_select_where_order_DESC():
    source = SourceString("select = SELECT Key FROM dict WHERE Value == 2 ORDER_BY Key DESC;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )
    select_term = program._statements[0]._expression
    assert ( isinstance(select_term, SelectTerm ))

    assert ( isinstance(select_term._select_expression, Identifier))
    assert (select_term._select_expression._name == "Key")

    assert ( isinstance(select_term._from_expression, Identifier))
    assert (select_term._from_expression._name == "dict")

    assert ( isinstance(select_term._where_expression, EqualsTerm))

    left = select_term._where_expression._left_additive_term
    right = select_term._where_expression._right_additive_term
    assert (left._name == "Value")
    assert (right._value == 2)

    assert ( isinstance(select_term._order_by_expression, Identifier))
    assert ( select_term._order_by_expression._name == "Key")
    assert ( select_term._asc_desc == "DESC")


def test_assign_add_two():
    source = SourceString("sum = 1 + 2;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "sum")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, AddTerm) )
    assert ( expression._left_mult_term._value == 1)

    expression = program._statements[0]._expression
    assert ( isinstance(expression, AddTerm) )
    assert ( expression._right_mult_term._value == 2)


def test_assign_add_three():
    source = SourceString("sum = 1 + 2 + 3;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "sum")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, AddTerm) )
    
    left = expression._left_mult_term
    assert ( isinstance(left, AddTerm) )
    assert ( left._left_mult_term._value == 1)
    assert ( left._right_mult_term._value == 2)

    assert ( expression._right_mult_term._value == 3)


def test_assign_mult_div():
    source = SourceString("result = 1 * 2 / 3;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "result")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, DivTerm) )
    
    left = expression._left_signed_factor
    assert ( isinstance(left, MultTerm) )
    assert ( left._left_signed_factor._value == 1)
    assert ( left._right_signed_factor._value == 2)

    assert ( expression._right_signed_factor._value == 3)


def test_assign_add_mult_div():
    source = SourceString("result = 1 * 2 - 8 / 2;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "result")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, SubTerm) )
    
    left = expression._left_mult_term
    assert ( isinstance(left, MultTerm) )
    assert ( left._left_signed_factor._value == 1)
    assert ( left._right_signed_factor._value == 2)


    right = expression._right_mult_term
    assert ( isinstance(right, DivTerm) )
    assert ( right._left_signed_factor._value == 8)
    assert ( right._right_signed_factor._value == 2)


def test_assign_comparison_equals():
    source = SourceString("result = x == 1;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "result")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, EqualsTerm) )
    assert ( expression._left_additive_term._name == "x")
    assert ( expression._right_additive_term._value == 1)


def test_assign_comparison_less_or_equals():
    source = SourceString("result = x <= 1;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "result")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, LessOrEqualTerm) )
    assert ( expression._left_additive_term._name == "x")
    assert ( expression._right_additive_term._value == 1)


def test_assign_elements_lists():
    source = SourceString("sum = list[0][2][4];")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "sum")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, IndexAccess) )

    assert ( isinstance(expression._index_object, Number) )
    assert ( expression._index_object._value == 4 )

    left = expression._left # list[0][2]
    assert ( isinstance(left, Item) )

    left = left._left # list[0]
    assert ( isinstance(left, Item) )

    left = left._left # list
    assert ( isinstance(left, Identifier) )

    # elements = expression._elements
    # assert ( len(elements) == 3 )
    # assert ( elements[0]._value == 0 )
    # assert ( elements[1]._value == 2 )
    # assert ( elements[2]._value == 4 )



def test_assign_two_dimensions_list():
    source = SourceString("A = [ [1,2,3], [2,4,6] ];")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "A")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, List) )

    lists = expression._values
    assert ( len(lists) == 2 )

    values0 = lists[0]._values
    assert ( isinstance(values0[0], Number))
    assert ( values0[0]._value == 1 )

    values1 = lists[1]._values
    assert ( isinstance(values1[2], Number))
    assert ( values1[2]._value == 6 )

def test_assign_fun_call():
    source = SourceString(" a = b();")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Item) )
    assert (expression._parameters == None)


def test_assign_fun_call_param():
    source = SourceString(" a = b(1);")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, Item) )
    assert (expression._parameters[0]._value == 1)

def test_assign_fun_call_dot():
    source = SourceString(" a = b(1).c;")
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()
    assert ( len(program._statements) == 1 )
    assert ( isinstance(program._statements[0], Assignment) )

    object_access = program._statements[0]._object_access
    assert ( isinstance(object_access, Identifier) )
    assert ( object_access._name == "a")

    expression = program._statements[0]._expression
    assert ( isinstance(expression, ObjectAccess) )
    assert (expression._right_item._name == "c")
