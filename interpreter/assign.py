class IdentifierEvaulation:
    def __init__(self, interpreter, object):
        self._interpreter = interpreter
        self._object = object
        self._name = object._name
        self._value = interpreter._current_context.get_scope_variable(object._name)

class IndexAcccesEvaulation:
    def __init__(self, interpreter, left_object, indexes):
        self._interpreter = interpreter
        self._name = left_object._name
        # if isinstance(left_object, IndexAcccesEvaulation):
        #     self._name = left_object._name
        self._left_object = left_object



        self._index_access_list = indexes
        left = interpreter.evaulate(left_object)
        # print(indexes)
        # print(left)
        if isinstance(left, list) or isinstance(left, tuple):
            self._value = left[indexes[-1]]
        else:
            key = [indexes[-1]]
            key = interpreter.evaulate(key[0])
            self._value = left[key]


        #         left = interpreter.evaulate_identifier(left)
        # self._value = left[index_access]
