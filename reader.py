from io import TextIOWrapper
import sys
from position import Position

EOL = '\n' # later maybe others
EOF = "EOF" # change

class Reader:
    def __init__(self, source):
        if isinstance(source, str):
            self._source = open(source, 'r')
        elif hasattr(source, 'read'):
            self._source = source
        elif source is sys.stdin:
            self._source = source
        else:
            raise ValueError("Invalid source type. Must be a file path, a file-like object, or sys.stdin.")
        
        self._position = Position()
        self._character = None
        self.next_character()
    
    def get_character(self):
        return self._character
    
    def get_position(self):
        #return (self.position.get_row(), self.position.get_column())
        return (self._position.get_row(), self._position.get_column())
    
    def read_character(self):
        character = self._source.read(1)
        if character:
            if self._character != EOL:
                self._position.increase_column()
            else:
                self._position.start_next_row()
            self._character = character
        else:
            self._character = EOF

    
    def next_character(self):
        if self._character is not EOF:
            self.read_character()


