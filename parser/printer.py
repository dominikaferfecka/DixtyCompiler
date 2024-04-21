from parser.visitor import Visitor

# indent = " " * 5
new_indent = "|" + ("-" * 5)

class Printer(Visitor):
    def __init__(self):
        pass

    def visit_for_statement(self, for_statement, indent=""):
        print(f"ForStatement [{for_statement} position [{for_statement._position}]")
        for_statement._identifier.accept(self)

    def visit_while_statement(self, while_statement, indent=""):
        print(f"WhileStatement [{while_statement} position [{while_statement._position}]")
        while_statement._identifier.accept(self)
    
    def visit_fun_def_statement(self, fun_def_statement, indent=""):
        print(f"FunDefStatement - memory: [{hex(id(fun_def_statement))}], name: [{fun_def_statement._name._name}], position [{fun_def_statement._position}]")
        #self.visit_block(fun_def_statement._block, indent + new_indent)
        fun_def_statement._block.accept(self, indent + new_indent)

    def visit_return_statement(self, return_statement, indent=""):
        print(f"ReturnStatement - memory: [{hex(id(return_statement))}], name: [{return_statement._name._name}], position [{return_statement._position}]")
        return_statement._expression.accept(self, indent + new_indent)
    
    def visit_assign_statement(self, assign_statement, indent=""):
        print(f"{indent}Assignment - memory: [{hex(id(assign_statement))}], position [{assign_statement._position}]") 
        assign_statement._object_access.accept(self, indent + new_indent)
        assign_statement._expression.accept(self, indent + new_indent)

    def visit_fun_call_statement(self, fun_call_statement, indent=""):
        print(f"{indent}FunCall - memory: [{hex(id(fun_call_statement))}], position [{fun_call_statement._position}], name [{fun_call_statement._name._name}]")
        for parameter in fun_call_statement._parameters:
            parameter.accept(self, indent + new_indent + "Parameter: ")
    
    def visit_if_statement(self, if_statement, indent=""):
        print(f"{indent}IfStatement - memory: [{hex(id(if_statement))}], position [{if_statement._position}]") 
        if_statement._expression.accept(self, indent + new_indent)
        if_statement._block.accept(self, indent + new_indent)
        for else_if in if_statement.else_if_statement:
            else_if.accept(self, indent + new_indent)
        if_statement._else_statement.accept(self, indent + new_indent)
    
    def visit_else_if_statement(self, else_if_statement, indent=""):
        print(f"{indent}ElseIfStatement - memory: [{hex(id(else_if_statement))}], position [{else_if_statement._position}]") 
        else_if_statement._expression.accept(self, indent + new_indent)
        else_if_statement._block.accept(self, indent + new_indent)

    def visit_else_statement(self, else_statement, indent=""):
        print(f"{indent}ElseStatement - memory: [{hex(id(else_statement))}], position [{else_statement._position}]") 
        else_statement._block.accept(self, indent + new_indent)

    def visit_or_term(self, or_term, indent=""):
        print(f"{indent}OrTerm - memory: [{hex(id(or_term))}], position [{or_term._position}]") 
        or_term._left_and_term.accept(self, indent + new_indent)
        or_term._right_and_term.accept(self, indent + new_indent)
    
    def visit_and_term(self, and_term, indent=""):
        print(f"{indent}AndTerm - memory: [{hex(id(and_term))}], position [{and_term._position}]") 
        and_term._left_not_term.accept(self, indent + new_indent)
        and_term._right_not_term.accept(self, indent + new_indent)
    
    def visit_not_term(self, not_term, indent=""):
        print(f"{indent}NotTerm - memory: [{hex(id(not_term))}], position [{not_term._position}]") 
        not_term._comparison_term.accept(self, indent + new_indent)
        not_term._rcomparison_term.accept(self, indent + new_indent)
    
    def visit_add_term(self, add_term, indent=""):
        print(f"{indent}AddTerm - memory: [{hex(id(add_term))}], position [{add_term._position}]") 
        add_term._left_mult_term.accept(self, indent + new_indent)
        add_term._right_mult_term.accept(self, indent + new_indent)

    def visit_sub_term(self, sub_term, indent=""):
        print(f"{indent}SubTerm - memory: [{hex(id(sub_term))}], position [{sub_term._position}]") 
        sub_term._left_mult_term.accept(self, indent + new_indent)
        sub_term._right_mult_term.accept(self, indent + new_indent)
    
    def visit_mult_term(self, mult_term, indent=""):
        print(f"{indent}MultTerm - memory: [{hex(id(mult_term))}], position [{mult_term._position}]") 
        mult_term._left_signed_factor.accept(self, indent + new_indent)
        mult_term._right_signed_factor.accept(self, indent + new_indent)
    
    def visit_div_term(self, div_term, indent=""):
        print(f"{indent}DivTerm - memory: [{hex(id(div_term))}], position [{div_term._position}]") 
        div_term._left_signed_factor.accept(self, indent + new_indent)
        div_term._right_signed_factor.accept(self, indent + new_indent)

    def visit_signed_factor(self, signed_factor, indent=""):
        print(f"{indent}SignedFactor - memory: [{hex(id(signed_factor))}], position [{signed_factor._position}], factor: [{signed_factor._factor}]") 

    def visit_literal(self, literal, indent=""):
        print(f"{indent}Literal - memory: [{hex(id(literal))}], position [{literal._position}], factor: [{literal._factor}]") 

    def visit_number(self, number, indent=""):
        print(f"{indent}Number - memory: [{hex(id(number))}], position [{number._position}], value: [{number._value}]") 
    
    def visit_string(self, string, indent=""):
        print(f"{indent}String - memory: [{hex(id(string))}], position [{string._position}], value: [{string._value}]") 
    
    def visit_bool(self, bool, indent=""):
        print(f"{indent}Bool - memory: [{hex(id(bool))}], position [{bool._position}], value: [{bool._value}]") 

    def visit_list(self, list, indent=""):
        print(f"{indent}List - memory: [{hex(id(list))}], position [{list._position}], value: [{list._values}]") 

    def visit_pair(self, pair, indent=""):
        print(f"{indent}Pair - memory: [{hex(id(pair))}], position [{pair._position}], value: [{pair._value}]") 

    def visit_dict(self, dict, indent=""):
        print(f"{indent}Dict - memory: [{hex(id(dict))}], position [{dict._position}], value: [{dict._values}]") 

    def visit_object_access(self, object_access, indent=""):
        print(f"{indent}Object access - memory: [{hex(id(object_access))}], position [{object_access._position}]") 
        object_access._left_item.accept(self, indent + new_indent)
        object_access._right_item.accept(self, indent + new_indent)

    def visit_item(self, item, indent=""):
        print(f"{indent}Item - memory: [{hex(id(item))}], position [{item._position}], value: [{item._name}]") 

    def visit_identifier(self, identifier, indent=""):
        print(f"{indent}Identifier - memory: [{hex(id(identifier))}], position [{identifier._position}], name [{identifier._name}]") 

    def visit_block(self, block, indent = ""):
        print(f"{indent}Block - memory: [{hex(id(block))}], position [{block._position}]") 
        for statement in block._statements:
            # self.visit_statement(statement)
            statement.accept(self,indent + new_indent)

    def visit_select_term(self, select_term, indent=""):
        print(f"{indent}Select term - memory: [{hex(id(select_term))}], position [{select_term._position}]") 
        select_term._select_expression.accept(self, indent + new_indent)
        select_term._from_expression.accept(self, indent + new_indent)
        if select_term._where_expression is not None:
            select_term._where_expression.accept(self, indent + new_indent)
        if select_term._order_by_expression is not None:   
            select_term._order_by_expression.accept(self, indent + new_indent)
            select_term._asc_desc.accept(self, indent + new_indent)