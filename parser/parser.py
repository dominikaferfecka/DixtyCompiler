from lexer.filter import Filter
from lexer.lexer import Lexer
from lexer.tokens import Token, TokenType
from syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    IfStatement
)

class Parser:
    def __init__(self, lexer):
        if not isinstance(lexer, Lexer) and not isinstance(lexer, Filter):
            raise TypeError("Lexer have to be type Lexer or Filter")
        self._lexer = lexer
        self._token = self._lexer.get_next_token() # consume token
    
    # program :== {statement};     
    def parse_program(self) -> Program:
        statements = []
        while statement := self.parse_statement():
            statements.append(statement)
        
        return Program(statements)
    
    def must_be(self, token_type, exception):
        if (self._token.get_token_type() != token_type):
            raise exception
        value = self._token.get_value()

        self._token = self._lexer.get_next_token()

        return value

    # statement ::== for_loop_statement | while_loop_statement | fun_def_statement | return_statement | assign_or_call | if_statement;
    def parse_statement(self):
        position = self._token.get_position()
        statement = self.parse_for_statement() or self.parse_while_statement() or self.parse_fun_def_statement() or self.parse_return_statement() or self.parse_assign_or_call_statement() or self.parse_if_statement()
        return statement

    # for_loop_statement   ::== 'for' identifier 'in' expression block;
    def parse_for_statement(self):
        if self._token.get_token_type() != TokenType.FOR:
            return None
        position = self._token.get_position()
        self._token = self._lexer.get_next_token()

        identifier = self.must_be(TokenType.IDENTIFIER, SyntaxError)
        self.must_be(TokenType.IN, SyntaxError)

        expression = self.parse_expression()
        if expression is None:
            raise SyntaxError
        
        block = self.parse_block()
        if block is None:
            raise SyntaxError
        
        return ForStatement(identifier, expression, block, position)

    def parse_expression(self):
        pass

    def parse_block(self):
        pass

    def parse_while_statement(self):
        pass

    def parse_fun_def_statement(self):
        pass

    def parse_return_statement(self):
        pass

    def parse_assign_or_call_statement(self):
        pass

    def parse_if_statement(self):
        pass

        

