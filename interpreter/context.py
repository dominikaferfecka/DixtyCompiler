from interpreter.scope import Scope
from interpreter.errors import VariableNotExists
import copy

class Context:
    def __init__(self, scopes=None):
        if scopes is None:
            self._scopes = [Scope()]
        else:
            self._scopes = scopes
            self._scopes = copy.deepcopy(scopes)
        self._nested = 0
        self._return_type = None
    
    def add_scope(self):
        self._scopes.append(Scope())
        self._nested += 1

    def remove_scope(self):
        if self._nested > 0:
            self._scopes.pop()
            self._nested -= 1        

    def get_scope_variable(self, name):
        for scope in reversed(self._scopes):
            variable = scope.get_variable(name)
            if variable is not None:
                break
        if variable is None:
            raise VariableNotExists(name)
        return variable

    def set_scope_variable(self, name, value):
        self._scopes[-1].set_variable(name, value)


