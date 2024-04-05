from io import TextIOWrapper, BytesIO
import sys
from position import Position
from standards import ETX, EOL
import codecs
from standards import NEWLINE

class Reader:
    def __init__(self, source, encoding='utf-8'):
        if isinstance(source, str):
            self._source = open(source, 'r', encoding=encoding)
            #self._source = source ??
        elif hasattr(source, 'read'):
            self._source = TextIOWrapper(BytesIO(source.getvalue().encode(encoding)), encoding=encoding)
        elif source is sys.stdin:
            self._source = TextIOWrapper(sys.stdin.buffer, encoding=encoding)
        else:
            raise ValueError("Invalid source type. Must be a file path, a file-like object, or sys.stdin.")
        
        self._position = Position()
        self._character = None
        self._last_two_chars_EOL = False
        self.next_character()
    
    def get_character(self):
        return self._character
    
    def get_position(self):
        # new_position = self._position
        # return new_position
        return (self._position.get_row(), self._position.get_column())
    
    def read_character(self):
        character = self._source.read(1)
        if character:
            if self._character != EOL:
                self._position.increase_column()
                self.check_EOL()
            else:
                self._position.start_next_row()
            self._character = character
        else:
            self._character = ETX

    
    def next_character(self):
        if self._character is not ETX and not self._last_two_chars_EOL:
            self._last_two_chars_EOL = False
            self.read_character()
        


    def check_EOL(self):
        if self._character in NEWLINE.keys():
            self.next_character()
            next_character = self.get_character()
            if next_character == NEWLINE[self._character]: # check 'EOL: \n\r' ACORN BBC and RISC OS standard
                self._last_two_chars_EOL = True
                self.next_character()
                return EOL
            elif self._character == '\\n':
                return EOL

