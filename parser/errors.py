class SemicolonMissing(Exception):
    def __init__(self, _, __, position):
        super().__init__(f'Missing semicolon after end of statement at position: {position}')
        self.position = position


class MissingExpectedStatement(Exception):
    def __init__(self, expected, received, position, extra_message=""):
        super().__init__(f'{extra_message}Expected token [{expected}], received token [{received}] at {position}')
        self.position = position
        self.expected = expected
        self.received = received


class InvalidFunctionDefinition(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidWhileLoop(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidForLoop(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidIfStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidElseIfStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidElseStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)
    

class InvalidReturnStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class InvalidAssignmentStatement(MissingExpectedStatement):
    def __init__(self, expected, received, position):
        super().__init__(expected, received, position)


class FunctionAlreadyExists(Exception):
    def __init__(self, name, position):
        super().__init__(f'Function with name [{name}] is already defined. Tried to define again at position: {position}')
        self.position = position
        self.name = name


class DictInvalidElement(Exception):
    def __init__(self, element, position):
        super().__init__(f'Elements in Dict must be Pair type. Object with invalid type {element} at {position}')
        self.position = position
        self.element = element


class UsedNotRecognizedStatement(Exception):
    def __init__(self, position):
        super().__init__(f'Not recognized statement detected at {position}')
        self.position = position
