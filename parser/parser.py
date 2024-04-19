from lexer.filter import Filter
from lexer.lexer import Lexer
from lexer.tokens import Token, TokenType
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    IfStatement,
    OrTerm,
    AndTerm,
    NotTerm,
    ComparisonTerm,
    AdditiveTerm,
    MultTerm,
    SignedFactor,
    Number,
    ObjectAccess,
    Item,
    Identifier,
    Assignment
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
            raise SyntaxError(f"Must be {token_type}")
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

    # while_loop_statement ::== 'while' '(' expression ')' 'block;
    def parse_while_statement(self):
        if self._token.get_token_type() != TokenType.WHILE:
            return None
        
        position = self._token.get_position()
        self._token = self._lexer.get_next_token()

        self.must_be(TokenType.BRACKET_OPENING, SyntaxError)
        
        expression = self.parse_expression()
        if expression is None:
            raise SyntaxError
        
        self.must_be(TokenType.BRACKET_CLOSING, SyntaxError)
        
        block = self.parse_block()
        if block is None:
            raise SyntaxError
        
        return WhileStatement(expression, block, position)

    def parse_fun_def_statement(self):
        pass

    def parse_return_statement(self):
        pass

    # assign_or_call  ::== object_access ['=' expression] ‘;’ ;
    def parse_assign_or_call_statement(self):
        object_access = self.parse_object_access()
        

        statement = self.parse_fun_call(object_access)
        if statement:
            pass
        else:
            statement = self.parse_assignment(object_access)

        # self.must_be(TokenType.SEMICOLON, SyntaxError)
        return statement


    def parse_fun_call(self, name):
        pass

    # assign_or_call  ::== object_access ['=' expression] ‘;’ ;

    def parse_assignment(self, object_access):
        position = self._token.get_position()
        # object_access = self.parse_object_access()

        if self._token.get_token_type() != TokenType.ASSIGN:
            return None
        

        self._token = self._lexer.get_next_token() 

        expression = self.parse_expression()

        if expression is None:
            raise SyntaxError("After assign must be expression")
        
        return Assignment(object_access, expression, position)

        # to do later
        return object_access


    def parse_object_access(self):
        left_item = self.parse_item()

        if left_item is None:
            return None # ?? maybe it should be error?
        
        while (self._token.get_token_type() == TokenType.DOT):
            position = self._token.get_position()
            self._token = self._lexer.get_next_token()

            right_item = self.parse_item()

            if right_item is None:
                raise SyntaxError
            
            left_item = ObjectAccess(left_item, position, right_item)
        
        return left_item
    

    # item ::== identifier {  ‘[‘ expression ‘]’ |  ‘(‘ [arguments] ‘)’ }; 
    def parse_item(self):
        identifier = self.parse_identifier()
        # to do later
        return identifier


    def parse_identifier(self):

        if self._token.get_token_type() != TokenType.IDENTIFIER:
            return None
        
        position = self._token.get_position()

        name = self._token.get_value()

        self._token = self._lexer.get_next_token()

        
        return Identifier(name, position)


    def parse_if_statement(self):
        pass

    
    
    # expression ::== and_term { ‘Or’ and_term}
    def parse_expression(self):
        left_and_term = self.parse_and_term()

        if left_and_term is None:
            return None # ?? maybe it should be error?
        
        while (self._token.get_token_type() == TokenType.OR):
            position = self._token.get_position()
            self._token = self._lexer.get_next_token()

            right_and_term = self.parse_and_term()

            if right_and_term is None:
                raise SyntaxError
            
            left_and_term = OrTerm(left_and_term, position, right_and_term)
        
        return left_and_term
    
    # and_term ::== not_term { ‘And’ not_term};
    def parse_and_term(self):
        left_not_term = self.parse_not_term()

        if left_not_term is None:
            return None # ?? maybe it should be error?
        
        while (self._token.get_token_type() == TokenType.AND):
            position = self._token.get_position()
            self._token = self._lexer.get_next_token()

            right_not_term = self.parse_not_term()

            if right_not_term is None:
                raise SyntaxError
            
            left_not_term = AndTerm(left_not_term, position, right_not_term)
        
        return left_not_term
    

    # not_term 	   ::== [‘Not’] comparison_term;
    def parse_not_term(self):

        position = self._token.get_position()

        negation = False
        if (self._token.get_token_type() == TokenType.NOT):
            negation = True
            self._token = self._lexer.get_next_token()
        
        comparison_term = self.parse_comparison_term()
        
        if negation:
            if comparison_term is None:
                raise SyntaxError
            return NotTerm(comparison_term, position)
        return comparison_term
    
    # comparison_term ::== additive_term [('=='|'<'|'>'|'<='|'>=') additive_term];
    def parse_comparison_term(self):
        left_additive_term = self.parse_additive_term()

        if (self._token.get_token_type() in (TokenType.EQUAL,TokenType.LESS, TokenType.MORE, TokenType.LESS_OR_EQUAL, TokenType.MORE_OR_EQUAL)):
            self._token = self._lexer.get_next_token() 
            position = self._token.get_position()

            right_additive_term = self.parse_additive_term()


            if right_additive_term is None:
                raise SyntaxError("After comparison operator must be right additive term")
            
            left_additive_term = ComparisonTerm(left_additive_term, position, right_additive_term)
        
        return left_additive_term


    # additive_term   ::== mult_term {('+' | '-') mult_term};
    def parse_additive_term(self):
        left_mult_term = self.parse_mult_term()

        if (self._token.get_token_type() in (TokenType.PLUS, TokenType.MINUS)):
            self._token = self._lexer.get_next_token() 
            position = self._token.get_position()

            right_mult_term = self.parse_mult_term()


            if right_mult_term is None:
                raise SyntaxError
            
            left_mult_term = AdditiveTerm(left_mult_term, position, right_mult_term)
        
        return left_mult_term
    
    # mult_term ::== signed_factor {('*' | '/') signed_factor}
    def parse_mult_term(self):
        left_signed_factor = self.parse_signed_factor()

        if (self._token.get_token_type() in (TokenType.ASTERISK, TokenType.SLASH)):
            self._token = self._lexer.get_next_token() 
            position = self._token.get_position()

            right_signed_factor = self.parse_signed_factor()

            if right_signed_factor is None:
                raise SyntaxError
            
            left_signed_factor = MultTerm(left_signed_factor, position, right_signed_factor)
        
        return left_signed_factor

    # signed_factor   ::== [sign] factor ;
    def parse_signed_factor(self):
        position = self._token.get_position()

        unary_negation = False
        if (self._token.get_token_type() == TokenType.MINUS):
            unary_negation = True
            self._token = self._lexer.get_next_token()
        
        factor = self.parse_factor()

        if factor is None:
            raise SyntaxError
        
        if unary_negation:
            return SignedFactor(factor, position)
        return factor
        

    # factor ::== pair_or_expr | literal | list_def | dict_def |  select_term |  object_access;
    def parse_factor(self):
        position = self._token.get_position()

        factor = self.parse_literal() # i inne

        return factor
    
    
    # literal ::== number | bool | string;
    def parse_literal(self):
        position = self._token.get_position()

        literal = self.parse_number() # i inne

        return literal
    
    def parse_number(self):

        position = self._token.get_position()

        if (self._token.get_token_type() in (TokenType.INT, TokenType.FLOAT)):
            value = self._token.get_value()
            return Number(value, position)

        return None


    # block ::== '{' {statement} '}'
    def parse_block(self):
        pass



        

