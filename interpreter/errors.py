class VariableNotExists(Exception):
    def __init__(self, name):
        super().__init__(f'Tried to use not defined variable: [{name}]')


class FunctionNotDeclared(Exception):
    def __init__(self, name, position):
        super().__init__(f'Tried to use not defined function: [{name}] at {position}')


class FunctionAlreadyDeclared(Exception):
    def __init__(self, name, position):
        super().__init__(f'Tried to declare already existing function: [{name}] at {position}')


class IncorrectArgumentsNumber(Exception):
    def __init__(self, function_name, expected, received, position):
        super().__init__(f'Got incorrect number of parameters for function [{function_name}], expected: [{expected}], received: [{received}] - at {position}')
    

class UnsupportedTypesToMakeOperation(Exception):
    def __init__(self, left, right, operation, position):
        super().__init__(f'Cannot make operation [{operation}] on given types: [{left}] and [{right}], at [{position}]')


class CannotAddUnsupportedTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "adding", position)


class CannotSubUnsupportedTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "subtraction", position)


class CannotMultUnsupportedTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "multiplication", position)


class CannotDivUnsupportedTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "division", position)


class CannotCompareUnsupportedTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "comparison", position)


class AlreadyExistingDictKey(Exception):
    def __init__(self, name):
        super().__init__(f'Tried to add key to dict which already exists: [{name}]')


class NotExistingDictKey(Exception):
    def __init__(self, name):
        super().__init__(f'Tried to remove key which not exist in dict: [{name}]')


class CannotConvertType(Exception):
    def __init__(self, received, desired):
        super().__init__(f'Cannot convert from [{received}] to [{desired}]')