
from interpreter.errors import (
    AlreadyExistingDictKey,
    NotExistingDictKey,
    CannotConvertType,
    NotExistingListValue,
    AttributeError
)

class FunEmbedded:
    def __init__(self, name, parameters, action):
        super().__init__()
        self._name = name
        self._parameters = parameters
        self._action = action
    
    def accept(self, visitor, *args):
        visitor.visit_fun_embedded(self, *args)
    
def display(arguments_parsed):
    message = arguments_parsed[0]
    print(message)

def length(arguments_parsed, object):
    if not isinstance(object, list) and not isinstance(object, dict) and not isinstance(object, str):
        raise AttributeError("len", type(object))
    
    return len(object)

def append_list(arguments_parsed, object):
    if not isinstance(object, list):
        raise AttributeError("append_list", type(object))
    
    value = arguments_parsed[0]
    object.append(value)

def remove_list(arguments_parsed, object):
    if not isinstance(object, list):
        raise AttributeError("remove_list", type(object))
    
    value = arguments_parsed[0]
    if value not in object:
        raise NotExistingListValue(value)
    object.remove(value)

def insert_list(arguments_parsed, object):
    if not isinstance(object, list):
        raise AttributeError("insert_list", type(object))
    
    index = arguments_parsed[0]
    value = arguments_parsed[1]
    object.insert(index, value)

def contains_key(arguments_parsed, object):
    if not isinstance(object, dict):
        raise AttributeError("contains_key", type(object))
    
    value = arguments_parsed[0]
    return value in object.keys()


def add_item(arguments_parsed, object):
    if not isinstance(object, dict):
        raise AttributeError("add_item", type(object))
    
    key = arguments_parsed[0]
    value = arguments_parsed[1]
    
    if not key in object.keys():
        object[key] = value
    else:
        raise AlreadyExistingDictKey(key)

def remove_item(arguments_parsed, object):
    if not isinstance(object, dict):
        raise AttributeError("remove_item", type(object))

    key = arguments_parsed[0]
    
    if not key in object.keys():
        raise NotExistingDictKey(key)
    else:
        del object[key]

        
def to_float(arguments_parsed, value):

    if isinstance(value, int) or isinstance(value, str):
        try:
            return float(value)
        except ValueError as e:
            raise CannotConvertType(type(value), float) from e
    else:
        raise CannotConvertType(type(value), float)

def to_int(arguments_parsed, value):
    if isinstance(value, float) or isinstance(value, str):
        try:
            return int(value)
        except ValueError as e:
            raise CannotConvertType(type(value), str) from e
    else:
        raise CannotConvertType(type(value), int)

def to_string(arguments_parsed, value):
    if isinstance(value, int) or isinstance(value, float):
        try:
           return str(value)
        except ValueError as e:
            raise CannotConvertType(type(value), int) from e
    else:
        raise CannotConvertType(type(value), str)


BUILTINS = {
    "print" : FunEmbedded("print", ["message"], display),
    "len" : FunEmbedded("len", [], length),
    "append" : FunEmbedded("append", ["value"], append_list),
    "remove" : FunEmbedded("remove", ["value"], remove_list),
    "insert" : FunEmbedded("insert", ["index", "value"], insert_list),
    "contains_key" : FunEmbedded("contains_key", ["value"], contains_key),
    "add_item" : FunEmbedded("add_item", ["key", "value"], add_item),
    "remove_item" : FunEmbedded("remove_item", ["key"], remove_item),
    "ToFloat" : FunEmbedded("ToFloat", [], to_float),
    "ToInt" : FunEmbedded("ToInt", [], to_int),
    "ToString" : FunEmbedded("ToString", [], to_string)
}
