from parser.parser import Parser
from parser.visitor import Visitor

class Interpreter(Visitor):
    def __init__(self):
        self._last_result = None
    
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
        print("if statement")

    def visit_else_if_statement(self, else_if_statement, arg):
        print("else_if_statement")
    
    def visit_else_statement(self, else_statement, arg):
        print("else statement")
       
    def visit_or_term(self, or_term, arg):
        or_term._left_not_term.accept(self, arg)
        left_not_term = self.get_last_result()
        or_term._right_not_term.accept(self, arg)
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
        self._last_result = left_additive_term < rigth_additive_term
        print(f"less_or_equal_term {self._last_result}")

    def visit_more_or_equal_term(self, more_or_equal_term, arg):
        more_or_equal_term._left_additive_term.accept(self, arg)
        left_additive_term = self.get_last_result()
        more_or_equal_term._right_additive_term.accept(self, arg)
        rigth_additive_term = self.get_last_result()
        self._last_result = left_additive_term < rigth_additive_term
        print(f"more_or_equal_term {self._last_result}")
    
    def visit_add_term(self, add_term, arg):
        add_term._left_mult_term.accept(self, arg)
        left_mult_term = self.get_last_result()
        add_term._right_mult_term.accept(self, arg)
        right_mult_term = self.get_last_result()

        self._last_result = left_mult_term + right_mult_term
        print(f"add_term: {self._last_result}")

    def visit_sub_term(self, sub_term, arg):
        sub_term._left_mult_term.accept(self, arg)
        left_mult_term = self.get_last_result()
        sub_term._right_mult_term.accept(self, arg)
        right_mult_term = self.get_last_result()

        self._last_result = left_mult_term - right_mult_term
        print(f"sub_term: {self._last_result}")
    
    def visit_mult_term(self, mult_term, arg):
        mult_term._left_signed_factor.accept(self, arg)
        left_signed_factor = self.get_last_result()
        mult_term._right_signed_factor.accept(self, arg)
        right_signed_factor = self.get_last_result()

        self._last_result = left_signed_factor * right_signed_factor
        print(f"mult_term: {self._last_result}")

    def visit_div_term(self, div_term, arg):
        div_term._left_signed_factor.accept(self, arg)
        left_signed_factor = self.get_last_result()
        div_term._right_signed_factor.accept(self, arg)
        right_signed_factor = self.get_last_result()

        self._last_result = left_signed_factor * right_signed_factor
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

    def visit_item_statement(self, item, arg):
        print("item_statement")

    def visit_index_access(self, index_access, arg):
        print("index access")
    
    def visit_fun_call(self, call_access, arg):
        print("fun call")


    def visit_list(self, list, arg):
        print("list")

    def visit_pair(self, pair, arg):
        print("pair")

    def visit_dict(self, dict, arg):
        print("dict")
        
    def visit_object_access(self, object_access, arg):
        print("object_access")

    def visit_item(self, item, arg):
        print("item")

    def visit_identifier(self, identifier, arg):
        print("identifier")

    def visit_block(self, block, arg):
        print("block")

    def visit_select_term(self, select_term, arg):
        print("select_term")


