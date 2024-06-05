from interpreter.interpreter import Interpreter
from parser.parser import Parser
from lexer.filter import Filter
from lexer.source import SourceFile
from interpreter.builtins import BUILTINS
import argparse
import sys

def parse_program(source, args):
    filter = Filter(source, args.int_limit, args.string_limit, args.identifier_limit)
    parser = Parser(filter)
    program = parser.parse_program()

    nodes = program._statements
    interpreter = Interpreter(program._functions, BUILTINS, args.recursion_limit)
    
    for node in nodes:
        if node is not None:
            node.accept(interpreter)

def main():
    parser = argparse.ArgumentParser(description="Interpreter for the Dixty programming language")
    parser.add_argument("source", help="Path to the source file or string")
    parser.add_argument("--source-type", choices=["file", "string"], default="file", help="Type of source (file or string), default: file")
    parser.add_argument("--int-limit", type=int, default=sys.maxsize, help="Maximum integer size")
    parser.add_argument("--string-limit", type=int, default=10**7, help="Maximum string size")
    parser.add_argument("--identifier-limit", type=int, default=10**7, help="Maximum identifier size")
    parser.add_argument("--recursion-limit", type=int, default=200, help="Maximum recursion depth")
    args = parser.parse_args()

    try:
        if args.source_type == "file":
            with SourceFile(args.source) as source:
                parse_program(source, args)

        elif args.source_type == "string":
            parse_program(args.source, args)
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
