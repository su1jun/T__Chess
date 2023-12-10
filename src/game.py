import pygame
from board import Board
from dragger import Dragger
from square import Square
from setting import *
from piece import *

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.config = Config()
        self.board = Board(self.config)
        self.dragger = Dragger()

        self.death_pieces = {
            "white" : {
                "pawn" : 0,
                "bishop" : 0,
                "knight" : 0,
                "rook" : 0,
                "queen" : 0,
            },
            "black" : {
                "pawn" : 0,
                "bishop" : 0,
                "knight" : 0,
                "rook" : 0,
                "queen" : 0,
            }
        }

    def show_title(self, surface):
        BLACK = (17, 17, 17)
        WHITE = (221, 221, 221)

        box_rect = pygame.Rect(0, 0, WIDTH, HEIGHT_IN)
        pygame.draw.rect(surface, BLACK, box_rect)

        box_rect = pygame.Rect(0, HEIGHT_IN, WIDTH, HEIGHT)
        pygame.draw.rect(surface, WHITE, box_rect)

        box_rect = pygame.Rect(0, HEIGHT + HEIGHT_IN, WIDTH, HEIGHT_IN)
        pygame.draw.rect(surface, BLACK, box_rect)

        img = pygame.image.load(self.config.game_title)
        img_center = WIDTH // 2 + 5, 180 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

    def show_title_btn(self, surface, bool1, bool2):
        if bool1:
            img = pygame.image.load(self.config.people1_btn_gray)
        else:
            img = pygame.image.load(self.config.people1_btn)

        img_center = WIDTH // 2 + 5, 420 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

        if bool2:
            img = pygame.image.load(self.config.people2_btn_gray)
        else:
            img = pygame.image.load(self.config.people2_btn)

        img_center = WIDTH // 2 + 5, 580 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

    def show_setting_btn(self, surface, bool1, bool2, bool3, bool4, bool5):
        if bool1:
            img = pygame.image.load(self.config.left_btn_gray)
        else:
            img = pygame.image.load(self.config.left_btn)
        img_center = WIDTH // 2 - 150, 335 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

        if bool2:
            img = pygame.image.load(self.config.right_btn_gray)
        else:
            img = pygame.image.load(self.config.right_btn)
        img_center = WIDTH // 2 + 150, 335 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

        if bool3:
            img = pygame.image.load(self.config.white_com_selected)
        else:
            img = pygame.image.load(self.config.white_com)
        img_center = WIDTH // 2 - 100, 470 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

        if bool4:
            img = pygame.image.load(self.config.black_com_selected)
        else:
            img = pygame.image.load(self.config.black_com)
        img_center = WIDTH // 2 + 100, 470 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

        if bool5:
            img = pygame.image.load(self.config.people1_btn_gray)
        else:
            img = pygame.image.load(self.config.people1_btn)
        
        img_center = WIDTH // 2 + 5, 640 + HEIGHT_IN
        surface.blit(img, img.get_rect(center=img_center))

    def show_level(self, surface, level):
        BLACK = (17, 17, 17)
        level_str = (2 - len(str(level))) * '0' + str(level)
        lv_font = self.config.lvfont.render(f'Lv : {level_str}', 1, BLACK)
        lv_font_pos = (WIDTH // 2 - 55, 305 + HEIGHT_IN)
        surface.blit(lv_font, lv_font_pos)

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
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_interface(self, surface, reversed, game_mode, level):
        BLACK = (17, 17, 17)
        WHITE = (221, 221, 221)
        GRAY = (77, 77, 77)
        
        if reversed:
            white_rect = 0
            black_rect = HEIGHT + HEIGHT_IN
            white_height = HEIGHT_IN * 0.5
            black_height = HEIGHT + HEIGHT_IN * 1.5
        else:
            white_rect = HEIGHT + HEIGHT_IN
            black_rect = 0
            white_height = HEIGHT + HEIGHT_IN * 1.5
            black_height = HEIGHT_IN * 0.5

        if self.next_player == 'black':
            box_rect = pygame.Rect(0, black_rect, WIDTH, HEIGHT_IN)
            pygame.draw.rect(surface, BLACK, box_rect)

            box_rect = pygame.Rect(0, white_rect, WIDTH, HEIGHT_IN)
            pygame.draw.rect(surface, GRAY, box_rect)

        else:
            box_rect = pygame.Rect(0, black_rect, WIDTH, HEIGHT_IN)
            pygame.draw.rect(surface, GRAY, box_rect)

            box_rect = pygame.Rect(0, white_rect, WIDTH, HEIGHT_IN)
            pygame.draw.rect(surface, BLACK, box_rect)

        box_rect = pygame.Rect(405, 46, 300, 3)
        pygame.draw.rect(surface, WHITE, box_rect)

        box_rect = pygame.Rect(405, HEIGHT + HEIGHT_IN + 46, 300, 3)
        pygame.draw.rect(surface, WHITE, box_rect)

        if game_mode == 1:
            white_side_txt = 'Player'
            black_side_txt = f'Lv.{level} Computer'
        elif game_mode == 2:
            white_side_txt = f'Lv.{level} Computer'
            black_side_txt = 'Player'
        else:
            white_side_txt = 'Player 1'
            black_side_txt = 'Player 2'

        # upper-side #

        # icons
        img = pygame.image.load(self.config.black_icon)
        img_center = SQSIZE // 2 - 15, black_height
        surface.blit(img, img.get_rect(center=img_center))

        # player
        player_font = self.config.interfont.render(black_side_txt, 1, WHITE)
        player_font_pos = (SQSIZE - 25, black_height - 15)
        surface.blit(player_font, player_font_pos)
        
        initial_x = WIDTH - SQSIZE // 2 + 15
        initial_y = black_height - 3
        for pieces in self.death_pieces['white']:
            texture = os.path.join('assets', 'images', f'imgs-30px/white_{pieces}.png')
            cnt = self.death_pieces['white'][pieces]
            for _ in range(cnt):
                img = pygame.image.load(texture)
                img_center = initial_x, initial_y
                surface.blit(img, img.get_rect(center=img_center))
                initial_x -= 15
            if cnt:
                initial_x -= 15

        # bottom-side #
        
        # icons
        img = pygame.image.load(self.config.white_icon)
        img_center = SQSIZE // 2 - 15, white_height
        surface.blit(img, img.get_rect(center=img_center))

        # player
        player_font = self.config.interfont.render(white_side_txt, 1, WHITE)
        player_font_pos = (SQSIZE - 25, white_height - 15)
        surface.blit(player_font, player_font_pos)

        initial_x = WIDTH - SQSIZE // 2 + 15
        initial_y = white_height - 3
        for pieces in self.death_pieces['black']:
            texture = os.path.join('assets', 'images', f'imgs-30px/black_{pieces}.png')
            cnt = self.death_pieces['black'][pieces]
            for _ in range(self.death_pieces['black'][pieces]):
                img = pygame.image.load(texture)
                img_center = initial_x, initial_y
                surface.blit(img, img.get_rect(center=img_center))
                initial_x -= 15
            if cnt:
                initial_x -= 15

    def show_moves(self, surface): # +attack mark
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                initial = move.initial
                final = move.final

                img_center = ((abs(final.col - self.config.show_reverse) + 0.5) * SQSIZE, (abs(final.row - self.config.show_reverse) + 0.5) * SQSIZE + HEIGHT_IN)
                color = self.config.theme.bg.light if (final.row + final.col) % 2 == 0 else self.config.theme.bg.dark
                if final.has_enemy_piece(self.next_player):
                    if final.en_passant and (final.row == 2 or final.row == 5):
                        color = self.config.theme.bg.light if (initial.row + final.col) % 2 == 0 else self.config.theme.bg.dark

                        img_center = ((abs(final.col - self.config.show_reverse) + 0.5) * SQSIZE, (abs(initial.row - self.config.show_reverse) + 0.5) * SQSIZE + HEIGHT_IN)
                        img = pygame.image.load(self.config.attack_point)
                        img_rect = img.get_rect(center=img_center)

                        surface.fill(color, img_rect)
                        self.show_last_move(surface, final)
                        surface.blit(img, img_rect)

                        img_center = ((abs(final.col - self.config.show_reverse) + 0.5) * SQSIZE, (abs(final.row - self.config.show_reverse) + 0.5) * SQSIZE + HEIGHT_IN)
                        color = self.config.theme.bg.light if (final.row + final.col) % 2 == 0 else self.config.theme.bg.dark
                        img = pygame.image.load(self.config.move_point)
                        img_rect = img.get_rect(center=img_center)
                    else:
                        img = pygame.image.load(self.config.attack_point)
                        img_rect = img.get_rect(center=img_center)
                else:
                    img = pygame.image.load(self.config.move_point)
                    img_rect = img.get_rect(center=img_center)
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
                elif move == final or move.en_passant:
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

    def show_game_end(self, surface):
        img_center = (WIDTH // 2, (HEIGHT + HEIGHT_IN * 2) // 2)
        img = pygame.image.load(self.config.game_end)
        img_rect = img.get_rect(center=img_center)
        surface.blit(img, img_rect)

    def reset(self):
        self.__init__()