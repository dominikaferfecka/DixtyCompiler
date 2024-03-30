class Position:
    def __init__(self, row=1, column=0):
        self._row = row
        self._column = column

    def get_row(self):
        return self._row
    
    def get_column(self):
        return self._column
    
    def get_position(self):
        return f" row: [ {self._row} ], column: [ {self._column} ]"
    
    def increase_row(self):
        self._row = self._row + 1

    def increase_column(self):
        self._column = self._column + 1

    def restart_column(self):
        self._column = 1
    
    def start_next_row(self):
        self.increase_row()
        self.restart_column()