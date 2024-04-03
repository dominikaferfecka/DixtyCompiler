class IntLimitExceeded(Exception):
    def __init__(self, position):
        super().__init__(f'Attempted to create integer bigger then maximum range \n Too big integer attempted to create at {position}')

class StringLimitExceeded(Exception):
    def __init__(self, position):
        super().__init__(f'Attempted to create string bigger then maximum range \n Too big string attempted to create at {position}')

class IdentifierLimitExceeded(Exception):
    def __init__(self, position):
        super().__init__(f'Attempted to create identifier bigger then maximum range \n Too big identifier attempted to create at {position}')

class StringNotFinished(Exception):
    def __init__(self, position):
        super().__init__(f"Could not find closing \" to the opened string \n Error occured with opened string at {position}")

class TokenNotRecognized(Exception):
     def __init__(self, position):
        super().__init__(f"Token was not recognized \n Invalid token attempted to create at {position}")