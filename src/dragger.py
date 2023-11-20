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
    def update_blit(self, surface, reversed=False):
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # img
        img = pygame.image.load(texture)
        # rect

        img_center = (self.mouseX, self.mouseY)
        if reversed: img_center = (abs(self.mouseX - WIDTH), abs(self.mouseY - (HEIGHT + HEIGHT_IN * 2)))
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)

    # other methods
    def update_mouse(self, pos, reversed=False):
        self.mouseX, self.mouseY = pos # (xcor, ycor)
        if reversed: self.mouseX, self.mouseY = abs(self.mouseX - WIDTH), abs(self.mouseY - (HEIGHT + HEIGHT_IN * 2))
            
    def save_initial(self, pos, reversed=False):
        initial_row = (pos[1] - HEIGHT_IN) // SQSIZE
        initial_col = pos[0] // SQSIZE
        if reversed:
            initial_row = (abs(pos[1] - (HEIGHT + HEIGHT_IN))) // SQSIZE
            initial_col = abs(pos[0] - WIDTH) // SQSIZE

        initial_row = max(initial_row, 0)
        initial_row = min(initial_row, 7)
        self.initial_row = initial_row
        self.initial_col = initial_col

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
