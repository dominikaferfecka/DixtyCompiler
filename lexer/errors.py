class IntLimitExceeded(Exception):
    def __init__(self, position, int_limit):
        super().__init__(f'Attempted to create integer bigger then maximum range [{int_limit}] \nInvalid integer position: {position}')
        self.position = position
        self.int_limit = int_limit


class StringLimitExceeded(Exception):
    def __init__(self, position, string_limit):
        super().__init__(f'Attempted to create string bigger then maximum range: [{string_limit}] \nInvalid string position: {position}')
        self.position = position
        self.string_limit = string_limit


class IdentifierLimitExceeded(Exception):
    def __init__(self, position, identifier_limit):
        super().__init__(f'Attempted to create identifier bigger then maximum range: [{identifier_limit}] \nInvalid identifier position: {position}')
        self.position = position
        self.identifier_limit = identifier_limit


class StringNotFinished(Exception):
    def __init__(self, position):
        super().__init__(f"Could not find closing \" to the opened string \n Not closed string position: {position}")
        self.position = position


class UnexpectedEscapeCharacter(Exception):
    def __init__(self, position, character):
        super().__init__(f"Invalid character [{character}] after escape sign. Expected character: 'n', 'r', 't', '\\' \nInvalid escape character position: {position}")
        self.position = position
        self.character = character


class TokenNotRecognized(Exception):
    def __init__(self, position, not_recognized):
        super().__init__(f"Token starting with character [{not_recognized}] was not recognized \nInvalid token position: {position}")
        self.position = position
        self.not_recognized = not_recognized


class NotFinishedOperator(Exception):
    def __init__(self, position, not_recognized):
        super().__init__(f"Operator != started but not finished, after '!' expected '=', received [{not_recognized}] \nInvalid token position: {position}")
        self.position = position
        self.not_recognized = not_recognized
