class Move:
    def __init__(self, initial, final): # initial(.col, .row)
        # initial and final are squares
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'{self.initial.alphacol}{8 - self.initial.row}({self.initial.piece})'
        s += f' -> {self.final.alphacol}{8 - self.final.row}({self.final.piece})'
        return s

    def __eq__(self, other): # other(.initial, .final)
        return self.initial == other.initial and self.final == other.final