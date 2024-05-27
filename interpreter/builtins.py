
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
    AlreadyExistingDictKey,
    NotExistingDictKey,
    CannotConvertType
)


class FunEmbedded:
    def __init__(self, name, parameters, action):
        super().__init__()
        self._name = name
        self._parameters = parameters
        self._action = action
    
    def run(self,  *args):
        self._action(*args)

    # def run(self, interpreter):
    #     self._action(interpreter)


def display(interpreter, left):
    message = interpreter._current_context.get_scope_variable("message")
    
    message = interpreter.evaulate(message)
    print(message)
    #print(f"#printing {message}")

def length(interpreter, object):
    list = interpreter.evaulate(object)
    interpreter._last_result = len(list)

def append_list(interpreter, object):
    value = interpreter._current_context.get_scope_variable("value")
    # list.append(value)
    #print(f"value {value}")
    #print(f"object {object._value}")
    # list.append(value)
    object._value.append(value)
    #print(f"object changed: {object._value}")
    #print("vvvv")

def remove_list(interpreter, object):
    index = interpreter._current_context.get_scope_variable("index")
    #print(f"index {index}")
    #print(f"object {object._value}")
    object._value.remove(index)

def insert_list(interpreter, object):
    value = interpreter._current_context.get_scope_variable("value")
    index = interpreter._current_context.get_scope_variable("index")
    #print(f"value {value}")
    object._value.insert(index, value)

def contains_key(interpreter, object):
    value = interpreter._current_context.get_scope_variable("value")
    #print(object._value.keys())
    if value in object._value.keys():
        interpreter._last_result = True
    else:
        interpreter._last_result = False

def add_item(interpreter, object):
    key = interpreter._current_context.get_scope_variable("key")
    value = interpreter._current_context.get_scope_variable("value")
    if not key in object._value.keys():
        object._value[key] = value
    else:
        raise AlreadyExistingDictKey(key)

def remove_item(interpreter, object):
    key = interpreter._current_context.get_scope_variable("key")
    if not key in object._value.keys():
        raise NotExistingDictKey(key)
    else:
        del object._value[key]

        

def to_float(interpreter, object):
    value = interpreter.evaulate(object)
    if isinstance(value, int) or isinstance(value, str):
        try:
            interpreter._last_result = float(value)
        except ValueError as e:
            raise CannotConvertType(type(value), float) from e
    else:
        raise CannotConvertType(type(value), float)

def to_int(interpreter, object):
    value = interpreter.evaulate(object)
    if isinstance(value, float) or isinstance(value, str):
        try:
            interpreter._last_result = int(value)
        except ValueError as e:
            raise CannotConvertType(type(value), str) from e
    else:
        raise CannotConvertType(type(value), int)

def to_string(interpreter, object):
    value = interpreter.evaulate(object)
    if isinstance(value, int) or isinstance(value, float):
        try:
            interpreter._last_result = str(value)
        except ValueError as e:
            raise CannotConvertType(type(value), int) from e
    else:
        raise CannotConvertType(type(value), str)

BUILTINS = {
    "print" : FunEmbedded("print", ["message"], display),
    "len" : FunEmbedded("len", [], length),
    "append" : FunEmbedded("append", ["value"], append_list),
    "remove" : FunEmbedded("remove", ["index"], remove_list),
    "insert" : FunEmbedded("insert", ["index", "value"], insert_list),
    "contains_key" : FunEmbedded("contains_key", ["value"], contains_key),
    "add_item" : FunEmbedded("add_item", ["key", "value"], add_item),
    "remove_item" : FunEmbedded("remove_item", ["key"], remove_item),
    "ToFloat" : FunEmbedded("ToFloat", [], to_float),
    "ToInt" : FunEmbedded("ToInt", [], to_int),
    "ToString" : FunEmbedded("ToString", [], to_string)
}




# fun = BUILTINS["#print"]
# fun.run()