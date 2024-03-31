from token_types import TokenType

OPERATORS = {
    "<" : TokenType.LESS,
    ">" : TokenType.MORE,
    "<=" : TokenType.LESS_OR_EQUAL,
    ">=" : TokenType.MORE_OR_EQUAL,
    "==" : TokenType.EQUAL,

    "=" : TokenType.ASSIGN,

    "+" : TokenType.PLUS,
    "-" : TokenType.MINUS,
    "*" : TokenType.ASTERISK,
    "/" : TokenType.SLASH,

    "." : TokenType.DOT,
    "," : TokenType.COMMA,
    ";" : TokenType.SEMICOLON,

    "(" : TokenType.BRACKET_OPENING,
    ")" : TokenType.BRACKET_CLOSING,
    "[" : TokenType.SQUARE_BRACKET_OPENING,
    "]" : TokenType.SQUARE_BRACKET_CLOSING,
    "{" : TokenType.BRACE_OPENING,
    "}" : TokenType.BRACE_CLOSING
}