from filter import Filter, Lexer, TokenType
from source import SourceFile, SourceString
import sys, argparse

def main():
    parser = argparse.ArgumentParser(description="Lexer of the Dixty programming language")
    parser.add_argument("source", help="Path to the source file or string")
    parser.add_argument("--int-limit", type=int, default=sys.maxsize, help="Maximum integer size")
    parser.add_argument("--string-limit", type=int, default=10**7, help="Maximum string size")
    parser.add_argument("--identifier-limit", type=int, default=10**7, help="Maximum identifier size")
    parser.add_argument("--source-type", choices=["file", "string"], default="file", help="Type of source (file or string), default: file")
    args = parser.parse_args()
    
    source = None
    if args.source_type == "file":
        source = SourceFile(args.source)
    elif args.source_type == "string":
        source = SourceString(args.source)
    
    filter = Filter(source, args.int_limit, args.string_limit, args.identifier_limit)

    token = filter.get_next_token()
    while token == None or token.get_token_type() != TokenType.END_OF_TEXT:
        if token:
            print(token)
        token = filter.get_next_token()
    print(token)

if __name__ == "__main__":
   main()
