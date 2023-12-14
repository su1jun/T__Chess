import pygame, sys
from game import Game
from square import Square
from move import Move
from chessbot import ChessBot
from piece import *
from setting import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT + HEIGHT_IN * 2) )
        pygame.display.set_caption('Chess')

        # 1 page, 2 page (arrow)
        self.btn_1 = False
        self.btn_2 = False
        self.btn_1_hover = False
        self.btn_2_hover = False

        # 2 page (computer)
        self.com_btn_1 = True
        self.com_btn_2 = False

        self.btn_3 = False
        self.btn_3_hover = False

        # 3 page
        self.game = Game()
        self.game_mode = 1 # 0 : normal, 1 : computer(black)

        self.bot = ChessBot()
        self.computer_turn = 0

        self.move_count = 0
        self.theme_change = False
        self.voice_change = False
        self.game_end = False
        self.reversed = False

    def mainloop(self):
        while True:
            self.game.show_title(self.screen)
            self.game.show_title_btn(self.screen, self.btn_1_hover, self.btn_2_hover)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: # click
                    mouseX, mouseY = event.pos
                    self.btn_1 = False
                    self.btn_2 = False
                    if WIDTH // 2 - 145 < mouseX and mouseX < WIDTH // 2 + 155:
                        if 360 + HEIGHT_IN < mouseY and mouseY < 480 + HEIGHT_IN:
                            self.btn_1 = True
                            self.btn_1_hover = True
                            self.game.config.click_sound.play()

                        elif 520 + HEIGHT_IN < mouseY and mouseY < 640 + HEIGHT_IN:
                            self.btn_2 = True
                            self.btn_2_hover = True
                            self.game.config.click_sound.play()

                    self.game.show_title(self.screen)
                    self.game.show_title_btn(self.screen, self.btn_1_hover, self.btn_2_hover)
                
                elif event.type == pygame.MOUSEMOTION: # mouse motion
                    mouseX, mouseY = event.pos
                    self.btn_1_hover = False
                    self.btn_2_hover = False
                    if WIDTH // 2 - 145 < mouseX and mouseX < WIDTH // 2 + 155:
                        if 360 + HEIGHT_IN < mouseY and mouseY < 480 + HEIGHT_IN:
                            self.btn_1_hover = True

                        elif 520 + HEIGHT_IN < mouseY and mouseY < 640 + HEIGHT_IN:
                            self.btn_2_hover = True

                    self.game.show_title(self.screen)
                    self.game.show_title_btn(self.screen, self.btn_1_hover, self.btn_2_hover)
                
                elif event.type == pygame.MOUSEBUTTONUP: # click release
                    if WIDTH // 2 - 145 < mouseX and mouseX < WIDTH // 2 + 155:
                        if 360 + HEIGHT_IN < mouseY and mouseY < 480 + HEIGHT_IN:
                            if self.btn_1:
                                self.settingloop()

                        elif 520 + HEIGHT_IN < mouseY and mouseY < 640 + HEIGHT_IN:
                            if self.btn_2:
                                self.game_mode = 0
                                # start game
                                self.gameloop()
                                
                    self.btn_1 = False
                    self.btn_2 = False

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def settingloop(self):
        while True:
            self.game.show_title(self.screen)
            self.game.show_setting_btn(self.screen, self.btn_1_hover, self.btn_2_hover, self.com_btn_1, self.com_btn_2, self.btn_3_hover)
            self.game.show_level(self.screen, self.bot.level)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: # click
                    mouseX, mouseY = event.pos
                    self.btn_1 = False
                    self.btn_2 = False
                    self.btn_3 = False
                    if 300 + HEIGHT_IN < mouseY and mouseY < 370 + HEIGHT_IN:
                        if WIDTH // 2 - 180 < mouseX and mouseX < WIDTH // 2 - 120:
                            self.btn_1 = True
                            self.btn_1_hover = True
                            self.game.config.click_sound.play()

                        elif WIDTH // 2 + 120 < mouseX and mouseX < WIDTH // 2 + 180:
                            self.btn_2 = True
                            self.btn_2_hover = True
                            self.game.config.click_sound.play()

                    elif 390 + HEIGHT_IN < mouseY and mouseY < 550 + HEIGHT_IN:
                        if WIDTH // 2 - 155 < mouseX and mouseX < WIDTH // 2 - 45:
                            self.com_btn_1 = True
                            self.com_btn_2 = False
                            self.game.config.click_sound.play()

                        elif WIDTH // 2 + 45 < mouseX and mouseX < WIDTH // 2 + 155:
                            self.com_btn_1 = False
                            self.com_btn_2 = True
                            self.game.config.click_sound.play()

                    elif 580 + HEIGHT_IN < mouseY and mouseY < 700 + HEIGHT_IN:
                        if WIDTH // 2 - 145 < mouseX and mouseX < WIDTH // 2 + 155:
                            self.btn_3 = True
                            self.btn_3_hover = True
                            self.game.config.click_sound.play()
                    
                    self.game.show_title(self.screen)
                    self.game.show_setting_btn(self.screen, self.btn_1_hover, self.btn_2_hover, self.com_btn_1, self.com_btn_2, self.btn_3_hover)
                    self.game.show_level(self.screen, self.bot.level)
                
                elif event.type == pygame.MOUSEMOTION: # mouse motion
                    mouseX, mouseY = event.pos
                    self.btn_1_hover = False
                    self.btn_2_hover = False
                    self.btn_3_hover = False
                    if 300 + HEIGHT_IN < mouseY and mouseY < 370 + HEIGHT_IN:
                        if WIDTH // 2 - 180 < mouseX and mouseX < WIDTH // 2 - 120:
                            self.btn_1_hover = True

                        elif WIDTH // 2 + 120 < mouseX and mouseX < WIDTH // 2 + 180:
                            self.btn_2_hover = True

                    elif 580 + HEIGHT_IN < mouseY and mouseY < 700 + HEIGHT_IN:
                        if WIDTH // 2 - 145 < mouseX and mouseX < WIDTH // 2 + 155:
                            self.btn_3_hover = True

                    self.game.show_title(self.screen)
                    self.game.show_setting_btn(self.screen, self.btn_1_hover, self.btn_2_hover, self.com_btn_1, self.com_btn_2, self.btn_3_hover)
                    self.game.show_level(self.screen, self.bot.level)
                
                elif event.type == pygame.MOUSEBUTTONUP: # click release
                    if 300 + HEIGHT_IN < mouseY and mouseY < 370 + HEIGHT_IN:
                        if WIDTH // 2 - 180 < mouseX and mouseX < WIDTH // 2 - 120:
                            if self.btn_1 and self.bot.level > 1:
                                self.bot.level -= 1

                        elif WIDTH // 2 + 120 < mouseX and mouseX < WIDTH // 2 + 180:
                            self.btn_2_hover = True
                            if self.btn_2 and self.bot.level < 20:
                                self.bot.level += 1

                    elif 580 + HEIGHT_IN < mouseY and mouseY < 700 + HEIGHT_IN:
                        if WIDTH // 2 - 145 < mouseX and mouseX < WIDTH // 2 + 155:
                            if self.btn_3_hover:
                                if self.com_btn_1:
                                    self.game_mode = 2
                                    self.computer_turn = 1
                                    self.game.show_bg(self.screen)
                                    self.game.show_moves(self.screen)
                                    self.game.show_pieces(self.screen)
                                    self.game.show_hover(self.screen)
                                    self.game.show_interface(self.screen, self.reversed, self.game_mode, self.bot.level)
                                    pygame.display.update()
                                else:
                                    self.game_mode = 1
                                self.bot.initial_level()
                                # start game
                                self.gameloop()

                    self.btn_1 = False
                    self.btn_2 = False
                    self.btn_3 = False

                # back to main
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if not self.game.dragger.dragging:
                            self.mainloop()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def gameloop(self):
        self.game.config.start_sound.play()
        while True:
            # show
            self.game.show_bg(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_check(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)
            self.game.show_hover(self.screen)
            self.game.show_interface(self.screen, self.reversed, self.game_mode, self.bot.level)
            if self.game_end: self.game.show_game_end(self.screen)
            
            if self.game.dragger.dragging:
                self.game.dragger.update_blit(self.screen, self.reversed)

            if self.game_mode == 0 or self.computer_turn == 0:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN: # click
                        self.game.dragger.update_mouse(event.pos, self.reversed) # position
                        # bounded pos
                        clicked_row = (self.game.dragger.mouseY - HEIGHT_IN) // SQSIZE
                        clicked_row = max(clicked_row, 0)
                        clicked_row = min(clicked_row, 7)
                        clicked_col = self.game.dragger.mouseX // SQSIZE
                        # if clicked square has a piece ?
                        if self.game.board.squares[clicked_row][clicked_col].has_piece():
                            piece = self.game.board.squares[clicked_row][clicked_col].piece
                            # valid piece (color) ?
                            if piece.color == self.game.next_player:
                                self.game.board.calc_moves(piece, clicked_row, clicked_col, testing=False)
                                self.game.dragger.save_initial(event.pos, self.reversed)
                                self.game.dragger.drag_piece(piece)
                                
                        # show
                        self.game.show_bg(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_check(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)
                        self.game.show_interface(self.screen, self.reversed, self.game_mode, self.bot.level)
                        if self.game_end: self.game.show_game_end(self.screen)
                    
                    elif event.type == pygame.MOUSEMOTION: # mouse motion
                        motion_row = (event.pos[1] - HEIGHT_IN) // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        motion_row = max(motion_row, 0)
                        motion_row = min(motion_row, 7)

                        motion_col = max(motion_col, 0)
                        motion_col = min(motion_col, 7)

                        self.game.set_hover(motion_row, motion_col)

                        if self.game.dragger.dragging:
                            self.game.dragger.update_mouse(event.pos, self.reversed)

                            # show
                            self.game.show_bg(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_check(self.screen)
                            self.game.show_moves(self.screen)
                            self.game.show_pieces(self.screen)
                            self.game.show_hover(self.screen)
                            self.game.show_interface(self.screen, self.reversed, self.game_mode, self.bot.level)
                            if self.game_end: self.game.show_game_end(self.screen)

                            self.game.dragger.update_blit(self.screen, self.reversed)
                    
                    elif event.type == pygame.MOUSEBUTTONUP: # click release
                        if self.game.dragger.dragging:
                            self.game.dragger.update_mouse(event.pos, self.reversed)

                            released_row = (self.game.dragger.mouseY - HEIGHT_IN) // SQSIZE
                            released_row = max(released_row, 0)
                            released_row = min(released_row, 7)
                            released_col = self.game.dragger.mouseX // SQSIZE
                            released_col = max(released_col, 0)
                            released_col = min(released_col, 7)

                            initial = Square(self.game.dragger.initial_row, self.game.dragger.initial_col)
                            final = Square(released_row, released_col, self.game.board.squares[released_row][released_col].piece)
                            chk_move = Move(initial, final)
                            move = self.game.board.valid_move(self.game.dragger.piece, chk_move)
                            # valid move ?
                            if move:
                                captured = self.game.board.squares[released_row][released_col].has_piece()
                                checked = self.game.board.on_check(self.game.dragger.piece, move)

                                # castling to checked
                                if isinstance(self.game.dragger.piece, King):
                                    castling_bool = (abs(initial.col - final.col) == 2)
                                    if castling_bool:
                                        side = (final.col - initial.col) < 0 # True : left, False : right

                                        if side:
                                            rook = self.game.board.squares[final.row][0].piece
                                            # rook move
                                            initial = Square(final.row, 0)
                                            final = Square(final.row, 3)
                                            move_Rook = Move(initial, final)
                                        else:
                                            rook = self.game.board.squares[final.row][7].piece
                                            # rook move
                                            initial = Square(final.row, 7)
                                            final = Square(final.row, 5)
                                            move_Rook = Move(initial, final)

                                        checked = (checked or self.game.board.on_check(rook, move_Rook))

                                if captured:
                                    piece = self.game.board.squares[released_row][released_col].piece
                                    self.game.death_pieces[piece.color][piece.name] += 1

                                # normal capture
                                self.game.board.move(self.game.dragger.piece, move)
                                checkmated, stalemated = self.game.board.on_mate(self.game.dragger.piece)

                                # en_passant?
                                if self.game.board.log_stack:
                                    final = self.game.board.log_stack[-1][1].final
                                    if isinstance(piece, Pawn):
                                        if final.en_passant:
                                            reversed_color = 'black' if self.game.next_player == 'white' else 'white'
                                            self.game.death_pieces[reversed_color]["pawn"] += 1

                                # sounds
                                self.game.play_sound(captured, checked, stalemated, checkmated)
                                
                                if checkmated or stalemated: self.game_end = True

                                # show
                                self.game.show_bg(self.screen)
                                self.game.show_last_move(self.screen)
                                self.game.show_check(self.screen)
                                self.game.show_pieces(self.screen)
                                self.game.show_interface(self.screen, self.reversed, self.game_mode, self.bot.level)
                                if self.game_end: self.game.show_game_end(self.screen)

                                self.move_count += 1
                                self.game.next_turn()
                                # next turn
                                if self.game_mode > 0:
                                    self.computer_turn = 1

                        self.game.dragger.undrag_piece()
                        self.game.show_pieces(self.screen)
                    
                    # key press
                    elif event.type == pygame.KEYDOWN:
                        #  back move
                        if event.key == pygame.K_q:
                            if not self.game.dragger.dragging:
                                if self.game.board.log_stack:
                                    if self.game.board.log_stack[-1][1].final.has_piece():       
                                        piece = self.game.board.log_stack[-1][1].final.piece
                                        self.game.death_pieces[piece.color][piece.name] -= 1

                                    if self.game_end: self.game_end = False

                                    self.move_count -= 1
                                    self.game.board.back_move()
                                    self.game.next_turn()

                                    if self.game_mode > 0:
                                        if self.game.board.log_stack:
                                            if self.game.board.log_stack[-1][1].final.has_piece():
                                                piece = self.game.board.log_stack[-1][1].final.piece
                                                self.game.death_pieces[piece.color][piece.name] -= 1

                                        if self.game_end: self.game_end = False
                                        
                                        self.move_count -= 1
                                        self.game.board.back_move()
                                        self.game.next_turn()

                        # self.game.config.show_reverse board
                        if event.key == pygame.K_w:
                            if not self.game.dragger.dragging:
                                if self.reversed:
                                    self.game.config.show_reverse = 0
                                    self.reversed = False
                                else:
                                    self.game.config.show_reverse = 7
                                    self.reversed = True
                        
                        # changing themes
                        if event.key == pygame.K_a:
                            self.game.change_theme()

                        # changing sound
                        if event.key == pygame.K_s:
                            self.game.config.change_sound()
                            self.game.config.change_voice.play()

                        # changing reset
                        if event.key == pygame.K_r:
                            self.game_end = False
                            self.theme_change = self.game.config.idx == 1
                            self.voice_change = self.game.config.idx2 == 1
                            self.game.reset()
                            if self.reversed:
                                self.game.config.show_reverse = 7
                            else:
                                self.game.config.show_reverse = 0

                            if self.game_mode == 2:
                                self.computer_turn = 1
                                self.game.show_bg(self.screen)
                                self.game.show_moves(self.screen)
                                self.game.show_pieces(self.screen)
                                self.game.show_hover(self.screen)
                                self.game.show_interface(self.screen, self.reversed, self.game_mode, self.bot.level)
                                pygame.display.update()

                            self.move_count = 0
                            self.game.config.start_sound.play()
                            if self.theme_change: self.game.change_theme()
                            if self.voice_change: self.game.config.change_sound()

                        # back to main
                        if event.key == pygame.K_BACKSPACE:
                            if not self.game.dragger.dragging:
                                self.theme_change = self.game.config.idx == 1
                                self.voice_change = self.game.config.idx2 == 1
                                self.game.reset()
                                if self.reversed:
                                    self.game.config.show_reverse = 7
                                else:
                                    self.game.config.show_reverse = 0
                                self.game_end = False
                                self.move_count = 0
                                if self.theme_change: self.game.change_theme()
                                if self.voice_change: self.game.config.change_sound()
                                self.mainloop()

                    # quit application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            elif self.computer_turn:
                pygame.display.update()
                fen = self.game.board.board_to_fen()
                if self.game_mode == 1:
                    fen += ' b'
                elif self.game_mode == 2:
                    fen += ' w'

                # castling?
                bq_castling = ''
                bk_castling = ''
                if self.game.board.squares[0][4].has_piece():
                    if isinstance(self.game.board.squares[0][4].piece, King) and self.game.board.squares[0][4].piece.color == 'black':
                        if not self.game.board.squares[0][4].piece.moved:
                            if self.game.board.squares[0][0].has_piece():
                                if isinstance(self.game.board.squares[0][0].piece, Rook) and self.game.board.squares[0][0].piece.color == 'black':
                                    if not self.game.board.squares[0][0].piece.moved:
                                        bq_castling = 'q'

                            if self.game.board.squares[0][7].has_piece():
                                if isinstance(self.game.board.squares[0][7].piece, Rook) and self.game.board.squares[0][7].piece.color == 'black':
                                    if not self.game.board.squares[0][7].piece.moved:
                                        bk_castling = 'k'

                wq_castling = ''
                wk_castling = ''
                if self.game.board.squares[7][4].has_piece():
                    if isinstance(self.game.board.squares[7][4].piece, King) and self.game.board.squares[7][4].piece.color == 'white':
                        if not self.game.board.squares[7][4].piece.moved:
                            if self.game.board.squares[7][0].has_piece():
                                if isinstance(self.game.board.squares[7][0].piece, Rook) and self.game.board.squares[7][0].piece.color == 'white':
                                    if not self.game.board.squares[7][0].piece.moved:
                                        wq_castling = 'Q'

                            if self.game.board.squares[7][7].has_piece():
                                if isinstance(self.game.board.squares[7][7].piece, Rook) and self.game.board.squares[7][7].piece.color == 'white':
                                    if not self.game.board.squares[7][7].piece.moved:
                                        wk_castling = 'K'
                castling_str = wk_castling + wq_castling + bk_castling + bq_castling
                if not castling_str: castling_str = '-'
                fen += ' ' + castling_str
                
                en_passant_location = ' -'
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.game.board.squares[row][col].en_passant:
                            en_passant_location = ' ' + get_alphacol(col) + str(8 - row)
                            break

                fen += en_passant_location
                fen += ' 0 '
                fen += str(self.move_count)
                # print("Stockfish input :", fen)
                best_move = self.bot.cal_move(fen)
                # print(f"best_move : {best_move}")
                ac1, ac2 = best_move[0], best_move[1]
                bc1, bc2 = best_move[2], best_move[3]
                
                try:
                    ir = 8 - int(ac2)
                    ic = get_number(ac1)
                    rr = 8 - int(bc2)
                    rc = get_number(bc1)
                except:
                    print("Game Over")

                # self.move_count += 1
                # self.game.next_turn()
                
                piece = self.game.board.squares[ir][ic].piece

                self.game.board.calc_moves(piece, ir, ic, testing=False)
                self.game.dragger.initial_row = ir
                self.game.dragger.initial_col = ic
                self.game.dragger.drag_piece(piece)

                released_row = rr
                released_col = rc

                initial = Square(self.game.dragger.initial_row, self.game.dragger.initial_col)
                final = Square(released_row, released_col, self.game.board.squares[released_row][released_col].piece)
                chk_move = Move(initial, final)
                move = self.game.board.valid_move(self.game.dragger.piece, chk_move)
                captured = self.game.board.squares[released_row][released_col].has_piece()
                checked = self.game.board.on_check(self.game.dragger.piece, move)

                if captured:
                    piece = self.game.board.squares[released_row][released_col].piece
                    self.game.death_pieces[piece.color][piece.name] += 1

                # castling to checked
                if isinstance(self.game.dragger.piece, King):
                    castling_bool = (abs(initial.col - final.col) == 2)
                    if castling_bool:
                        side = (final.col - initial.col) < 0 # True : left, False : right

                        if side:
                            rook = self.game.board.squares[final.row][0].piece
                            # rook move
                            initial = Square(final.row, 0)
                            final = Square(final.row, 3)
                            move_Rook = Move(initial, final)
                        else:
                            rook = self.game.board.squares[final.row][7].piece
                            # rook move
                            initial = Square(final.row, 7)
                            final = Square(final.row, 5)
                            move_Rook = Move(initial, final)

                        checked = (checked or self.game.board.on_check(rook, move_Rook))

                # normal capture
                self.game.board.move(self.game.dragger.piece, move)
                checkmated, stalemated = self.game.board.on_mate(self.game.dragger.piece)

                # en_passant?
                if self.game.board.log_stack:
                    final = self.game.board.log_stack[-1][1].final
                    if isinstance(piece, Pawn):
                        if final.en_passant:
                            reversed_color = 'black' if self.game.next_player == 'white' else 'white'
                            self.game.death_pieces[reversed_color]["pawn"] += 1
                
                # sounds
                self.game.play_sound(captured, checked, stalemated, checkmated)
                
                if checkmated or stalemated: self.game_end = True

                # show
                self.game.show_bg(self.screen)
                self.game.show_last_move(self.screen)
                self.game.show_check(self.screen)
                self.game.show_pieces(self.screen)
                self.game.show_interface(self.screen, self.reversed, self.game_mode, self.bot.level)
                if self.game_end: self.game.show_game_end(self.screen)

                self.move_count += 1
                self.game.next_turn()
                self.computer_turn = 0

                self.game.dragger.undrag_piece()

            pygame.display.update()

main = Main()
main.mainloop()