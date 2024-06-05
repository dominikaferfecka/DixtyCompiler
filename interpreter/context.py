from interpreter.scope import Scope, IdentifierEvaulation
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
        # check if exists
        changed = False
        for idx, scope in enumerate(reversed(self._scopes)):
            if changed is False:
                if isinstance(name, IdentifierEvaulation):
                    variable = scope.get_variable(name._name)
                else:
                    variable = scope.get_variable(name)
                if variable is not None:
                    index = len(self._scopes) - idx - 1
                    self._scopes[index].set_variable(name, value)
                    changed = True
        if changed is False:
            self._scopes[-1].set_variable(name, value)


