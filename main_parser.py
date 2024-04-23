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

    #source = SourceString("fun () {x=2;}")
    source = SourceString("fun a ) {x=2;}")
    
    filter = Filter(source)

    parser = Parser(filter)
    program = parser.parse_program()


if __name__ == "__main__":
    main()
