from reader import Reader
import io
from standards import EOL

def test_EOL_n():
    reader = Reader(io.StringIO("\n"))
    
    character = reader.get_character()
    assert(character == EOL) 

def test_EOL_n_r():
    reader = Reader(io.StringIO("\n\r"))
    
    character = reader.get_character()
    assert(character == EOL)  

def test_EOL_r_n():
    reader = Reader(io.StringIO("\r\n"))
    
    character = reader.get_character()
    assert(character == EOL)  