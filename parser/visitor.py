from syntax_tree import Node
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
    def visit_fun_call_statement(self, fun_call_statement):
        pass

    @abstractmethod
    def visit_if_statement(self, if_statement):
        pass