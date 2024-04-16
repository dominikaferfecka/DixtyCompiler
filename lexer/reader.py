from position import Position
from standards import ETX, EOL
from standards import NEWLINE


class Reader:
    def __init__(self, source):
        self._source = source
        self._position = Position()
        self._character = None
        self._last_checked_EOL = False
        self.next_character()

    def get_character(self):
        self._last_checked_EOL = False
        return self._character

    def get_position(self):
        return (self._position.get_row(), self._position.get_column())

    def next_character(self):
        if self._character is not ETX:
            if not self._last_checked_EOL:
                new_character = self.read_character() 
                if new_character == ETX:
                    self._character = ETX
                else:
                    return self.check_EOL(new_character) # EOL or other
            else:  # next is already in the self character
                self._last_checked_EOL = False
        return self._character

    def read_character(self):
        character = self._source.read()
        if character:
            if self._character != EOL:  # check last
                self._position.increase_column()
            else:
                self._position.start_next_row()
            return character
        else:
            return ETX

    def check_EOL(self, character):
        if character in NEWLINE.keys():
            next_character = self._source.read()
            if next_character == NEWLINE[character]:
                self._character = EOL
                return EOL
            elif character == '\n':
                self._character = next_character
                self._position.start_next_row()
                self._last_checked_EOL = True
                return EOL
            else:
                self._position.increase_column()
                self._last_checked_EOL = True
                self._character = next_character
                return character
        else:
            self._character = character
            return character
