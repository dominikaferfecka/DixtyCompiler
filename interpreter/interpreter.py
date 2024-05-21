from parser.parser import Parser, Identifier
from parser.visitor import Visitor
from interpreter.context import Context, Scope
from interpreter.assign import IdentifierEvaulation, IndexAcccesEvaulation
from interpreter.builtins import FunEmbedded

class Interpreter(Visitor):
    def __init__(self, functions, builtins):
        self._functions = functions
        self._functions.update(builtins)
        self._last_result = None
        self._if_done = False
        self._current_context = Context(functions)
        self._contexts = []
        #self._return_type = None
        self._return = False # if true stop visiting in block statemet till fundef

    
    def add_context(self):
        self._contexts.append(self._current_context)
        self._current_context = Context(self._functions, self._current_context._scopes)
    def remove_context(self):
        self._current_context = self._contexts.pop()
    
    def get_last_result(self):
        last_result = self._last_result
        self._last_result = None
        return last_result

    # def evaulate(self, element):
    #     if isinstance(element, Identifier): #?
    #         element = self._current_context.get_scope_variable(element._name)
    #     return element

    def evaulate(self, element):
        if isinstance(element, IdentifierEvaulation): #?
            element = element._value
        elif isinstance(element, IndexAcccesEvaulation):
            element = element._value
        return element


    def visit_for_statement(self, for_statement, arg):
        for_statement._identifier.accept(self, arg)
        self._current_context.add_scope()
        variable = self.get_last_result()
        for_statement._expression.accept(self, arg)
        iterating = self.get_last_result()
        

        iterating = self.evaulate(iterating)
        for value in iterating:
            self._current_context.set_scope_variable(variable, value )
            for_statement._block.accept(self, arg)
        print("for statement")
        self._current_context.remove_scope()
    
    def visit_while_statement(self, while_statement, arg):
        print("while statement")
        self._current_context.add_scope()
        while_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        print(expression)


        while expression:
            while_statement._block.accept(self)
            while_statement._expression.accept(self, arg)
            expression = self.get_last_result()
        self._current_context.remove_scope()

    
    def visit_fun_def_statement(self, fun_def_statement, arg):
        print("fun_def statement")

    def visit_return_statement(self, return_statement, arg):
        self._last_result = None # clear in case there was no value after return
        return_statement._expression.accept(self, arg)
        self._return = True
        print(f"return statement {return_statement}")
 
    def visit_assign_statement(self, assign_statement, arg):
        assign_statement._object_access.accept(self, arg)
        object_access = self.get_last_result()
        assign_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        
        expression = self.evaulate(expression)

        self._current_context.set_scope_variable(object_access, expression)

        print([scope._variables for scope in self._current_context._scopes])

        print(f"assign_statement {object_access} = {expression}")


    def visit_if_statement(self, if_statement, arg):
        if_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        print(f"if statement ({expression})")
        self._if_done = False
        if expression:
            self._current_context.add_scope()
            if_statement._block.accept(self, arg)
            self._if_done = True
            self._current_context.remove_scope()
        else:
            else_if_list = if_statement._else_if_statement
            if else_if_list is not None:
                for else_if in else_if_list:
                    if self._if_done is False:
                        else_if.accept(self, arg)
        if self._if_done is False:
            else_statement = if_statement._else_statement
            if else_statement is not None:
                else_statement.accept(self, arg)

    def visit_else_if_statement(self, else_if_statement, arg):
        else_if_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        print(f"else_if statement ({expression})")
        if expression:
            self._current_context.add_scope()
            else_if_statement._block.accept(self, arg)
            self._if_done = True
            self._current_context.remove_scope()
    
    def visit_else_statement(self, else_statement, arg):
        print(f"else statement")
        self._current_context.add_scope()
        else_statement._block.accept(self, arg)
        self._if_done = True
        self._current_context.remove_scope()
    
    def visit_block(self, block, arg):
        print("block")
        for statement in block._statements:
            if not self._return:
                statement.accept(self, arg)
    

    def visit_or_term(self, or_term, arg):
        or_term._left_and_term.accept(self, arg)
        left_not_term = self.get_last_result()
        or_term._right_and_term.accept(self, arg)
        right_not_term = self.get_last_result()

        self._last_result = left_not_term or right_not_term
        print(f"or_term {self._last_result}")

    def visit_and_term(self, and_term, arg):
        and_term._left_not_term.accept(self, arg)
        left_not_term = self.get_last_result()
        and_term._right_not_term.accept(self, arg)
        right_not_term = self.get_last_result()

        self._last_result = left_not_term and right_not_term
        print(f"and_term {self._last_result}")
    
    def visit_not_term(self, not_term, arg):
        not_term._comparison_term.accept(self, arg)
        comparison_term = self.get_last_result()
        self._last_result = not comparison_term
        print(f"not_term {self._last_result}")

    def visit_equal_term(self, equal_term, arg):
        equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        equal_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, int):
            self._last_result = int(left_additive_term / right_additive_term) # ??
        elif self.check_types(left_additive_term, right_additive_term, float):
            self._last_result = left_additive_term / right_additive_term
        else:
            raise SyntaxError  

        self._last_result = left_additive_term == right_additive_term
        print(f"equal_term {self._last_result}")

    def visit_less_term(self, less_term, arg):
        less_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        less_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, int):
            self._last_result = int(left_additive_term / right_additive_term) # ??
        elif self.check_types(left_additive_term, right_additive_term, float):
            self._last_result = left_additive_term / right_additive_term
        else:
            raise SyntaxError  

        self._last_result = left_additive_term < right_additive_term
        print(f"less_term {self._last_result}")

    def visit_more_term(self, more_term, arg):
        more_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        more_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()
        
        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, int):
            self._last_result = int(left_additive_term / right_additive_term) # ??
        elif self.check_types(left_additive_term, right_additive_term, float):
            self._last_result = left_additive_term / right_additive_term
        else:
            raise SyntaxError  
        
        self._last_result = left_additive_term > right_additive_term
        print(f"more_term {self._last_result}")

    def visit_less_or_equal_term(self, less_or_equal_term, arg):
        less_or_equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        less_or_equal_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, int):
            self._last_result = int(left_additive_term / right_additive_term) # ??
        elif self.check_types(left_additive_term, right_additive_term, float):
            self._last_result = left_additive_term / right_additive_term
        else:
            raise SyntaxError  
        
        self._last_result = left_additive_term <= right_additive_term
        print(f"less_or_equal_term {self._last_result}")

    def visit_more_or_equal_term(self, more_or_equal_term, arg):
        more_or_equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        more_or_equal_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, int):
            self._last_result = int(left_additive_term / right_additive_term) # ??
        elif self.check_types(left_additive_term, right_additive_term, float):
            self._last_result = left_additive_term / right_additive_term
        else:
            raise SyntaxError  
        
        self._last_result = left_additive_term <= right_additive_term
        print(f"more_or_equal_term {self._last_result}")
    
    def check_types(self, left, right, type):
        return isinstance(left, type) and isinstance(right, type)


    def visit_add_term(self, add_term, arg):
        add_term._left_mult_term.accept(self, arg)
        left_mult_term = self.get_last_result()
        add_term._right_mult_term.accept(self, arg)
        right_mult_term = self.get_last_result()

        left_mult_term = self.evaulate(left_mult_term)
        right_mult_term = self.evaulate(right_mult_term)

        if self.check_types(left_mult_term, right_mult_term, int) or self.check_types(left_mult_term, right_mult_term, float) or self.check_types(left_mult_term, right_mult_term, str):
            self._last_result = left_mult_term + right_mult_term
        else:
            raise SyntaxError    
        print(f"add_term: {self._last_result}")

    def visit_sub_term(self, sub_term, arg):
        sub_term._left_mult_term.accept(self, arg)
        left_mult_term = self.get_last_result()
        sub_term._right_mult_term.accept(self, arg)
        right_mult_term = self.get_last_result()

        left_mult_term = self.evaulate(left_mult_term)
        right_mult_term = self.evaulate(right_mult_term)

        if self.check_types(left_mult_term, right_mult_term, int) or self.check_types(left_mult_term, right_mult_term, float):
            self._last_result = left_mult_term + right_mult_term
        else:
            raise SyntaxError   
        print(f"sub_term: {self._last_result}")
    
    def visit_mult_term(self, mult_term, arg):
        mult_term._left_signed_factor.accept(self, arg)
        left_signed_factor = self.get_last_result()
        mult_term._right_signed_factor.accept(self, arg)
        right_signed_factor = self.get_last_result()

        left_signed_factor = self.evaulate(left_signed_factor)
        right_signed_factor = self.evaulate(right_signed_factor)

        if self.check_types(left_signed_factor, right_signed_factor, int) or self.check_types(left_signed_factor, right_signed_factor, float):
            self._last_result = left_signed_factor * right_signed_factor
        else:
            raise SyntaxError  
        print(f"mult_term: {self._last_result}")

    def visit_div_term(self, div_term, arg):
        div_term._left_signed_factor.accept(self, arg)
        left_signed_factor = self.get_last_result()
        div_term._right_signed_factor.accept(self, arg)
        right_signed_factor = self.get_last_result()

        left_signed_factor = self.evaulate(left_signed_factor)
        right_signed_factor = self.evaulate(right_signed_factor)

        if self.check_types(left_signed_factor, right_signed_factor, int):
            self._last_result = int(left_signed_factor / right_signed_factor) # ??
        elif self.check_types(left_signed_factor, right_signed_factor, float):
            self._last_result = left_signed_factor / right_signed_factor
        else:
            raise SyntaxError  

        print(f"div_term: {self._last_result}")
    
    def visit_signed_factor(self, signed_factor, arg):
        signed_factor._factor.accept(self, arg)
        signed_factor = self.get_last_result()
        self._last_result = signed_factor
        print(f"signed factor: {self._last_result}")

    def visit_object_access(self, object_access, arg):
        object_access._left_item.accept(self, arg)
        left_item = self.get_last_result()
        object_access._right_item.accept(self, arg)
        right_item = self.get_last_result()

        self._last_result = object_access

        print(f"object_access: {left_item} . {right_item}")

    def visit_item(self, item, arg):
        print("item")
    
    def visit_item_statement(self, item, arg):
        print("item_statement")

    def visit_index_access(self, index_access, arg):
        index_access._left.accept(self, arg)
        left = self.get_last_result()
        # if isinstance(left, IndexAcccesEvaulation):
        #     left = left._value
        index_access._index_object.accept(self, arg)
        index_object = self.get_last_result()

        if isinstance(left, IndexAcccesEvaulation):
            indexes = left._index_access_list
            indexes.append(index_object)
        else:
            indexes = [index_object]

        # left_object = self.evaulate(left)
        # self._last_result = left_object[index_object]

        # self._last_result = IndexAcccesEvaulation(self, left, index_object)
        self._last_result = IndexAcccesEvaulation(self, left, indexes)
        
        print(f"index access: {left} [ {index_object} ] - {self._last_result}")
    
    def visit_fun_call(self, fun_call, arg):
        fun_call._left.accept(self, arg)
        identifier = self.get_last_result()
        arguments = fun_call._arguments

        fun_def = self._current_context.get_scope_function(identifier._name)
        
        if fun_def is None:
            raise SyntaxError

        # if isinstance(fun_def, FunEmbedded):
        #     pass
        # else:
        parameters = fun_def._parameters

        # if parameters is None:
        #     parameters = []
        if arguments is None:
            arguments = []

        if not len(parameters) == len(arguments):
            raise SyntaxError
        
        self.add_context()
        #self._current_context.add_scope()
        arguments_parsed = []
        for argument, parameter in zip(arguments,parameters):
            #print(f"parameter: {parameter._name}")
            print(f"argument {argument}")
            argument.accept(self, arg)
            argument_parsed = self.get_last_result()
            print(f"argument_parsed {argument_parsed}")
            argument_parsed = self.evaulate(argument_parsed)
            print(f"argument_parsed_evaulate {argument_parsed}")
            arguments_parsed.append(argument_parsed)
            self._current_context.set_scope_variable(parameter, argument_parsed)
            
        print(f"fun_call: {identifier._name} ( {arguments_parsed} )")
        
        if isinstance(fun_def, FunEmbedded):
            fun_def.run(self._current_context)
        else:
            fun_def._block.accept(self, arg)

        #returned_value = self.get_last_result()

        self._return = False
        #self._current_context.remove_scope()
        self.remove_context()

    def visit_list(self, list, arg):
        result_list = []
        for element in  list._values:
            element.accept(self, arg)
            parsed_element = self.get_last_result()
            result_list.append(parsed_element)
        self._last_result = result_list
        print(f"list {self._last_result}")

    def visit_pair(self, pair, arg):
        pair._first.accept(self, arg)
        first = self.get_last_result()
        pair._second.accept(self, arg)
        second = self.get_last_result()
        self._last_result = (first, second)
        print(f"pair {self._last_result}")

    def visit_dict(self, dict, arg):
        result_dict = {}
        if dict._values is not None:
            for value in dict._values:
                value.accept(self, arg)
                pair = self.get_last_result()
                pair_key = self.evaulate(pair[0])
                pair_value = self.evaulate(pair[1])
                print(f" pair {pair_value}")
                result_dict[pair_key] = pair_value
        self._last_result = result_dict
        print(f"dict {self._last_result}")

    def visit_select_term(self, select_term, arg):
        print("select_term")

    def visit_identifier(self, identifier, arg):
        self._last_result = IdentifierEvaulation(self, identifier)
        # print(f"identifier {self._last_result}")

    def visit_literal(self, literal, arg):
        print("literal")

    def visit_number(self, number, arg):
        self._last_result = number._value
        print(f"number {self._last_result}")

    def visit_string(self, string, arg):
        self._last_result = string._value
        print(f"string {self._last_result}")
    
    def visit_bool(self, bool, arg):
        self._last_result = bool._value
        print(f"bool {self._last_result}")



