from visitor import Visitor

class Printer(Visitor):
    def __init__(self):
        pass

    def visit_for_statement(self, for_statement):
        print("FOR statement")

    def visit_while_statement(self, while_statement):
        print("WHILE statement")
    
    def visit_fun_def_statement(self, fun_def_statement):
        print("FUN DEF statement")

    def visit_return_statement(self, return_statement):
        print("RETURN statement")
    
    def visit_assign_or_call_statement(self, assign_or_call_statement):
        print("ASSIGN OR CALL statement")
    
    def visit_if_statement(self, if_statement):
        print("IF statement")
    