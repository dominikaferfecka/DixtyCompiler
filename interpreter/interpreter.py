from parser.visitor import Visitor
from interpreter.context import Context
from interpreter.assign import IdentifierEvaulation, IndexAcccesEvaulation
from interpreter.builtins import FunEmbedded
from interpreter.errors import (
    FunctionNotDeclared,
    IncorrectArgumentsNumber,
    CannotAddUnsupportedTypes,
    CannotSubUnsupportedTypes,
    CannotMultUnsupportedTypes,
    CannotDivUnsupportedTypes,
    CannotCompareUnsupportedTypes
)

class Interpreter(Visitor):
    def __init__(self, functions, builtins):
        self._functions = functions
        self._functions.update(builtins)
        self._last_result = None
        self._if_done = False
        self._current_context = Context()
        self._contexts = []
        self._return = False 

    def add_context(self):
        self._contexts.append(self._current_context)
        self._current_context = Context(self._current_context._scopes)
    
    def remove_context(self):
        self._current_context = self._contexts.pop()

    def get_function(self, name):
        if name in self._functions.keys():
            return self._functions[name]
    
    def get_last_result(self):
        last_result = self._last_result
        self._last_result = None
        return last_result

    def evaulate(self, element):
        if isinstance(element, IdentifierEvaulation): 
            element = element._value
        elif isinstance(element, IndexAcccesEvaulation):
            element = element._value
        elif isinstance(element, list):
            result = []
            for el in element:
                result.append(self.evaulate(el))
            element = result
        elif isinstance(element, tuple):
            element = (self.evaulate(element[0]), self.evaulate(element[1]))
        return element

    def check_types(self, left, right, types):
        for type in types:
            if isinstance(left, type) and isinstance(right, type):
                return True
        return False


    def visit_for_statement(self, for_statement, arg):
        for_statement._identifier.accept(self, arg)
        variable = self.get_last_result()
        for_statement._expression.accept(self, arg)
        iterating = self.get_last_result()
        
        iterating = self.evaulate(iterating)
        for value in iterating:
            self._current_context.set_scope_variable(variable, value )
            for_statement._block.accept(self, arg)
    
    def visit_while_statement(self, while_statement, arg):
        while_statement._expression.accept(self, arg)
        expression = self.get_last_result()

        while expression:
            for statement in while_statement._block._statements:
                if not self._return:
                    statement.accept(self, arg)
            while_statement._expression.accept(self, arg)
            expression = self.get_last_result()


    def visit_return_statement(self, return_statement, arg):
        self._last_result = None # clear in case there was no value after return
        if return_statement._expression is not None:
            return_statement._expression.accept(self, arg)
        self._return = True


    def visit_assign_statement(self, assign_statement, arg):
        assign_statement._object_access.accept(self, arg)
        object_access = self.get_last_result()
        assign_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        expression = self.evaulate(expression)

        self._current_context.set_scope_variable(object_access, expression)


    def visit_if_statement(self, if_statement, arg):
        if_statement._expression.accept(self, arg)
        expression = self.get_last_result()

        self._if_done = False
        if expression:
            if_statement._block.accept(self, arg)
            self._if_done = True
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

        if expression:
            else_if_statement._block.accept(self, arg)
            self._if_done = True
    
    def visit_else_statement(self, else_statement, arg):
        else_statement._block.accept(self, arg)
        self._if_done = True

    def visit_block(self, block, arg):
        self._current_context.add_scope()
        for statement in block._statements:
            if not self._return:
                statement.accept(self, arg)
        self._current_context.remove_scope()
    

    def visit_or_term(self, or_term, arg):
        or_term._left_and_term.accept(self, arg)
        left_not_term = self.get_last_result()
        or_term._right_and_term.accept(self, arg)
        right_not_term = self.get_last_result()

        self._last_result = left_not_term or right_not_term

    def visit_and_term(self, and_term, arg):
        and_term._left_not_term.accept(self, arg)
        left_not_term = self.get_last_result()
        and_term._right_not_term.accept(self, arg)
        right_not_term = self.get_last_result()

        self._last_result = left_not_term and right_not_term
    
    def visit_not_term(self, not_term, arg):
        not_term._comparison_term.accept(self, arg)
        comparison_term = self.get_last_result()
        self._last_result = not comparison_term

    def visit_equal_term(self, equal_term, arg):
        position = equal_term._position
        equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        equal_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str, bool]):
            self._last_result = left_additive_term == right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 

        self._last_result = left_additive_term == right_additive_term

    def visit_less_term(self, less_term, arg):
        position = less_term._position
        
        less_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        less_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term < right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 


    def visit_more_term(self, more_term, arg):
        position = more_term._position

        more_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        more_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()
        
        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term > right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 
    

    def visit_less_or_equal_term(self, less_or_equal_term, arg):
        position = less_or_equal_term._position

        less_or_equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        less_or_equal_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term <= right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 


    def visit_more_or_equal_term(self, more_or_equal_term, arg):
        position = more_or_equal_term._position

        more_or_equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        more_or_equal_term._right_additive_term.accept(self, arg)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term >= right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 
        
    
    def visit_add_term(self, add_term, arg):
        position = add_term._position

        add_term._left_mult_term.accept(self, arg)
        left_mult_term = self.get_last_result()
        add_term._right_mult_term.accept(self, arg)
        right_mult_term = self.get_last_result()

        left_mult_term = self.evaulate(left_mult_term)
        right_mult_term = self.evaulate(right_mult_term)

        if self.check_types(left_mult_term, right_mult_term, [int, float, str]):
            self._last_result = left_mult_term + right_mult_term
        else:
            raise CannotAddUnsupportedTypes(left_mult_term, right_mult_term, position) 

    def visit_sub_term(self, sub_term, arg):
        position = sub_term._position

        sub_term._left_mult_term.accept(self, arg)
        left_mult_term = self.get_last_result()
        sub_term._right_mult_term.accept(self, arg)
        right_mult_term = self.get_last_result()

        left_mult_term = self.evaulate(left_mult_term)
        right_mult_term = self.evaulate(right_mult_term)

        if self.check_types(left_mult_term, right_mult_term, [int, float]):
            self._last_result = left_mult_term - right_mult_term
        else:
            raise CannotSubUnsupportedTypes(left_mult_term, right_mult_term, position) 
    
    def visit_mult_term(self, mult_term, arg):
        position = mult_term._position

        mult_term._left_signed_factor.accept(self, arg)
        left_signed_factor = self.get_last_result()
        mult_term._right_signed_factor.accept(self, arg)
        right_signed_factor = self.get_last_result()

        left_signed_factor = self.evaulate(left_signed_factor)
        right_signed_factor = self.evaulate(right_signed_factor)

        if self.check_types(left_signed_factor, right_signed_factor, [int, float]):
            self._last_result = left_signed_factor * right_signed_factor
        else:
            raise CannotMultUnsupportedTypes(left_signed_factor, right_signed_factor, position) 

    def visit_div_term(self, div_term, arg):
        position = div_term._position

        div_term._left_signed_factor.accept(self, arg)
        left_signed_factor = self.get_last_result()
        div_term._right_signed_factor.accept(self, arg)
        right_signed_factor = self.get_last_result()

        left_signed_factor = self.evaulate(left_signed_factor)
        right_signed_factor = self.evaulate(right_signed_factor)

        if self.check_types(left_signed_factor, right_signed_factor, [int]):
            self._last_result = int(left_signed_factor / right_signed_factor)
        elif self.check_types(left_signed_factor, right_signed_factor, [float]):
            self._last_result = left_signed_factor / right_signed_factor
        else:
            raise CannotDivUnsupportedTypes(left_signed_factor, right_signed_factor, position) 

    def visit_signed_factor(self, signed_factor, arg):
        signed_factor._factor.accept(self, arg)
        signed_factor = self.get_last_result()
        self._last_result = signed_factor

    def visit_object_access(self, object_access, arg):
        object_access._left_item.accept(self, arg)
        left_item = self.get_last_result()
        object_access._right_item.accept(self, left_item)
        right_item = self.get_last_result()

        self._last_result = right_item

    def visit_index_access(self, index_access, arg):
        index_access._left.accept(self, arg)
        left = self.get_last_result()
        index_access._index_object.accept(self, arg)
        index_object = self.get_last_result()

        if isinstance(left, IndexAcccesEvaulation):
            indexes = left._index_access_list
            indexes.append(index_object) 
        else:
            indexes = [index_object]

        self._last_result = IndexAcccesEvaulation(self, left, indexes)
        
    
    def visit_fun_call(self, fun_call, object):
        position = fun_call._position
        fun_call._left.accept(self, None)
        identifier = self.get_last_result()
        arguments = fun_call._arguments

        fun_def = self.get_function(identifier._name)
        
        if fun_def is None:
            raise FunctionNotDeclared(identifier._name, position)

        parameters = fun_def._parameters

        if arguments is None:
            arguments = []

        if not len(parameters) == len(arguments):
            raise IncorrectArgumentsNumber(identifier._name, len(parameters), len(arguments), position)
        
        self.add_context()
        self._current_context.add_scope()
        arguments_parsed = []
        for argument, parameter in zip(arguments,parameters):
            argument.accept(self,  None)
            argument_parsed = self.get_last_result()
            argument_parsed = self.evaulate(argument_parsed)
            arguments_parsed.append(argument_parsed)
            self._current_context.set_scope_variable(parameter, argument_parsed)
        
        if isinstance(fun_def, FunEmbedded):
            fun_def.run(self, object)
        else:
            fun_def._block.accept(self, None)

        self._return = False
        self._current_context.remove_scope()
        self.remove_context()

    def visit_list(self, list, arg):
        result_list = []
        for element in  list._values:
            element.accept(self, arg)
            parsed_element = self.get_last_result()
            result_list.append(parsed_element)
        self._last_result = result_list

    def visit_pair(self, pair, arg):
        pair._first.accept(self, arg)
        first = self.get_last_result()
        pair._second.accept(self, arg)
        second = self.get_last_result()
        self._last_result = (first, second)

    def visit_dict(self, dict, arg):
        result_dict = {}
        if dict._values is not None:
            for value in dict._values:
                value.accept(self, arg)
                pair = self.get_last_result()
                pair_key = self.evaulate(pair[0])
                pair_value = self.evaulate(pair[1])
                result_dict[pair_key] = pair_value
        self._last_result = result_dict

    def visit_select_term(self, select_term, arg):
        select_expression = select_term._select_expression

        select_term._from_expression.accept(self, arg)
        from_expression = self.get_last_result()
        from_object = self.evaulate(from_expression)

        result = []

        for key, value in from_object.items():
            self._current_context.set_scope_variable("Key", key)
            self._current_context.set_scope_variable("Value", value)

            where_expression =  select_term._where_expression
            if where_expression is not None:
                where_expression.accept(self, arg)
                where_expression = self.get_last_result()
            else:
                where_expression = True

            if where_expression is True:
                select_term._select_expression.accept(self, arg)
                select_expression = self.get_last_result()
                if isinstance(select_expression, tuple):
                    select_expression = (self.evaulate(self.evaulate(select_expression[0])), self.evaulate(self.evaulate(select_expression)[1])) 
                else:
                    select_expression = self.evaulate(select_expression)
                
                result.append(select_expression)

        order_by_expression =  select_term._order_by_expression
        if order_by_expression is not None:
            asc_desc = select_term._asc_desc
            if asc_desc == "DESC":
                result.sort(reverse=True)
            else:
                result.sort()

        self._last_result = result

    def visit_identifier(self, identifier, arg):
        self._last_result = IdentifierEvaulation(self, identifier)

    def visit_number(self, number, arg):
        self._last_result = number._value

    def visit_string(self, string, arg):
        self._last_result = string._value
    
    def visit_bool(self, bool, arg):
        self._last_result = bool._value

    # def visit_literal(self, literal, arg):
    #     pass

    def visit_item_statement(self, item, arg):
        pass

    def visit_fun_def_statement(self, fun_def_statement, arg):
        pass
