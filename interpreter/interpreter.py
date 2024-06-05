from parser.visitor import Visitor
from interpreter.context import Context
from interpreter.assign import IdentifierEvaulation, IndexAcccesEvaulation
from interpreter.builtins import FunEmbedded, BUILTINS
from interpreter.errors import (
    FunctionNotDeclared,
    IncorrectArgumentsNumber,
    CannotAddUnsupportedTypes,
    CannotSubUnsupportedTypes,
    CannotMultUnsupportedTypes,
    CannotDivUnsupportedTypes,
    CannotCompareUnsupportedTypes,
    CannotMakeOrOnNotBoolTypes,
    CannotMakeAndOnNotBoolTypes,
    CannotMakeNotOnNotBoolTypes,
    CannotDivByZero,
    RecursionLimitExceeded,
    VariableNotExists
)

class Interpreter(Visitor):
    def __init__(self, functions, builtins=BUILTINS, recursion_limit=200):
        self._functions = functions
        self._functions.update(builtins)
        self._last_result = None
        self._if_done = False
        self._current_context = Context()
        self._contexts = []
        self._return = False 
        self._recursion_depth = 0
        self._recursion_limit = recursion_limit

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


    def visit_for_statement(self, for_statement, *args):
        for_statement._identifier.accept(self, *args)
        variable = self.get_last_result()
        for_statement._expression.accept(self, *args)
        iterating = self.get_last_result()
        
        iterating = self.evaulate(iterating)
        for value in iterating:
            self._current_context.add_scope()
            self._current_context.set_scope_variable(variable, value )
            for_statement._block.accept(self, *args)
            self._current_context.remove_scope()
    
    def visit_while_statement(self, while_statement, *args):
        while_statement._expression.accept(self, *args)
        expression = self.get_last_result()

        self._current_context.add_scope()
        while expression:
            for statement in while_statement._block._statements:
                if not self._return:
                    statement.accept(self, *args)
            while_statement._expression.accept(self, *args)
            expression = self.get_last_result()
        self._current_context.remove_scope()


    def visit_return_statement(self, return_statement, *args):
        self._last_result = None # clear in case there was no value after return
        if return_statement._expression is not None:
            return_statement._expression.accept(self, *args)
        self._return = True


    def visit_assign_statement(self, assign_statement, *args):
        #self._last_result = None # in case if for example 2+3 were before
        assign_statement._object_access.accept(self, *args)
        object_access = self.get_last_result()
        assign_statement._expression.accept(self, *args)
        expression = self.get_last_result()
        expression = self.evaulate(expression)

        self._current_context.set_scope_variable(object_access, expression)


    def visit_if_statement(self, if_statement, *args):
        if_statement._expression.accept(self, *args)
        expression = self.get_last_result()

        self._if_done = False
        if expression:
            self._current_context.add_scope()
            if_statement._block.accept(self, *args)
            self._current_context.remove_scope()
            self._if_done = True
        else:
            else_if_list = if_statement._else_if_statement
            if else_if_list is not None:
                for else_if in else_if_list:
                    if self._if_done is False:
                        else_if.accept(self, *args)
        if self._if_done is False:
            else_statement = if_statement._else_statement
            if else_statement is not None:
                else_statement.accept(self, *args)

    def visit_else_if_statement(self, else_if_statement, *args):
        else_if_statement._expression.accept(self, *args)
        expression = self.get_last_result()

        if expression:
            self._current_context.add_scope()
            else_if_statement._block.accept(self, *args)
            self._current_context.remove_scope()
            self._if_done = True
    
    def visit_else_statement(self, else_statement, *args):
        self._current_context.add_scope()
        else_statement._block.accept(self, *args)
        self._current_context.remove_scope()
        self._if_done = True

    def visit_block(self, block, *args):
        for statement in block._statements:
            if not self._return:
                statement.accept(self, *args)

    def visit_or_term(self, or_term, *args):
        position = or_term._position
        or_term._left_and_term.accept(self, *args)
        left_and_term = self.get_last_result()
        or_term._right_and_term.accept(self, *args)
        right_and_term = self.get_last_result()
        
        if self.check_types(left_and_term, right_and_term, [bool]):
            self._last_result = left_and_term or right_and_term
        else:
            raise CannotMakeOrOnNotBoolTypes(left_and_term, right_and_term, position) 

    def visit_and_term(self, and_term, *args):
        position = and_term._position
        and_term._left_not_term.accept(self, *args)
        left_not_term = self.get_last_result()
        and_term._right_not_term.accept(self, *args)
        right_not_term = self.get_last_result()
        
        if self.check_types(left_not_term, right_not_term, [bool]):
            self._last_result = left_not_term and right_not_term
        else:
            raise CannotMakeAndOnNotBoolTypes(left_not_term, right_not_term, position) 
    
    def visit_not_term(self, not_term, *args):
        position = not_term._position
        not_term._comparison_term.accept(self, *args)
        comparison_term = self.get_last_result()
        
        if self.check_types(comparison_term, comparison_term, [bool]):
            self._last_result = not comparison_term
        else:
            raise CannotMakeNotOnNotBoolTypes(comparison_term, position) 

    def visit_equal_term(self, equal_term, *args):
        position = equal_term._position
        equal_term._left_additive_term.accept(self, *args)
        left_additive_term = self.get_last_result()
        equal_term._right_additive_term.accept(self, *args)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str, bool]):
            self._last_result = left_additive_term == right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 

        self._last_result = left_additive_term == right_additive_term

    def visit_less_term(self, less_term, *args):
        position = less_term._position
        
        less_term._left_additive_term.accept(self, *args)
        left_additive_term = self.get_last_result()
        less_term._right_additive_term.accept(self, *args)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term < right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 


    def visit_more_term(self, more_term, *args):
        position = more_term._position

        more_term._left_additive_term.accept(self, *args)
        left_additive_term = self.get_last_result()
        more_term._right_additive_term.accept(self, *args)
        right_additive_term = self.get_last_result()
        
        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term > right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 
    

    def visit_less_or_equal_term(self, less_or_equal_term, *args):
        position = less_or_equal_term._position

        less_or_equal_term._left_additive_term.accept(self, *args)
        left_additive_term = self.get_last_result()
        less_or_equal_term._right_additive_term.accept(self, *args)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term <= right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 


    def visit_more_or_equal_term(self, more_or_equal_term, *args):
        position = more_or_equal_term._position

        more_or_equal_term._left_additive_term.accept(self, *args)
        left_additive_term = self.get_last_result()
        more_or_equal_term._right_additive_term.accept(self, *args)
        right_additive_term = self.get_last_result()

        left_additive_term = self.evaulate(left_additive_term)
        right_additive_term = self.evaulate(right_additive_term)

        if self.check_types(left_additive_term, right_additive_term, [int, float, str]):
            self._last_result = left_additive_term >= right_additive_term
        else:
            raise CannotCompareUnsupportedTypes(left_additive_term, right_additive_term, position) 
        
    
    def visit_add_term(self, add_term, *args):
        position = add_term._position

        add_term._left_mult_term.accept(self, *args)
        left_mult_term = self.get_last_result()
        add_term._right_mult_term.accept(self, *args)
        right_mult_term = self.get_last_result()

        left_mult_term = self.evaulate(left_mult_term)
        right_mult_term = self.evaulate(right_mult_term)

        if self.check_types(left_mult_term, right_mult_term, [int, float, str]):
            self._last_result = left_mult_term + right_mult_term
        else:
            raise CannotAddUnsupportedTypes(left_mult_term, right_mult_term, position) 

    def visit_sub_term(self, sub_term, *args):
        position = sub_term._position

        sub_term._left_mult_term.accept(self, *args)
        left_mult_term = self.get_last_result()
        sub_term._right_mult_term.accept(self, *args)
        right_mult_term = self.get_last_result()

        left_mult_term = self.evaulate(left_mult_term)
        right_mult_term = self.evaulate(right_mult_term)

        if self.check_types(left_mult_term, right_mult_term, [int, float]):
            self._last_result = left_mult_term - right_mult_term
        else:
            raise CannotSubUnsupportedTypes(left_mult_term, right_mult_term, position) 
    
    def visit_mult_term(self, mult_term, *args):
        position = mult_term._position

        mult_term._left_signed_factor.accept(self, *args)
        left_signed_factor = self.get_last_result()
        mult_term._right_signed_factor.accept(self, *args)
        right_signed_factor = self.get_last_result()

        left_signed_factor = self.evaulate(left_signed_factor)
        right_signed_factor = self.evaulate(right_signed_factor)

        if self.check_types(left_signed_factor, right_signed_factor, [int, float]):
            self._last_result = left_signed_factor * right_signed_factor
        else:
            raise CannotMultUnsupportedTypes(left_signed_factor, right_signed_factor, position) 

    def visit_div_term(self, div_term, *args):
        position = div_term._position

        div_term._left_signed_factor.accept(self, *args)
        left_signed_factor = self.get_last_result()
        div_term._right_signed_factor.accept(self, *args)
        right_signed_factor = self.get_last_result()

        left_signed_factor = self.evaulate(left_signed_factor)
        right_signed_factor = self.evaulate(right_signed_factor)

        if right_signed_factor == 0:
            raise CannotDivByZero(position)

        if self.check_types(left_signed_factor, right_signed_factor, [int]):
            self._last_result = int(left_signed_factor / right_signed_factor)
        elif self.check_types(left_signed_factor, right_signed_factor, [float]):
            self._last_result = left_signed_factor / right_signed_factor
        else:
            raise CannotDivUnsupportedTypes(left_signed_factor, right_signed_factor, position) 

    def visit_signed_factor(self, signed_factor, *args):
        signed_factor._factor.accept(self, *args)
        signed_factor = self.get_last_result()
        self._last_result = signed_factor

    def visit_object_access(self, object_access, *args):
        object_access._left_item.accept(self, *args)
        left_item = self.get_last_result()
        object_access._right_item.accept(self, left_item)
        right_item = self.get_last_result()

        self._last_result = right_item

    def visit_index_access(self, index_access, *args):
        index_access._left.accept(self, *args)
        left = self.get_last_result()
        index_access._index_object.accept(self, *args)
        index_object = self.get_last_result()

        if isinstance(left, IndexAcccesEvaulation):
            indexes = left._index_access_list
            indexes.append(index_object) 
        else:
            indexes = [index_object]

        self._last_result = IndexAcccesEvaulation(self, left, indexes)
        
    
    def visit_fun_call(self, fun_call, *args):
        self._recursion_depth += 1
        if self._recursion_depth > self._recursion_limit:
            raise RecursionLimitExceeded(self._recursion_limit)
        
        position = fun_call._position
        # fun_call._left.accept(self, None)
        fun_call._left.accept(self, *args)
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
            # argument.accept(self,  None)
            argument.accept(self, *args)
            argument_parsed = self.get_last_result()
            argument_parsed = self.evaulate(argument_parsed)
            if argument_parsed is None and argument is not None:
                raise VariableNotExists(argument._name, position)
            arguments_parsed.append(argument_parsed)
            self._current_context.set_scope_variable(parameter, argument_parsed)
        
        # if isinstance(fun_def, FunEmbedded):
        #     fun_def.run(self, object)
        # else:
        #     fun_def._block.accept(self, None)

        # self._return = False
        # self._current_context.remove_scope()
        # self.remove_context()
        if isinstance(fun_def, FunEmbedded):
            fun_def.accept(self, arguments_parsed, *args)
        else:
            self._current_context.add_scope()
            fun_def._block.accept(self, *args)
            self._current_context.remove_scope()

        self._return = False
        self._current_context.remove_scope()
        self.remove_context()
        self._recursion_depth -= 1
    
    def visit_fun_embedded(self, fun_def, arguments_parsed, *args):

        if len(args) > 0:
            object = args[0]
            object = self.evaulate(object)
            returned = fun_def._action(arguments_parsed, object)

        else:
        # fun_def.run(self, object)
            returned = fun_def._action(arguments_parsed)
        if returned is not None:
            self._last_result = returned
        

    def visit_list(self, list, *args):
        result_list = []
        for element in  list._values:
            element.accept(self, *args)
            parsed_element = self.get_last_result()
            result_list.append(parsed_element)
        self._last_result = result_list

    def visit_pair(self, pair, *args):
        pair._first.accept(self, *args)
        first = self.get_last_result()
        pair._second.accept(self, *args)
        second = self.get_last_result()
        self._last_result = (first, second)

    def visit_dict(self, dict, *args):
        result_dict = {}
        if dict._values is not None:
            for value in dict._values:
                value.accept(self, *args)
                pair = self.get_last_result()
                pair_key = self.evaulate(pair[0])
                pair_value = self.evaulate(pair[1])
                result_dict[pair_key] = pair_value
        self._last_result = result_dict

    def visit_select_term(self, select_term, *args):
        select_expression = select_term._select_expression

        select_term._from_expression.accept(self, *args)
        from_expression = self.get_last_result()
        from_object = self.evaulate(from_expression)

        result = []

        for key, value in from_object.items():
            self._current_context.set_scope_variable("Key", key)
            self._current_context.set_scope_variable("Value", value)

            where_expression =  select_term._where_expression
            if where_expression is not None:
                where_expression.accept(self, *args)
                where_expression = self.get_last_result()
            else:
                where_expression = True

            if where_expression is True:
                select_term._select_expression.accept(self, *args)
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

    def visit_identifier(self, identifier, *args):
        self._last_result = IdentifierEvaulation(self, identifier)

    def visit_number(self, number, *args):
        self._last_result = number._value

    def visit_string(self, string, *args):
        self._last_result = string._value
    
    def visit_bool(self, bool, *args):
        self._last_result = bool._value

    # def visit_literal(self, literal, *args):
    #     pass

    def visit_item_statement(self, item, *args):
        pass

    def visit_fun_def_statement(self, fun_def_statement, *args):
        pass
