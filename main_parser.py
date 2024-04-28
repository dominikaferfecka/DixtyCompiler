from lexer.filter import Filter
from lexer.source import SourceFile
from parser.parser import Parser
import sys
import argparse

def parse_program(source, args):
    filter = Filter(source, args.int_limit, args.string_limit, args.identifier_limit)
    parser = Parser(filter)
    return parser.parse_program()


def main():
    parser = argparse.ArgumentParser(description="Parser of the Dixty programming language")
    parser.add_argument("source", help="Path to the source file or string")
    parser.add_argument("--int-limit", type=int, default=sys.maxsize, help="Maximum integer size")
    parser.add_argument("--string-limit", type=int, default=10**7, help="Maximum string size")
    parser.add_argument("--identifier-limit", type=int, default=10**7, help="Maximum identifier size")
    parser.add_argument("--source-type", choices=["file", "string"], default="file", help="Type of source (file or string), default: file")
    args = parser.parse_args()

    try:
        if args.source_type == "file":
            with SourceFile(args.source) as source:
                program = parse_program(source, args)
                print(program)

        elif args.source_type == "string":
            program = parse_program(source, args)
            print(program)
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()

