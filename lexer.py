from reader import Reader, Position
from tokens import Token, TokenType

EOT = "EOT" # change later

# FOR TEST OTHER PARTS
# if __name__ == "__main__":
#    reader = Reader("test_file.txt")
#    for i in range(15):
#         print(reader.get_character())
#         current_position = reader.get_position()
#         print(current_position)
#         reader.next_character()


class Lexer:
   def __init__(self, source):
      self._reader = Reader(source)

   def get_next_token(self):

      self.skip_whites()

      position = self._reader.get_position()

      if self._reader.get_character() == EOT:
         return Token(TokenType.END_OF_TEXT, position)

      # try to build tokens   


   def skip_whites(self):
      while (self._reader.get_character()).isspace():
         self._reader.next_character()

   def build_number(self):
      pass

   def build_string(self):
      pass
   
   def build_identifier_or_keyword(self):
      pass

   # operators




