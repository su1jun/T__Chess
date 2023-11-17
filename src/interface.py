import os
from piece import *

class Interface:

    def __init__(self, name, color, time = 45):
        self.name = name
        self.color = color
        self.time = time
        self.name_bar_img = os.path.join(f'assets/images/img-interface/name_bar.png')
        self.timer_img = os.path.join(f'assets/images/img-interface/timer.png')
        self.surrender_img = os.path.join(f'assets/images/img-interface/surrender.png')
        self.kiled_pieces = []
        self.set_kiled()

    def set_kiled(self):
        self.kiled_pieces.append(Dummy_Piece(None, self.color, 1.5))
        self.kiled_pieces.append(Dummy_Piece(None, self.color, 3.05))
        self.kiled_pieces.append(Dummy_Piece(None, self.color, 4))
        self.kiled_pieces.append(Dummy_Piece(None, self.color, 6))
        self.kiled_pieces.sort(key=lambda x : abs(x.value))

    def clear_kiled(self):
        self.kiled_pieces = []

    def add_kiled(self, piece):
        self.kiled_pieces.append(piece)
        self.kiled_pieces.sort(key=lambda x : abs(x.value))