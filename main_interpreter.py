from interpreter.interpreter import Interpreter

from parser.printer import Printer
from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceFile
import sys
import argparse

def parse_program(source):
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()

    nodes = program._statements
    interpreter = Interpreter()
    
    for node in nodes:
        if node is not None:
            node.accept(interpreter)

def main():
    with SourceFile("test_file_interpreter.dx") as source:
        parse_program(source)
   

if __name__ == "__main__":
    main()