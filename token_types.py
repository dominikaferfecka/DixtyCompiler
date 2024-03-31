from enum import Enum, auto

class TokenType(Enum):
    # keywords general
    FOR = auto()                        # for
    WHILE = auto()                      # while
    IF = auto()                         # if
    ELSE_IF = auto()                    # else_if
    ELSE = auto()                       # else
    IN = auto()                         # in
    FUN = auto()                        # fun
    RETURN = auto()                     # return
    
    #keywords LINQ
    SELECT = auto()                     # SELECT
    FROM = auto()                       # FROM
    WHERE = auto()                      # WHERE
    ORDER_BY = auto()                   # ORDER_BY
    ASC = auto()                        # ASC
    DESC = auto()                       # DESC

    # keywords value
    TRUE = auto()                       # True
    FALSE = auto()                      # False
    
    # logical operators
    AND = auto()                        # And
    OR = auto()                         # Or
    NOT = auto()                        # Not
    
    # operators
    PLUS = auto()                       # +
    MINUS = auto()                      # -
    ASTERISK = auto()                   # *
    SLASH = auto()                      # /
    DOT = auto()                        # .
    COMMA = auto()                      # ,
    SEMICOLON = auto()                  # ;
    ASSIGN = auto()                     # =

    # comparison operators
    LESS = auto()                       # <
    MORE = auto()                       # >
    LESS_OR_EQUAL = auto()              # <=
    MORE_OR_EQUAL = auto()              # >=
    EQUAL = auto()                      # ==
    # NOT_EQUAL = auto()                  # !=    

    # brackets
    BRACKET_OPENING = auto()            # (
    BRACKET_CLOSING = auto()            # )
    SQUARE_BRACKET_OPENING = auto()     # [
    SQUARE_BRACKET_CLOSING = auto()     # ]
    BRACE_OPENING = auto()              # {
    BRACE_CLOSING = auto()              # }

    # others
    IDENTIFIER  = auto()   
    END_OF_TEXT = auto()
    COMMENT     = auto()                # # tekst

    # const
    STRING      = auto()                # "tekst"
    INT         = auto()
    FLOAT       = auto()





