from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visit_for_statement(self, for_statement):
        pass

    @abstractmethod
    def visit_while_statement(self, while_statement):
        pass

    @abstractmethod
    def visit_fun_def_statement(self, fun_def_statement):
        pass

    @abstractmethod
    def visit_return_statement(self, return_statement):
        pass

    @abstractmethod
    def visit_assign_statement(self, assign_statement):
        pass

    @abstractmethod
    def visit_return_statement(self, return_statement):
        pass

    @abstractmethod
    def visit_if_statement(self, if_statement):
        pass

    @abstractmethod
    def visit_else_if_statement(self, else_if_statement):
        pass

    @abstractmethod
    def visit_else_statement(self, else_statement):
        pass

    @abstractmethod
    def visit_or_term(self, or_term):
        pass

    @abstractmethod
    def visit_and_term(self, and_term):
        pass

    @abstractmethod
    def visit_not_term(self, not_term):
        pass

    @abstractmethod
    def visit_add_term(self, add_term):
        pass

    @abstractmethod
    def visit_sub_term(self, sub_term):
        pass

    @abstractmethod
    def visit_mult_term(self, mult_term):
        pass

    @abstractmethod
    def visit_div_term(self, div_term):
        pass

    @abstractmethod
    def visit_equal_term(self, equal_term):
        pass

    @abstractmethod
    def visit_less_term(self, less_term):
        pass

    @abstractmethod
    def visit_less_or_equal_term(self, less_or_equal_term):
        pass

    @abstractmethod
    def visit_more_term(self, more_term):
        pass

    @abstractmethod
    def visit_more_or_equal_term(self, more_or_equal_term):
        pass

    @abstractmethod
    def visit_signed_factor(self, signed_factor):
        pass

    @abstractmethod
    def visit_item_statement(self, item):
        pass

    @abstractmethod
    def visit_index_access(self, call_access):
        pass

    @abstractmethod
    def visit_fun_call(self, call_access):
        pass

    @abstractmethod
    def visit_fun_embedded(self, call_access):
        pass

    # @abstractmethod
    # def visit_literal(self, literal):
    #     pass

    @abstractmethod
    def visit_number(self, number):
        pass

    @abstractmethod
    def visit_string(self, string):
        pass

    @abstractmethod
    def visit_bool(self, bool):
        pass

    @abstractmethod
    def visit_list(self, list):
        pass

    @abstractmethod
    def visit_pair(self, pair):
        pass

    @abstractmethod
    def visit_dict(self, dict):
        pass

    @abstractmethod
    def visit_object_access(self, object_access):
        pass

    @abstractmethod
    def visit_identifier(self, identifier):
        pass

    @abstractmethod
    def visit_block(self, block):
        pass

    @abstractmethod
    def visit_select_term(self, select_term):
        pass