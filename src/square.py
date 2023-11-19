from piece import *
from setting import *

class Square:
    def __init__(self, row, col, piece=None, enpassant=False):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = ALPHACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __str__(self):
        s = ''
        s += f'({self.alphacol}{8 - self.row} '
        s += f'{self.piece})'
        return s

    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        '''
            > empty (1) or enemy (!= color)
        '''
        return self.isempty() or self.has_enemy_piece(color)
    
    def is_en_passant(self):
        return isinstance(self.piece, Pawn) and self.piece.en_passant

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        
        return True

    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]