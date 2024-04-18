from lexer.filter import Filter, TokenType
from lexer.source import SourceFile, SourceString
import sys
import argparse

def get_tokens_from_filter(source, args):
    filter = Filter(source, args.int_limit, args.string_limit, args.identifier_limit)

    token = filter.get_next_token()
    while token is None or token.get_token_type() != TokenType.END_OF_TEXT:
        if token:
            print(token)
        token = filter.get_next_token()
    print(token)


def main():
    parser = argparse.ArgumentParser(description="Lexer of the Dixty programming language")
    parser.add_argument("source", help="Path to the source file or string")
    parser.add_argument("--int-limit", type=int, default=sys.maxsize, help="Maximum integer size")
    parser.add_argument("--string-limit", type=int, default=10**7, help="Maximum string size")
    parser.add_argument("--identifier-limit", type=int, default=10**7, help="Maximum identifier size")
    parser.add_argument("--source-type", choices=["file", "string"], default="file", help="Type of source (file or string), default: file")
    args = parser.parse_args()

    source = None

    try:
    
        if args.source_type == "file":
            with SourceFile(args.source) as source:
                get_tokens_from_filter(source, args)

        elif args.source_type == "string":
            source = SourceString(args.source)
            get_tokens_from_filter(source, args)
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
