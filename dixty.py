from interpreter.interpreter import Interpreter
from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceFile
from interpreter.builtins import BUILTINS
import argparse

def parse_program(source):
    filter = Filter(source)
    parser = Parser(filter)
    program = parser.parse_program()

    nodes = program._statements
    interpreter = Interpreter(program._functions, BUILTINS)
    
    for node in nodes:
        if node is not None:
            node.accept(interpreter)

def main():
    parser = argparse.ArgumentParser(description="Interpreter for the Dixty programming language")
    parser.add_argument("source", help="Path to the source file or string")
    parser.add_argument("--source-type", choices=["file", "string"], default="file", help="Type of source (file or string), default: file")
    args = parser.parse_args()

    try:
        if args.source_type == "file":
            with SourceFile(args.source) as source:
                parse_program(source)

        elif args.source_type == "string":
            parse_program(args.source)
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
