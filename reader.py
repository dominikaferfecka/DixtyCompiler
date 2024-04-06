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
        self._last_EOL = False
        self.next_character()
    
    def get_character(self):
        self._last_EOL = False
        return self._character
    
    def get_position(self):
        # new_position = self._position
        # return new_position
        return (self._position.get_row(), self._position.get_column())


    
    def next_character(self):
        if self._character is not ETX:
            if not self._last_EOL:
                new_character = self.read_character() 
                if new_character == ETX:
                    self._character = ETX
                else:
                    character_checked = self.check_EOL(new_character) # EOL or other
                    return character_checked
            else: # already next is in the character
               self._last_EOL = False
        return self._character      

    def read_character(self):
        character = self._source.read()
        if character:
            if self._character != EOL: # check last
                self._position.increase_column()
            else:
                self._position.start_next_row()
            return character
        else:
            return ETX 


    def check_EOL(self, character):
        if character in NEWLINE.keys():
            self._character = EOL
            next_character = self.read_character()
            if next_character == NEWLINE[character]: # check 'EOL: \n\r' ACORN BBC and RISC OS standard
                self.next_character()
                self._last_EOL = True
                return EOL
            elif character == '\n':
                self._character = next_character
                self._last_EOL = True
                return EOL
        else:
            self._character = character
            return character

