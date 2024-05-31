from interpreter.assign import IdentifierEvaulation, IndexAcccesEvaulation

class Scope:
    def __init__(self):
        self._variables = {}
    
    def get_variable(self, name):
        if not name in self._variables.keys():
            return None
        return self._variables[name]
    
    def set_nested_value(self, nested_list, indexes, value):
        current = nested_list
        for index in indexes[:-1]:
            current = current[index]
        current[indexes[-1]] = value

    def set_variable(self, object, value):
        if isinstance(object, IndexAcccesEvaulation):
            name = object._left_object._name
            if name in self._variables.keys():
                old_values = self._variables[name]
                indexes = object._index_access_list
                self.set_nested_value(old_values, indexes, value )

                value = old_values
            self._variables[name] = value
        if isinstance(object, str):
            self._variables[object] = value
        else:
            self._variables[object._name] = value



