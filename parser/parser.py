from lexer.filter import Filter
from lexer.lexer import Lexer
from lexer.tokens import Token, TokenType
import sys
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    ReturnStatement,
    IfStatement,
    ElseIfStatement,
    ElseStatement,
    OrTerm,
    AndTerm,
    NotTerm,
    LessTerm,
    MoreTerm,
    EqualsTerm,
    LessOrEqualTerm,
    MoreOrEqualTerm,
    AddTerm,
    SubTerm,
    MultTerm,
    DivTerm,
    SignedFactor,
    Number,
    ObjectAccess,
    Item,
    Identifier,
    Assignment,
    String,
    Bool,
    List,
    Pair,
    Dict,
    Block,
    FunCall,
    SelectTerm
)

from parser.errors import (
    SemicolonMissing,
    MissingExpectedStatement,
    InvalidFunctionDefinition,
    InvalidWhileLoop,
    InvalidForLoop,
    InvalidIfStatement,
    InvalidElseStatement,
    InvalidElseIfStatement,
    InvalidReturnStatement,
    InvalidAssignmentStatement,
    FunctionAlreadyExists
    )

class Parser:
    def __init__(self, lexer):
        if not isinstance(lexer, Lexer) and not isinstance(lexer, Filter):
            raise TypeError("Lexer have to be type Lexer or Filter")
        # sys.setrecursionlimit(10000)
        self._lexer = lexer
        self._token = self._lexer.get_next_token() # consume token
        self._functions = {}
    
    # program :== {statement};     
    def parse_program(self) -> Program:
        statements = []
        while statement := self.parse_statement():
            statements.append(statement)
        
        return Program(statements)
    
    def consume_token(self):
        self._token = self._lexer.get_next_token()
    
    def must_be(self, token_type, exception):
        if (self._token.get_token_type() != token_type):
            position = self._token.get_position()
            raise exception(token_type, self._token.get_token_type(), position)
        value = self._token.get_value()
        self._token = self._lexer.get_next_token()
        return value
    
    def not_none(self, element, exception, expected):
        received = self._token.get_token_type()
        position = self._token.get_position()
        if element is None:
            raise exception(expected, received, position)

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

        identifier = self.parse_identifier()
        self.not_none(identifier, InvalidForLoop, TokenType.IDENTIFIER)
        
        self.must_be(TokenType.IN, InvalidForLoop)

        expression = self.parse_expression()
        self.not_none(expression, InvalidForLoop, "Expression")
        
        block = self.parse_block()
        self.not_none(block, InvalidForLoop, "Loop block")
        
        return ForStatement(identifier, expression, block, position)

    # while_loop_statement ::== 'while' '(' expression ')' 'block;
    def parse_while_statement(self):
        if self._token.get_token_type() != TokenType.WHILE:
            return None
        
        position = self._token.get_position()
        self._token = self._lexer.get_next_token()

        self.must_be(TokenType.BRACKET_OPENING, InvalidWhileLoop)
        
        expression = self.parse_expression()
        self.not_none(expression, InvalidWhileLoop, "Expression")
        
        self.must_be(TokenType.BRACKET_CLOSING, InvalidWhileLoop)
        
        block = self.parse_block()
        self.not_none(block, InvalidWhileLoop, "Loop block")
       
        return WhileStatement(expression, block, position)

    # fun_def_statement   ::== 'fun' identifier '(' [ parameters ] ')' block;
    def parse_fun_def_statement(self):
        if self._token.get_token_type() != TokenType.FUN:
            return None

        position = self._token.get_position()
        self._token = self._lexer.get_next_token()

        name = self.parse_identifier()
        self.not_none(name, InvalidFunctionDefinition, TokenType.IDENTIFIER)
        # if name is None:
        #     raise InvalidFunctionDefinition(self._token.get_token_type(), TokenType.IDENTIFIER)
        
        self.must_be(TokenType.BRACKET_OPENING, InvalidFunctionDefinition)

        parameters = self.parse_parameters()

        self.must_be(TokenType.BRACKET_CLOSING, InvalidFunctionDefinition)

        block = self.parse_block()

        if name._name in self._functions.keys():
            raise FunctionAlreadyExists(name._name, position)
        
        fun = FunStatement(name, parameters, block, position)
        self._functions[name._name] = fun

        return fun



    # parameters ::== identifier {',' identifier}
    def parse_parameters(self):
        
        parameters = []
        position = self._token.get_position()
        identifier = self.parse_identifier()
        if identifier is None:
            return parameters
        parameters.append(identifier)
        
        while self._token.get_token_type() == TokenType.COMMA:
            self._token = self._lexer.get_next_token()
            identifier = self.parse_identifier()
            self.not_none(identifier, MissingExpectedStatement, TokenType.IDENTIFIER)
            parameters.append(identifier)

        return parameters

    def parse_return_statement(self):
        if self._token.get_token_type() != TokenType.RETURN:
            return None

        position = self._token.get_position()
        self._token = self._lexer.get_next_token()
        
        expression = self.parse_expression()
        self.not_none(expression, InvalidReturnStatement, "Expression")
        
        self.must_be(TokenType.SEMICOLON, SemicolonMissing)

        return ReturnStatement(expression, position)


    # assign_or_call  ::== object_access ['=' expression] ‘;’ ;
    def parse_assign_or_call_statement(self):

        identifier = self.parse_identifier()
        if identifier is None:
            return None
        
        statement = self.parse_fun_call(identifier)
        if statement:
            pass
        else:
            object_access = self.parse_object_access(identifier)
            statement = self.parse_assignment(object_access)
    
        return statement

    # call :: == identifier([parameters])’;’
    def parse_fun_call(self, identifier):
        # identifier = self.parse_identifier()

        if identifier is None:
            return None

        if self._token.get_token_type() != TokenType.BRACKET_OPENING:
            return None
        
        left = identifier
        while self._token.get_token_type() == TokenType.BRACKET_OPENING:
        
            position = self._token.get_position()
            self._token = self._lexer.get_next_token()

            parameters = self.parse_expressions_list()
            if parameters is None:
                parameters = []
            
            self.must_be(TokenType.BRACKET_CLOSING, MissingExpectedStatement)

            left = FunCall(left, parameters, position)

        self.must_be(TokenType.SEMICOLON, SemicolonMissing)

        return left



    # assign_or_call  ::== object_access ['=' expression] ‘;’ ;

    def parse_assignment(self, object_access):
        position = self._token.get_position()
        # object_access = self.parse_object_access()

        if self._token.get_token_type() != TokenType.ASSIGN:
            return None
        
        
        self._token = self._lexer.get_next_token() 

        expression = self.parse_expression()

        self.not_none(expression, InvalidAssignmentStatement, "Expression")
        # if expression is None:
        #     raise SyntaxError("After assign must be expression")
        
        self.must_be(TokenType.SEMICOLON, SemicolonMissing)
        
        return Assignment(object_access, expression, position)

    def parse_object_access_identifier(self):
        identifier = self.parse_identifier()
        if identifier is None:
            return None
        return self.parse_object_access(identifier)

    def parse_object_access(self, identifier):
        left_item = self.parse_item(identifier)

        if left_item is None:
            return None # ?? maybe it should be error?
        
        while (self._token.get_token_type() == TokenType.DOT):
            position = self._token.get_position()
            self._token = self._lexer.get_next_token()

            right_item = self.parse_item()

            self.not_none(right_item, MissingExpectedStatement, "right_item")

            
            left_item = ObjectAccess(left_item, position, right_item)
        
        return left_item
    

    # item ::== identifier {  ‘[‘ expression ‘]’ | ‘(‘ [arguments] ‘)’ }; 
    def parse_item(self, identifier=None):

        if identifier is None:
            identifier = self.parse_identifier()
        # return identifier
        # if identifier is None:
        #     return None

        position = self._token.get_position()

        token = self._token.get_token_type()
        elements = []
        # while token == TokenType.SQUARE_BRACKET_OPENING:
        #     self.consume_token()
    
        #     if token == TokenType.SQUARE_BRACKET_OPENING:
        #         expression = self.parse_expression()
        #         self.not_none(expression, MissingExpectedStatement, "Expression")
        #         self.must_be(TokenType.SQUARE_BRACKET_CLOSING, MissingExpectedStatement)
        #         elements.append(expression)
        #         token = self._token.get_token_type()
        left = identifier
        while token in (TokenType.SQUARE_BRACKET_OPENING, TokenType.BRACKET_OPENING):
            #self.consume_token()
    
            if token == TokenType.SQUARE_BRACKET_OPENING:
                self.consume_token()
                expression = self.parse_expression()
                self.not_none(expression, MissingExpectedStatement, "Expression")
                self.must_be(TokenType.SQUARE_BRACKET_CLOSING, MissingExpectedStatement)
                elements.append(expression)
                token = self._token.get_token_type()
                left = Item(left, expression, None, position)
            elif token == TokenType.BRACKET_OPENING:
                self.consume_token()
                parameters = self.parse_expressions_list()
                elements.append(parameters)
                self.must_be(TokenType.BRACKET_CLOSING, MissingExpectedStatement)
                token = self._token.get_token_type()
                left = Item(left, None, parameters, position)

        return left


    def parse_identifier(self):

        if self._token.get_token_type() != TokenType.IDENTIFIER:
            return None
        
        position = self._token.get_position()

        name = self._token.get_value()

        self._token = self._lexer.get_next_token()

        
        return Identifier(name, position)


    def parse_if_statement(self):
        if self._token.get_token_type() != TokenType.IF:
            return None
        position = self._token.get_position()
        self.consume_token()
        
        self.must_be(TokenType.BRACKET_OPENING, InvalidIfStatement)

        expression = self.parse_expression()
        self.not_none(expression, InvalidIfStatement, "Expression")

        self.must_be(TokenType.BRACKET_CLOSING, InvalidIfStatement)

        block = self.parse_block()
        self.not_none(expression, InvalidIfStatement, "If block")
        
        else_if_lists = []
        while else_if_statement := self.parse_else_if():
            else_if_lists.append(else_if_statement)
        
        else_statement = self.parse_else()

        return IfStatement(expression, block,  else_if_lists, else_statement, position)


    def parse_else_if(self):
        if self._token.get_token_type() != TokenType.ELSE_IF:
            return None
        position = self._token.get_position()
        self.consume_token()    

        self.must_be(TokenType.BRACKET_OPENING, InvalidElseIfStatement)

        expression = self.parse_expression()
        self.not_none(expression, InvalidElseIfStatement, "Expression")

        self.must_be(TokenType.BRACKET_CLOSING, InvalidElseIfStatement)

        block = self.parse_block()
        self.not_none(block, InvalidElseIfStatement, "Else if block")

        return ElseIfStatement(expression, block, position)
    

    def parse_else(self):
        if self._token.get_token_type() != TokenType.ELSE:
            return None
        position = self._token.get_position()
        self.consume_token()    

        block = self.parse_block()
        self.not_none(block, InvalidElseStatement, "Else block")

        return ElseStatement(block, position)

    
    # expression ::== and_term { ‘Or’ and_term}
    def parse_expression(self):
        left_and_term = self.parse_and_term()

        if left_and_term is None:
            return None # ?? maybe it should be error?
        
        while (self._token.get_token_type() == TokenType.OR):
            position = self._token.get_position()
            self._token = self._lexer.get_next_token()

            right_and_term = self.parse_and_term()

            self.not_none(right_and_term, MissingExpectedStatement, "Expression")

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

            self.not_none(right_not_term, MissingExpectedStatement, "Not term")
            
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
            self.not_none(comparison_term, MissingExpectedStatement, "Comparison term")
            return NotTerm(comparison_term, position)
        return comparison_term
    
    # comparison_term ::== additive_term [('=='|'<'|'>'|'<='|'>=') additive_term];
    def parse_comparison_term(self):
        left_additive_term = self.parse_additive_term()

        if (self._token.get_token_type() in (TokenType.EQUAL,TokenType.LESS, TokenType.MORE, TokenType.LESS_OR_EQUAL, TokenType.MORE_OR_EQUAL)):

            comparison = {
                TokenType.EQUAL : EqualsTerm,
                TokenType.LESS : LessTerm,
                TokenType.MORE : MoreTerm,
                TokenType.LESS_OR_EQUAL : LessOrEqualTerm,
                TokenType.MORE_OR_EQUAL : MoreOrEqualTerm
            }

            Class = comparison[self._token.get_token_type()]

            self._token = self._lexer.get_next_token() 
            position = self._token.get_position()

            right_additive_term = self.parse_additive_term()

            self.not_none(right_additive_term, MissingExpectedStatement, "right_additive_term")
            # raise SyntaxError("After comparison operator must be right additive term")
            
            left_additive_term = Class(left_additive_term, position, right_additive_term)
        
        return left_additive_term


    # additive_term   ::== mult_term {('+' | '-') mult_term};
    def parse_additive_term(self):
        left_mult_term = self.parse_mult_term()

        while self._token.get_token_type() in (TokenType.PLUS, TokenType.MINUS):
            operator = self._token.get_token_type() 
            
            self._token = self._lexer.get_next_token() 
            position = self._token.get_position()

            right_mult_term = self.parse_mult_term()

            self.not_none(right_mult_term, MissingExpectedStatement, "right_mult_term")
            
            if operator == TokenType.PLUS:
                left_mult_term = AddTerm(left_mult_term, position, right_mult_term)
            else:
                left_mult_term = SubTerm(left_mult_term, position, right_mult_term)
               
        return left_mult_term
    
    # mult_term ::== signed_factor {('*' | '/') signed_factor}
    def parse_mult_term(self):
        left_signed_factor = self.parse_signed_factor()

        while (self._token.get_token_type() in (TokenType.ASTERISK, TokenType.SLASH)):
            operator = self._token.get_token_type() 

            self._token = self._lexer.get_next_token() 
            position = self._token.get_position()

            right_signed_factor = self.parse_signed_factor() 

            self.not_none(right_signed_factor, MissingExpectedStatement, "right_signed_factor")
            
            if operator == TokenType.ASTERISK:
                left_signed_factor = MultTerm(left_signed_factor, position, right_signed_factor)
            else:
                left_signed_factor = DivTerm(left_signed_factor, position, right_signed_factor)
        
        return left_signed_factor

    # signed_factor   ::== [sign] factor ;
    def parse_signed_factor(self):
        position = self._token.get_position()

        unary_negation = False
        if (self._token.get_token_type() == TokenType.MINUS):
            unary_negation = True
            self._token = self._lexer.get_next_token()
        
        factor = self.parse_factor()
        
        if unary_negation:
            self.not_none(factor, MissingExpectedStatement, "factor", position)
            return SignedFactor(factor, position)
        return factor
        

    # factor ::== pair_or_expr | literal | list_def | dict_def |  select_term |  object_access;
    def parse_factor(self):
        position = self._token.get_position()

        factor = self.parse_literal() or self.parse_list() or self.parse_object_access_identifier() or self.parse_pair_or_expr() or self.parse_dict() or self.parse_select()

        return factor
    
    
    # literal ::== number | bool | string;
    def parse_literal(self):
        literal = self.parse_number() or self.parse_string() or self.parse_bool() 
        if literal:
            return literal
        return None
    
    def parse_number(self):
        position = self._token.get_position()

        if self._token.get_token_type() not in (TokenType.INT, TokenType.FLOAT):
            return None
        
        value = self._token.get_value()
        self._token = self._lexer.get_next_token()

        return Number(value, position)
    
    def parse_string(self):
        position = self._token.get_position()

        if self._token.get_token_type() != TokenType.STRING:
            return None
        
        value = self._token.get_value()
        self._token = self._lexer.get_next_token()

        return String(value, position)
    
    
    def parse_bool(self):
        position = self._token.get_position()

        if self._token.get_token_type() == TokenType.TRUE:
            value = True
        elif self._token.get_token_type() == TokenType.FALSE:
            value = False
        else:
            return None

        self._token = self._lexer.get_next_token()
        return Bool(value, position)

    # list_def	::== '[' [ expressions_list ] ']' ;
    def parse_list(self):

        if self._token.get_token_type() != TokenType.SQUARE_BRACKET_OPENING:
            return None
        
        position = self._token.get_position()
        
        self._token = self._lexer.get_next_token()
        values = self.parse_expressions_list()

        if values is None:
            values = []

        if self._token.get_token_type() != TokenType.SQUARE_BRACKET_CLOSING:
            raise SyntaxError("Missing ']' to close list")
        

        self._token = self._lexer.get_next_token()
        return List(values, position)
    

    # expressions_list ::== expression {‘,’ expression}
    def parse_expressions_list(self):
        expressions = []
        expression = self.parse_expression()
        position = self._token.get_position()
        if expression is None:
            return None
        
        expressions.append(expression)

        while (self._token.get_token_type() == TokenType.COMMA):
            self._token = self._lexer.get_next_token()
            expression = self.parse_expression()
            
            self.not_none(expression, MissingExpectedStatement, "Expression")
            expressions.append(expression)
        
        return expressions
    
    # pair_or_expr ::== ‘(‘ expression [‘,' expression ] ‘)’ # or expression
    def parse_pair_or_expr(self):
        position = self._token.get_position()

        if self._token.get_token_type() != TokenType.BRACKET_OPENING:
            return None
        
        self._token = self._lexer.get_next_token()

        expression = self.parse_expression()

        if self._token.get_token_type() != TokenType.COMMA:
            if self._token.get_token_type() != TokenType.BRACKET_CLOSING:
                raise SyntaxError("Missing ')' to close expression in brackets")
            return expression
    
        self._token = self._lexer.get_next_token()

        expression_second = self.parse_expression()

        # raise SyntaxError("Pair started but missing second expression")
        self.not_none(expression_second, MissingExpectedStatement, "Expression")

        if self._token.get_token_type() != TokenType.BRACKET_CLOSING:
            raise SyntaxError("Missing ')' to close pair")
        self._token = self._lexer.get_next_token()

        return Pair(expression, expression_second, position)

    # dict_def 	   ::== '{' [ expressions_list ]  '}';
    def parse_dict(self):
        position = self._token.get_position()

        if self._token.get_token_type() != TokenType.BRACE_OPENING:
            return None
        
        self._token = self._lexer.get_next_token()
        values = self.parse_expressions_list()

        if values is None:
            values = {}

        if self._token.get_token_type() != TokenType.BRACE_CLOSING:
            raise SyntaxError("Missing '}' to close dict")
        

        self._token = self._lexer.get_next_token()
        return Dict(values, position)
    
    #select_term ::== 'SELECT' expression 'FROM' expression [ 'WHERE' expression ] [ 'ORDER BY' expression ['ASC' | 'DESC'] ] ‘;’;

    def parse_select(self):
        if self._token.get_token_type() != TokenType.SELECT:
            return None
        
        position = self._token.get_position()
        self.consume_token()

        select_expression = self.parse_expression()
        self.not_none(select_expression, MissingExpectedStatement, "select_expression")

        self.must_be(TokenType.FROM, MissingExpectedStatement)

        from_expression = self.parse_expression()
        self.not_none(from_expression, MissingExpectedStatement, "FROM_expression")

        if self._token.get_token_type() != TokenType.WHERE:
            return SelectTerm(select_expression, from_expression, position)
        
        self.consume_token()

        where_expression = self.parse_expression()
        self.not_none(where_expression, MissingExpectedStatement, "WHERE_expression")

        if self._token.get_token_type() != TokenType.ORDER_BY:
            return SelectTerm(select_expression, from_expression, position, where_expression)
        
        self.consume_token()

        order_by_expression = self.parse_expression()
        self.not_none(order_by_expression, MissingExpectedStatement, "ORDER_BY_expression")

        asc_desc = "ASC"
        if self._token.get_token_type() == TokenType.ASC:
            self.consume_token()
        elif self._token.get_token_type() == TokenType.DESC:
            asc_desc = "DESC"
            self.consume_token()

        return SelectTerm(select_expression, from_expression, position, where_expression, order_by_expression, asc_desc)




    

    # non statements possible?
    # block ::== '{' {statement} '}'
    def parse_block(self):
        position = self._token.get_position()

        if self._token.get_token_type() != TokenType.BRACE_OPENING:
            return None
        self._token = self._lexer.get_next_token()

        block_statements = []

        while statement := self.parse_statement():
            block_statements.append(statement)
        
        self.must_be(TokenType.BRACE_CLOSING, MissingExpectedStatement)

        return Block(block_statements, position)
        



        

