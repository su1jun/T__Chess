import os

class Piece:
    def __init__(self, name, color, texture=None, texture_rect=None):
        self.name = name
        self.color = color
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
        super().__init__('pawn', color)

    def __str__(self):
        s = super().__str__()
        return s

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color)

class King(Piece):
    def __init__(self, color):
        self.castling = False
        super().__init__('king', color)
    
    def __str__(self):
        s = super().__str__()
        if self.castling:
            s += "/T"
        else:
            s += "/F"
        return s