from parser.printer import Printer
# from parser.syntax_tree import IfStatement, ForStatement
# from parser.visitor import Visitor


from parser.parser import Parser, Filter
from lexer.source import SourceString, SourceFile
import sys
from parser.syntax_tree import (
    Program,
    ForStatement,
    WhileStatement,
    FunStatement,
    IfStatement,
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
    Block
)


if __name__ == "__main__":
    # # source = SourceString("for i in list { a = 2; };")
    # source = SourceString("""fun f(x) {result = 2+2+3; x = \"a\"; print(1);} y = 2;""")
    with SourceFile("test_file.dx") as source:
        filter = Filter(source)
        parser = Parser(filter)
        program = parser.parse_program()

        nodes = program._statements
        printer = Printer()
        
        for node in nodes:
            node.accept(printer)
