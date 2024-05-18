from parser.parser import Parser
from parser.visitor import Visitor

class Interpreter(Visitor):
    def __init__(self):
        self._last_result = None
        self._if_done = False
    
    def get_last_result(self):
        last_result = self._last_result
        self._last_result = None
        return last_result

    def visit_for_statement(self, for_statement, arg):
        print("for statement")
    
    def visit_while_statement(self, while_statement, arg):
        print("while statement")
    
    def visit_fun_def_statement(self, fun_def_statement, arg):
        print("fun_def statement")

    def visit_return_statement(self, return_statement, arg):
        print("return statement")
 
    def visit_assign_statement(self, assign_statement, arg):
        assign_statement._object_access.accept(self, arg)
        object_access = self.get_last_result()
        assign_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        # create variable
        # add value
        print(f"assign_statement {object_access} = {expression}")


    def visit_if_statement(self, if_statement, arg):
        if_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        print(f"if statement ({expression})")
        self._if_done = False
        if expression:
            if_statement._block.accept(self, arg)
            self._if_done = True
        else:
            for else_if in if_statement._else_if_statement:
                if self._if_done is False:
                    else_if.accept(self, arg)
        if self._if_done is False:
            if_statement._else_statement.accept(self, arg)

    def visit_else_if_statement(self, else_if_statement, arg):
        else_if_statement._expression.accept(self, arg)
        expression = self.get_last_result()
        print(f"else_if statement ({expression})")
        if expression:
            else_if_statement._block.accept(self, arg)
            self._if_done = True
    
    def visit_else_statement(self, else_statement, arg):
        print(f"else statement")
        else_statement._block.accept(self, arg)
        self._if_done = True
       
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
        rigth_additive_term = self.get_last_result()

        self._last_result = left_additive_term == rigth_additive_term
        print(f"equal_term {self._last_result}")

    def visit_less_term(self, less_term, arg):
        less_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        less_term._right_additive_term.accept(self, arg)
        rigth_additive_term = self.get_last_result()

        self._last_result = left_additive_term < rigth_additive_term
        print(f"less_term {self._last_result}")

    def visit_more_term(self, more_term, arg):
        more_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        more_term._right_additive_term.accept(self, arg)
        rigth_additive_term = self.get_last_result()
        self._last_result = left_additive_term > rigth_additive_term
        print(f"more_term {self._last_result}")

    def visit_less_or_equal_term(self, less_or_equal_term, arg):
        less_or_equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        less_or_equal_term._right_additive_term.accept(self, arg)
        rigth_additive_term = self.get_last_result()
        self._last_result = left_additive_term <= rigth_additive_term
        print(f"less_or_equal_term {self._last_result}")

    def visit_more_or_equal_term(self, more_or_equal_term, arg):
        more_or_equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        more_or_equal_term._right_additive_term.accept(self, arg)
        rigth_additive_term = self.get_last_result()
        self._last_result = left_additive_term <= rigth_additive_term
        print(f"more_or_equal_term {self._last_result}")
    
    def check_types(self, left, right, type):
        return isinstance(left, type) and isinstance(right, type)


    def visit_add_term(self, add_term, arg):
        add_term._left_mult_term.accept(self, arg)
        left_mult_term = self.get_last_result()
        add_term._right_mult_term.accept(self, arg)
        right_mult_term = self.get_last_result()

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

    def visit_list(self, list, arg):
        print("list")

    def visit_pair(self, pair, arg):
        print("pair")

    def visit_dict(self, dict, arg):
        print("dict")
        
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
        index_access._index_object(self, arg)
        index_object = self.get_last_result()
        print(f"index access: {left} [ {index_object} ]")
    
    def visit_fun_call(self, fun_call, arg):
        fun_call._left.accept(self, arg)
        left = self.get_last_result()
        fun_call._parameters(self, arg)
        parameters = self.get_last_result()
        print(f"fun_call: {left} ( {parameters} )")

    def visit_identifier(self, identifier, arg):
        self._last_result = identifier._name
        print(f"identifier {self._last_result}")

    def visit_block(self, block, arg):
        print("block")
        for statement in block._statements:
            statement.accept(self, arg)

    def visit_select_term(self, select_term, arg):
        print("select_term")


