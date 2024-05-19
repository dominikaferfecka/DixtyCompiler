from interpreter.scope import Scope

class Context:
    def __init__(self):
        self._scopes = [Scope()]
        self._nested = 0
        self._return_type = None
    
    def add_scope(self):
        self._scopes.append(Scope())
        self._nested += 1

    def remove_scope(self):
        self._scopes.pop()
        self._nested -= 1

    def get_scope_variable(self, name):
        for scope in reversed(self._scopes):
            variable = scope.get_variable(name)
            if variable is not None:
                break
        return variable

    def set_scope_variable(self, name, value):
        self._scopes[-1].set_variable(name, value)

    def get_scope_function(self):
        pass

    def set_scope_function(self):
        pass