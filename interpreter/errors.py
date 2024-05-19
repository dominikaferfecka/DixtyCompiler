class VariableNotExists(Exception):
    def __init__(self, name):
        super().__init__(f'Tried to use not defined variable: {name}')

