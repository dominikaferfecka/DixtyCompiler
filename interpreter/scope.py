from interpreter.assign import IdentifierEvaulation, IndexAcccesEvaulation

class Scope:
    def __init__(self, functions=None):
        self._variables = {}
        self._functions = functions
    
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
        # create or modify
        if not isinstance(object, IndexAcccesEvaulation):
            self._variables[object._name] = value
        else:
            name = object._left_object._name
            if name in self._variables.keys():
                old_values = self._variables[name]
                indexes = object._index_access_list
                self.set_nested_value(old_values, indexes, value )

                # for index in object._index_access_list:
                #     old_values[index] = value
                # # old_values[object._index_access_list] = value
                value = old_values
            self._variables[name] = value

        # if isinstance(name, IdentifierEvaulation):
        #     self._variables[name._name] = value
        # else:
        #     self._variables[name._name] = value

    def set_function(self):
        pass

    def get_function(self, name):
        print(name)
        if name in self._functions.keys():
            return self._functions[name]


