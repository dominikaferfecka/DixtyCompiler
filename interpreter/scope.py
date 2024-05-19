from interpreter.errors import ( VariableNotExists)

class Scope:
    def __init__(self):
        self._variables = {}
        self._functions = {}
    
    def get_variable(self, name):
        if not name in self._variables.keys():
            raise VariableNotExists(name)
        return self._variables[name]

    def set_variable(self, name, value):
        # create or modify
        self._variables[name] = value

    def set_function(self):
        pass

    def get_function(self):
        pass


