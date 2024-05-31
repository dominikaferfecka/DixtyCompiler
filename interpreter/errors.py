class VariableNotExists(Exception):
    def __init__(self, name, position=None):
        super().__init__(f'Tried to use not defined variable: [{name}] at [{position}]')
        self._name = name
        self._postion = position


class FunctionNotDeclared(Exception):
    def __init__(self, name, position):
        super().__init__(f'Tried to use not defined function: [{name}] at {position}')
        self._name = name
        self._postion = position


class FunctionAlreadyDeclared(Exception):
    def __init__(self, name, position):
        super().__init__(f'Tried to declare already existing function: [{name}] at {position}')
        self._name = name
        self._postion = position


class IncorrectArgumentsNumber(Exception):
    def __init__(self, function_name, expected, received, position):
        super().__init__(f'Got incorrect number of parameters for function [{function_name}], expected: [{expected}], received: [{received}] - at {position}')
        self._function_name = function_name
        self._expected = expected
        self._received = received
        self._position = position

class UnsupportedTypesToMakeOperation(Exception):
    def __init__(self, left, right, operation, position):
        super().__init__(f'Cannot make operation [{operation}] on given types: [{left}] and [{right}], at [{position}]')
        self._left = left
        self._right = right
        self._operation = operation
        self._positon = position


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


class CannotDivByZero(Exception):
    def __init__(self, position):
        super().__init__(f'Tried to divied by zero at: [{position}]')
        self._positon = position

class CannotCompareUnsupportedTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "comparison", position)


class CannotMakeOrOnNotBoolTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "or", position)


class CannotMakeAndOnNotBoolTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, right, position):
        super().__init__(left, right, "and", position)


class CannotMakeNotOnNotBoolTypes(UnsupportedTypesToMakeOperation):
    def __init__(self, left, position):
        super().__init__(left, "", "not", position)


class AlreadyExistingDictKey(Exception):
    def __init__(self, name):
        super().__init__(f'Tried to add key to dict which already exists: [{name}]')
        self._name = name


class NotExistingDictKey(Exception):
    def __init__(self, name):
        super().__init__(f'Tried to remove key which not exist in dict: [{name}]')
        self._name = name

class CannotConvertType(Exception):
    def __init__(self, received, desired):
        super().__init__(f'Cannot convert from [{received}] to [{desired}]')
        self._received = received
        self._desired = desired

class RecursionLimitExceeded(Exception):
    def __init__(self, recursion_limit):
        super().__init__(f'Exceeded recursion max limit [{recursion_limit}]')
        self._recursion_limit = recursion_limit