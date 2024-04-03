from io import TextIOWrapper, BytesIO
import sys
from position import Position
from standards import ETX, EOL
import codecs

class Reader:
    def __init__(self, source, encoding='utf-8'):
        if isinstance(source, str):
            self._source = open(source, 'r', encoding=encoding)
        elif hasattr(source, 'read'):
            self._source = TextIOWrapper(BytesIO(source.getvalue().encode(encoding)), encoding=encoding)
        elif source is sys.stdin:
            self._source = TextIOWrapper(sys.stdin.buffer, encoding=encoding)
        else:
            raise ValueError("Invalid source type. Must be a file path, a file-like object, or sys.stdin.")
        
        self._position = Position()
        self._character = None
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
        if self._character is not ETX:
            self.read_character()

    
    def check_EOL(self):
        if self._character == '\n':
            next_character = self.peek_next_character()
            if next_character == '\r': # check 'EOL: \n\r' ACORN BBC and RISC OS standard
                self._source.read(1) # omit next
            return EOL

        # elif self._character == '\r':
        #     next_character = self.peek_next_character()
        #     if next_character == '\n': # check 'EOL: \r\n' Microsoft Windows, DOS, Atari TOS standard
        #         self._source.read(1) # omit next
        #     return EOL

    def peek_next_character(self):
        current_position = self._source.tell() 
        next_character = self._source.read(1)
        self._source.seek(current_position)
        return next_character



# dodać obsługę znaku nowej lini 
# może być \n ale też \r\n -> i wtedy zamienić to na \n
            
# musi też ogarnąć koniec, wystawia znak ETX, niezależnie od tego czym się kończy naprawdę
# źródło z pliku - null lub none


# daje kod znaku w unicode