
from interpreter.context import Context

class FunEmbedded:
    def __init__(self, name, parameters, action):
        super().__init__()
        self._name = name
        self._parameters = parameters
        self._action = action
    
    # def run(self,  *args, **kwargs):
    #     self._action(*args, **kwargs)

    def run(self, context):
        self._action(context)

def display(context):
    message = context.get_scope_variable("message")
    print(f"printing {message}")


BUILTINS = {
    "print" : FunEmbedded("print", ["message"], display)
}

# fun = BUILTINS["print"]
# fun.run()