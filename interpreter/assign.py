from interpreter.errors import VariableNotExists, NotExistingDictKey

class IdentifierEvaulation:
    def __init__(self, interpreter, object):
        self._interpreter = interpreter
        self._object = object
        self._name = object._name
        try:
            self._value = interpreter._current_context.get_scope_variable(object._name)
        except VariableNotExists: 
            self._value = None

class IndexAcccesEvaulation:
    def __init__(self, interpreter, left_object, indexes):
        self._interpreter = interpreter
        self._name = left_object._name
        self._left_object = left_object

        self._index_access_list = indexes
        left = interpreter.evaulate(left_object)
    
        if isinstance(left, list) or isinstance(left, tuple):
            self._value = left[indexes[-1]]
        else:
            key = [indexes[-1]]
            key = interpreter.evaulate(key[0])
            if isinstance (left, dict):
                if key not in left.keys():
                    raise NotExistingDictKey(key)
            self._value = left[key]

