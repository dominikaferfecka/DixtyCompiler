class LexerMock():
    def __init__(self, tokens):
        self._tokens = tokens
        self._iterator = 0

    def get_next_token(self):
        token = self._tokens[self._iterator]
        self._iterator += 1
        return token