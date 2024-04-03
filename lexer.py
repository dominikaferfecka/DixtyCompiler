from reader import Reader, Position
from tokens import Token, TokenType
from keywords import KEYWORDS
from operators import OPERATORS
import sys
from errors import (
   IntLimitExceeded, 
   StringLimitExceeded,
   IdentifierLimitExceeded,
   StringNotFinished,
   TokenNotRecognized
)
from standards import ETX, EOL

# FOR TEST OTHER PARTS
# if __name__ == "__main__":
#    reader = Reader("test_file.txt")
#    for i in range(15):
#         print(reader.get_character())
#         current_position = reader.get_position()
#         print(current_position)
#         reader.next_character(

class Lexer:
   def __init__(self, source):
      self._reader = Reader(source)

   def get_next_token(self):

      self.skip_whites()

      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])

      if self._reader.get_character() == ETX:
         return Token(TokenType.END_OF_TEXT, position)

      token = self.build_number() or self.build_string() or self.build_identifier_or_keyword() or self.build_one_or_two_chars_operators() or self.build_one_char_operators() or self.build_comment()
      if not token:
         raise TokenNotRecognized(position)
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
      STRING_MAX_LIMIT = 10**7 # ?

      if self._reader.get_character() != '"':
         return None
      
      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      self._reader.next_character()
      
      #StringBuilder = ['"']
      StringBuilder = ['']

      character = self._reader.get_character()

      while character not in ('"', ETX): # $ też?, chyba nie, na wykładzie tylko " ETX
         if len(StringBuilder) >= STRING_MAX_LIMIT:
            raise StringLimitExceeded(position)
         StringBuilder.append(character)
         self._reader.next_character()
         character = self._reader.get_character()

      if character == ETX:
         raise StringNotFinished(position)
      
      if character == '"':
         #StringBuilder.append('"')
         value = "".join(StringBuilder)
         self._reader.next_character()
         return Token(TokenType.STRING, position, value)

      # if character == '$':
      #    StringBuilder.append('"')
      #    value = StringBuilder.join(",")
      #    return Token(TokenType.STRING, position, value)


   def build_identifier_or_keyword(self):
      IDENTIFIER_MAX_LIMIT = 10**10
      character = self._reader.get_character()
      if not character.isalpha():
         return None
      
      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      StringBuilder = [character]

      self._reader.next_character()
      character = self._reader.get_character()

      while (character.isalpha() or character.isdecimal() or character == "_") and character != ETX:
         
         if len(StringBuilder) >= IDENTIFIER_MAX_LIMIT:
            raise IdentifierLimitExceeded(position)
         
         StringBuilder.append(character)
         self._reader.next_character()
         character = self._reader.get_character()

      value = "".join(StringBuilder)

      if value in KEYWORDS.keys():
         return Token( KEYWORDS[value], position)

      return Token(TokenType.IDENTIFIER, position, value)
      

   def build_one_or_two_chars_operators(self):
      character = self._reader.get_character()

      if character not in ("<", ">", "="):
         return None
      
      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      first_character = character

      self._reader.next_character()
      character = self._reader.get_character()


      if character == "=":
         self._reader.next_character()
         return Token(OPERATORS[first_character + "="], position)
      else:
         return Token(OPERATORS[first_character], position)
      
   def build_one_char_operators(self):
      character = self._reader.get_character()

      if character not in OPERATORS.keys() or character in ("<", ">", "="):
         return None
      
      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      self._reader.next_character()
      
      return Token(OPERATORS[character], position)
   
   # def build_two_chars_operators(self):
   #    character = self._reader.get_character()

   #    if character != "!":
   #       return None
      
   #    position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
   #    self._reader.next_character()

   #    if character == "=":
   #       return Token(OPERATORS["!="], position)
   #    else:
   #       raise Invalid 



   # operators

   def build_comment(self):
      if self._reader.get_character() != "#":
         return None
      
      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      StringBuilder = []

      self._reader.next_character()
      character = self._reader.get_character()
      while character != EOL and character != ETX:
         StringBuilder.append(character)
         self._reader.next_character()
         character = self._reader.get_character()
      
      value = "".join(StringBuilder)
      self._reader.next_character()

      return Token( TokenType.COMMENT, position, value)




