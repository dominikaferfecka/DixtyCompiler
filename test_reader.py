from reader import Reader
import io
from standards import EOL
from source import SourceFile, SourceString

def test_EOL_n():
    reader = Reader(SourceString("\n"))
    
    character = reader.get_character()
    assert(character == EOL) 

def test_EOL_n_r():
    reader = Reader(SourceString("\n\r"))
    
    character = reader.get_character()
    assert(character == EOL)  

def test_EOL_r_n():
    reader = Reader(SourceString("\r\n"))
    
    character = reader.get_character()
    assert(character == EOL)  