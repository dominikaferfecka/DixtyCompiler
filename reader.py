from io import TextIOWrapper, BytesIO
import sys
from position import Position
from source import Source
from standards import ETX, EOL
import codecs
from standards import NEWLINE

class Reader:
    def __init__(self, source, encoding='utf-8'):
        self._source = source
        
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
        character = self._source.read()
        if character:
            if self._character != EOL:
                self._position.increase_column()
                new_EOL = self.check_EOL(character)
                if new_EOL:
                    self._character = new_EOL
                else:
                    self._character = character

            else:
                self._position.start_next_row()
                self._character = character
        else:
            self._character = ETX

    
    def next_character(self):
        if self._character is not ETX and not self._last_two_chars_EOL:
            self._last_two_chars_EOL = False
            self.read_character()
        


    def check_EOL(self, character):
        keys = NEWLINE.keys()
        if character in NEWLINE.keys():
            self._character = EOL
            self.next_character()
            next_character = self.get_character()
            expected = NEWLINE[character]
            self._last_two_chars_EOL = True
            if next_character == NEWLINE[character]: # check 'EOL: \n\r' ACORN BBC and RISC OS standard
                self._last_two_chars_EOL = False
                self.next_character()
                return EOL
            elif character == '\n':
                return EOL

