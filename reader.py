from io import TextIOWrapper, BytesIO
import sys
from position import Position
from source import Source
from standards import ETX, EOL
import codecs
from standards import NEWLINE

class Reader:
    def __init__(self, source):
        self._source = source
        self._position = Position()
        self._character = None
        self._last_two_chars_EOL = False
        self.next_character()
    
    def get_character(self):
        character = self.check_EOL(self._character)
        return character
    
    def get_position(self):
        # new_position = self._position
        # return new_position
        return (self._position.get_row(), self._position.get_column())
    
    def read_character(self):
        character = self._source.read()
        if character:
            if self._character != EOL:
                self._position.increase_column()
                self._character = character

            else:
                self._position.start_next_row()
                self._character = character
        else:
            self._character = ETX

    
    def next_character(self):
        if self._character is not ETX:
            self._last_two_chars_EOL = False
            self.read_character()
        


    def check_EOL(self, character):
        if character in NEWLINE.keys():
            self._character = EOL
            self.next_character()
            next_character = self.get_character()
            if next_character == NEWLINE[character]: # check 'EOL: \n\r' ACORN BBC and RISC OS standard
                self.next_character()
                return EOL
            elif character == '\n':
                return EOL
        else:
            return character

