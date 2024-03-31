from reader import Reader, Position
from tokens import Token, TokenType
import sys

EOT = "EOT" # change later

# FOR TEST OTHER PARTS
# if __name__ == "__main__":
#    reader = Reader("test_file.txt")
#    for i in range(15):
#         print(reader.get_character())
#         current_position = reader.get_position()
#         print(current_position)
#         reader.next_character()
class IntLimitExceeded:
   pass

class Lexer:
   def __init__(self, source):
      self._reader = Reader(source)

   def get_next_token(self):

      self.skip_whites()

      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])

      if self._reader.get_character() == EOT:
         return Token(TokenType.END_OF_TEXT, position)

      # try to build tokens 
      token = self.build_number()
      return token



   def skip_whites(self):
      while (self._reader.get_character()).isspace():
         self._reader.next_character()

   def build_number(self):
      character = self._reader.get_character()
      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      if (not character.isdecimal()):
         return None
      
      if character == "0":
         value = 0
         self._reader.next_character()
      else:
         value = int(character) # ascii code for 0

         self._reader.next_character()
         character = self._reader.get_character()

         while character.isdecimal():
            new_value = int(character)
            
            if ( value >= (sys.maxsize - new_value)/10 ):
               raise IntLimitExceeded(position)

            value = value*10 + new_value
            self._reader.next_character()  
            character = self._reader.get_character()

      if self._reader.get_character() != '.':
         return Token(TokenType.INT, position, value)
      
      self._reader.next_character()
      character = self._reader.get_character()
      fraction = 0
      digits = 0
      while character.isdecimal():
            new_decimal = int(character)
            
            # correct later - it should check with integer value
            if ( fraction >= (sys.maxsize - new_decimal)/10 ):
               raise IntLimitExceeded(position)

            fraction = fraction*10 + new_decimal
            digits += 1
            self._reader.next_character()
            character = self._reader.get_character() 

      number = float( value + fraction / 10**digits)
      return Token(TokenType.FLOAT, position, number)


   def build_string(self):
      pass
   
   def build_identifier_or_keyword(self):
      pass
      # powinien być to maks limit identifiera

   def build_two_letters_operators(self):
      pass
   # operators




