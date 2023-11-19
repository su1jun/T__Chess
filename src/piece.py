import os

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1 # white == 1, black == -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def __str__(self):
        s = ''
        s += f'{self.__class__.__name__}, '
        s += f'{self.color}'
        return s

    def set_texture(self, size=80):
        self.texture = os.path.join(
            'assets', 'images', f'imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Dummy_Piece:
    def __init__(self, name = None, color = "white", value = 0):
        self.name = name
        self.color = color
        self.value = value

class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0)

    def __str__(self):
        s = super().__str__()
        if self.en_passant:
            s += "_T"
        else:
            s += "_F"
        return s

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.1)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        self.castling = False
        super().__init__('king', color, 10000.0)