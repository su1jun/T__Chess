import pygame
from board import Board
from dragger import Dragger
from square import Square
from setting import *
from piece import *
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
                    lbl = self.config.font.render(get_alphacol(col), 1, color)
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
                        img_center = abs(col - self.config.show_reverse) * SQSIZE + SQSIZE // 2, abs(row - self.config.show_reverse) * SQSIZE + SQSIZE // 2 + HEIGHT_IN
                        # print(f"{piece}, 위치 {abs(col - self.config.show_reverse)}, {abs(row - self.config.show_reverse)}")
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_inter(self, surface):
            pass

    def show_moves(self, surface): # +attack mark
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                final = move.final

                img_center = ((abs(final.col - self.config.show_reverse) + 0.5) * SQSIZE, (abs(final.row - self.config.show_reverse) + 0.5) * SQSIZE + HEIGHT_IN)
                color = self.config.theme.bg.light if (final.row + final.col) % 2 == 0 else self.config.theme.bg.dark
                if final.has_enemy_piece(self.next_player):
                    if final.is_en_passant() and (final.row == 2 or final.row == 5):
                        temp = 1 if self.next_player == 'white' else -1 # white == 1, black == -1
                        color = self.config.theme.bg.light if (final.row + temp + final.col) % 2 == 0 else self.config.theme.bg.dark

                        img_center = ((abs(final.col - self.config.show_reverse) + 0.5) * SQSIZE, (abs(final.row - self.config.show_reverse) + temp + 0.5) * SQSIZE + HEIGHT_IN)
                        img = pygame.image.load(self.config.attack_point)
                        img_rect = img.get_rect(center=img_center)

                        surface.fill(color, img_rect)
                        self.show_last_move(surface, final)
                        surface.blit(img, img_rect)

                        img_center = (((final.col - self.config.show_reverse) + 0.5) * SQSIZE, ((final.row - self.config.show_reverse) + 0.5) * SQSIZE + HEIGHT_IN)
                        color = self.config.theme.bg.light if (final.row + final.col) % 2 == 0 else self.config.theme.bg.dark
                        img = pygame.image.load(self.config.move_point)
                        img_rect = img.get_rect(center=img_center)
                    else:
                        img = pygame.image.load(self.config.attack_point)
                        img_rect = img.get_rect(center=img_center)
                else:
                    img = pygame.image.load(self.config.move_point)
                    img_rect = img.get_rect(center=img_center)
                #$%
                # surface.fill(color, img_rect)
                # self.show_last_move(surface, move.final)
                surface.blit(img, img_rect)

    def show_last_move(self, surface, move=None):
        # show when rewind
        if self.board.log_stack:
            initial = self.board.log_stack[-1][1].initial
            final = self.board.log_stack[-1][1].final
            if move: # show when the last move location overlay
                if move == initial:
                    color = self.config.theme.trace.light if (initial.row + initial.col) % 2 == 0 else self.config.theme.trace.dark
                    rect = (abs(initial.col - self.config.show_reverse) * SQSIZE, abs(initial.row - self.config.show_reverse) * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)
                elif move == final or move.is_en_passant():
                    color = self.config.theme.trace.light if (final.row + final.col) % 2 == 0 else self.config.theme.trace.dark
                    rect = (abs(final.col - self.config.show_reverse) * SQSIZE, abs(final.row - self.config.show_reverse) * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)
            else:
                for pos in [initial, final]:
                    color = self.config.theme.trace.light if (pos.row + pos.col) % 2 == 0 else self.config.theme.trace.dark
                    rect = (abs(pos.col - self.config.show_reverse) * SQSIZE, abs(pos.row - self.config.show_reverse) * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
                    pygame.draw.rect(surface, color, rect)

    def show_check(self, surface):
        if self.board.check_locs:
            for pos in self.board.check_locs:
                color = ATTACK_LIGHT if (pos.row + pos.col) % 2 == 0 else ATTACK_DARK
                rect = (abs(pos.col - self.config.show_reverse) * SQSIZE, abs(pos.row - self.config.show_reverse) * SQSIZE + HEIGHT_IN, SQSIZE, SQSIZE)
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

    def play_sound(self, captured, checked, stalemated, checkmated):
        if checkmated:
            self.config.check_sound.play()
            self.config.checkmate_voice.play()
        elif checked:
            self.config.check_sound.play()
            self.config.check_voice.play()
        elif captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

        if stalemated:
            self.config.stalemate_voice.play()

    def reset(self):
        self.__init__()