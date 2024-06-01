from lexer.reader import Reader, Position
from lexer.tokens import Token, TokenType
from lexer.keywords import KEYWORDS
from lexer.operators import OPERATORS
from lexer.standards import STRING_ESCAPE
import sys
from lexer.errors import (
   IntLimitExceeded,
   StringLimitExceeded,
   IdentifierLimitExceeded,
   StringNotFinished,
   TokenNotRecognized,
   UnexpectedEscapeCharacter
)
from lexer.standards import ETX, EOL


class Lexer:
   def __init__(self, source, INT_LIMIT=sys.maxsize, STRING_LIMIT=10**7, IDENTIFIER_LIMIT=10**7):
      self._reader = Reader(source)
      self._INT_LIMIT = INT_LIMIT
      self._STRING_LIMIT = STRING_LIMIT
      self._IDENTIFIER_LIMIT = IDENTIFIER_LIMIT

   def get_next_token(self):

      self.skip_whites()

      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])

      if self._reader.get_character() == ETX:
         return Token(TokenType.END_OF_TEXT, position)

      token = self.build_number() or self.build_string() or self.build_identifier_or_keyword() or self.build_one_or_two_chars_operators() or self.build_one_char_operators() or self.build_comment()
      if not token:
         not_recognized = self._reader.get_character()
         raise TokenNotRecognized(position, not_recognized)
      return token

   def skip_whites(self):
      character = self._reader.get_character()
      while character.isspace() or character == '':
         character = self._reader.next_character()

   def build_number(self):
      character = self._reader.get_character()
      
      if (not character.isdecimal()):
         return None
      
      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])

      if character == "0":
         value = 0
         character = self._reader.next_character()
      else:
         value = int(character)  # ascii code for 0

         character = self._reader.next_character()

         while character.isdecimal():
            new_value = int(character)

            if (value >= (self._INT_LIMIT - new_value) / 10):
               raise IntLimitExceeded(position, self._INT_LIMIT)

            value = value*10 + new_value
            character = self._reader.next_character()


      if character != '.':
         return Token(TokenType.INT, position, value)

      character = self._reader.next_character()
      fraction = 0
      digits = 0
      while character.isdecimal():
            new_decimal = int(character)

            if (fraction >= (self._INT_LIMIT - new_decimal) / 10):
               raise IntLimitExceeded(position, self._INT_LIMIT)

            fraction = fraction*10 + new_decimal
            digits += 1
            character = self._reader.next_character()

      number = float(value + fraction / 10**digits)
      return Token(TokenType.FLOAT, position, number)

   def build_string(self):

      if self._reader.get_character() != '"':
         return None

      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      character = self._reader.next_character()

      StringBuilder = ['']

      while character not in ('"', ETX):
         if len(StringBuilder) >= self._STRING_LIMIT:
            raise StringLimitExceeded(position, self._STRING_LIMIT)

         if character == '\\':
            character = self._reader.next_character()
            if character in STRING_ESCAPE.keys():
               StringBuilder.append(STRING_ESCAPE[character])
            else:
               raise UnexpectedEscapeCharacter(position, character)
         else:
            StringBuilder.append(character)

         character = self._reader.next_character()

      if character == ETX:
         raise StringNotFinished(position)

      if character == '"':
         value = "".join(StringBuilder)
         _ = self._reader.next_character()
         return Token(TokenType.STRING, position, value)

   def build_identifier_or_keyword(self):
      character = self._reader.get_character()
      if not character.isalpha():
         return None

      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      StringBuilder = [character]

      character = self._reader.next_character()

      while (character.isalpha() or character.isdecimal() or character == "_") and character != ETX:

         if len(StringBuilder) >= self._IDENTIFIER_LIMIT:
            raise IdentifierLimitExceeded(position, self._IDENTIFIER_LIMIT)

         StringBuilder.append(character)
         character = self._reader.next_character()

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

      character = self._reader.next_character()

      if character == "=":
         _ = self._reader.next_character()
         return Token(OPERATORS[first_character + "="], position)
      else:
         return Token(OPERATORS[first_character], position)

   def build_one_char_operators(self):
      character = self._reader.get_character()

      if character not in OPERATORS.keys() or character in ("<", ">", "="):
         return None

      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      _ = self._reader.next_character()

      return Token(OPERATORS[character], position)


   def build_comment(self):
      if self._reader.get_character() != "#":
         return None

      position = Position(self._reader.get_position()[0], self._reader.get_position()[1])
      StringBuilder = []

      character = self._reader.next_character()
      while character != EOL and character != ETX:
         StringBuilder.append(character)
         character = self._reader.next_character()

      value = "".join(StringBuilder)
      return Token(TokenType.COMMENT, position, value)
