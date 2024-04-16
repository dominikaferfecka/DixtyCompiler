from lexer import Lexer, TokenType


class Filter:
    def __init__(self, source, INT_LIMIT, STRING_LIMIT, IDENTIFIER_LIMIT):
        self._lexer = Lexer(source, INT_LIMIT, STRING_LIMIT, IDENTIFIER_LIMIT)

    def get_next_token(self):
        token = self._lexer.get_next_token()
        if token.get_token_type() != TokenType.COMMENT:
            return token
        else:
            return None
