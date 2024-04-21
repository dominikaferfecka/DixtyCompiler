from printer import Printer
from syntax_tree import IfStatement, ForStatement

if __name__ == "__main__":
    nodes = [IfStatement("a", {}, None, None, 1), ForStatement("b", "a", {}, 1)]
    printer = Printer()
    
    for node in nodes:
        node.accept(printer)
