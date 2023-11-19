import pygame
from setting import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def __str__(self):
        s = ''
        s += f"{self.piece}, {self.dragging}, "
        final_col = self.mouseX // SQSIZE
        final_row = self.mouseY // SQSIZE
        final_row = max(final_row, 0)
        final_row = min(final_row, 7)
        s += f"{ALPHACOLS[self.initial_col]}{8 - self.initial_row} -> {ALPHACOLS[final_col]}{8 - final_row}"
        return s

    # blit method
    def update_blit(self, surface):
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # img
        img = pygame.image.load(texture)
        # rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)

    # other methods
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos # (xcor, ycor)

    def save_initial(self, pos):
        initial_row = (pos[1] - HEIGHT_IN) // SQSIZE
        initial_row = max(initial_row, 0)
        initial_row = min(initial_row, 7)
        self.initial_row = initial_row
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
