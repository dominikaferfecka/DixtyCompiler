from lexer.token_types import TokenType

KEYWORDS = {
    # general
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
    "if": TokenType.IF,
    "else_if": TokenType.ELSE_IF,
    "else": TokenType.ELSE,
    "in": TokenType.IN,
    "fun": TokenType.FUN,
    "return": TokenType.RETURN,

    # LINQ
    "SELECT": TokenType.SELECT,
    "FROM": TokenType.FROM,
    "WHERE": TokenType.WHERE,
    "ORDER_BY": TokenType.ORDER_BY,
    "ASC": TokenType.ASC,
    "DESC": TokenType.DESC,

    # Value
    "True": TokenType.TRUE,
    "False": TokenType.FALSE,

    # Logical operators
    "And": TokenType.AND,
    "Or": TokenType.OR,
    "Not": TokenType.NOT
}
