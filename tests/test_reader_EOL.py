from reader import Reader
import io
from standards import EOL
from source import SourceFile, SourceString

def test_EOL_n():
    reader = Reader(SourceString("a\n"))
    
    character = reader.get_character()
    assert(character == "a")
    character = reader.next_character()
    assert(character == "\n") 

def test_EOL_n_r():
    reader = Reader(SourceString("a\n\r"))
    
    character = reader.get_character()
    assert(character == "a")
    character = reader.next_character()
    assert(character == EOL) 

def test_EOL_r_n():
    reader = Reader(SourceString("a\r\n"))
    
    character = reader.get_character()
    assert(character == "a")
    character = reader.next_character()
    assert(character == EOL) 