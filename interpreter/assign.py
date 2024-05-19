class IdentifierEvaulation:
    def __init__(self, interpreter, object):
        self._interpreter = interpreter
        self._object = object
        self._name = object._name
        self._value = interpreter._current_context.get_scope_variable(object._name)

class IndexAcccesEvaulation:
    def __init__(self, interpreter, left_object, index_access):
        self._interpreter = interpreter
        self._left_object = left_object
        self._index_access = index_access
        left = interpreter.evaulate(left_object)
        print(left)
        self._value = left[index_access]


        #         left = interpreter.evaulate_identifier(left)
        # self._value = left[index_access]
