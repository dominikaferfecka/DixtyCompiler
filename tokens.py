from token_types import TokenType
from keywords import KEYWORDS
from position import Position

class Token:
    def __init__(self, token_type, position, value=None):
        if isinstance(token_type, TokenType):
            self._token_type = token_type
        else:
            raise ValueError("Invalid token type. Must be from TokenType enum.")
        
        if isinstance(position, Position):
            self._position = position
        else:
            raise ValueError("Invalid position type. Must be Position object.")
        
        if isinstance(value, str) or isinstance(value, int) or value is None:
            self._value = value
        else:
            raise ValueError("Invalid token value. Must be string or int")
    
    def __str__(self):
        return f"TokenType: [ {self._token_type} ], position: [ {self._position} ], value: [ {self._value} ]"

position = Position()
token = Token(TokenType.IF, position)
print(token)

