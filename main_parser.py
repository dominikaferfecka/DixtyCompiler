from lexer.filter import Filter, TokenType
from lexer.source import SourceFile, SourceString
from parser.parser import Parser
import sys
import argparse


def main():
    
    # with SourceFile("test_file.dx") as source:
    #     filter = Filter(source)

    #     parser = Parser(filter)
    #     program = parser.parse_program()
    #     print(program)




    source = SourceString("for i in list: print(\"a\")")
    
    filter = Filter(source)

    parser = Parser(filter)
    program = parser.parse_program()
    print(program)




if __name__ == "__main__":
    main()
