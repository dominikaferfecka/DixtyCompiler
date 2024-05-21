
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
    print(f"printing {message}")

def length(interpreter, left):
    list = interpreter._current_context.get_scope_variable("list")
    interpreter._last_result = len(list)

def append_list(interpreter, object):
    value = interpreter._current_context.get_scope_variable("value")
    # list.append(value)
    print(f"value {value}")
    print(f"object {object._value}")
    # list.append(value)
    object._value.append(value)
    print(f"object changed: {object._value}")
    print("vvvv")

def remove_list(interpreter, object):
    index = interpreter._current_context.get_scope_variable("index")
    print(f"index {index}")
    print(f"object {object._value}")
    object._value.remove(index)

def insert_list(interpreter, object):
    value = interpreter._current_context.get_scope_variable("value")
    index = interpreter._current_context.get_scope_variable("index")
    print(f"value {value}")
    object._value.insert(index, value)

def contains_key(interpreter, dict):
    pass

def to_float():
    pass

def to_int():
    pass

def to_string():
    pass

BUILTINS = {
    "print" : FunEmbedded("print", ["message"], display),
    "len" : FunEmbedded("len", ["list"], length),
    "append" : FunEmbedded("append", ["value"], append_list),
    "remove" : FunEmbedded("remove", ["index"], remove_list),
    "insert" : FunEmbedded("insert", ["index", "value"], insert_list)
}




# fun = BUILTINS["print"]
# fun.run()