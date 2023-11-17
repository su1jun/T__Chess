import pygame
from board import Board
from dragger import Dragger
from square import Square
from setting import *
from interface import Interface

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.config = Config()
        self.board = Board(self.config)
        self.dragger = Dragger()
        self.interface_white = Interface("player 1", "white")
        self.interface_black = Interface("player 2", "black")

    # blit methods
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                color = self.config.theme.bg.light if (row + col) % 2 == 0 else self.config.theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                # row, label (1, 2, ...)
                if col == 0:
                    color = self.config.theme.bg.dark if row % 2 == 0 else self.config.theme.bg.light
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE + HEIGHT_IN)
                    surface.blit(lbl, lbl_pos)

                # col, label (A, B, ...)
                if row == 7: 
                    color = self.config.theme.bg.dark if (row + col) % 2 == 0 else self.config.theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20 + HEIGHT_IN)
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2 + HEIGHT_IN
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_inter(self, surface):
            pass

    def show_moves(self, surface): # +attack mark
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                img_center = ((move.final.col + 0.5) * SQSIZE, (move.final.row + 0.5) * SQSIZE + HEIGHT_IN)
                color = self.config.theme.bg.light if (move.final.row + move.final.col) % 2 == 0 else self.config.theme.bg.dark
                if move.final.has_enemy_piece(self.next_player):
                    img = pygame.image.load(self.config.attack_point)
                    img_rect = img.get_rect(center=img_center)
                else:
                    img = pygame.image.load(self.config.move_point)
                    img_rect = img.get_rect(center=img_center)
                surface.fill(color, img_rect)
                self.show_last_move(surface, move.final)
                surface.blit(img, img_rect)
                
                # color = (226, 226, 226, 245)
                # circle = ((move.final.col + 0.5) * SQSIZE, (move.final.row + 0.5) * SQSIZE + HEIGHT_IN)
                # pygame.draw.circle(surface, color, circle, SQSIZE//4)

    def show_last_move(self, surface, move=None):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            if move:
                if move == initial:
                    color = self.config.theme.trace.light if (initial.row + initial.col) % 2 == 0 else self.config.theme.trace.dark
                    rect = (initial.col * SQSIZE, initial.row * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)
                elif move == final:
                    color = self.config.theme.trace.light if (final.row + final.col) % 2 == 0 else self.config.theme.trace.dark
                    rect = (final.col * SQSIZE, final.row * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)
            else:
                for pos in [initial, final]:
                    color = self.config.theme.trace.light if (pos.row + pos.col) % 2 == 0 else self.config.theme.trace.dark
                    rect = (pos.col * SQSIZE, pos.row * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False, checked=False):
        print(f"play_sound // captured 여부 : {captured}") #@!
        if checked:
            self.config.check_sound.play()
            self.config.check_voice.play()
        elif captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()