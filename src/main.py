import pygame, sys
from game import Game
from square import Square
from move import Move
from piece import *
from setting import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT + HEIGHT_IN * 2) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.theme_change = False
        self.voice_change = False
        self.game_end = False
        self.reversed = False

    def mainloop(self):
        while True:
            # show
            self.game.show_bg(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_check(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)
            self.game.show_hover(self.screen)
            self.game.show_interface(self.screen, self.reversed)
            if self.game_end: self.game.show_game_end(self.screen)
            
            if self.game.dragger.dragging:
                self.game.dragger.update_blit(self.screen, self.reversed)

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
                    self.game.show_interface(self.screen, self.reversed)
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
                        self.game.show_interface(self.screen, self.reversed)
                        if self.game_end: self.game.show_game_end(self.screen)

                        self.game.dragger.update_blit(self.screen, self.reversed)
                
                elif event.type == pygame.MOUSEBUTTONUP: # click release
                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos, self.reversed)

                        released_row = (self.game.dragger.mouseY - HEIGHT_IN) // SQSIZE
                        released_row = max(released_row, 0)
                        released_row = min(released_row, 7)
                        released_col = self.game.dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(self.game.dragger.initial_row, self.game.dragger.initial_col)
                        final = Square(released_row, released_col)
                        chk_move = Move(initial, final)
                        move = self.game.board.valid_move(self.game.dragger.piece, chk_move)
                        # valid move ?
                        if move:
                            captured = self.game.board.squares[released_row][released_col].has_piece()
                            checked = self.game.board.on_check(self.game.dragger.piece, move)

                            if captured:
                                piece = self.game.board.squares[released_row][released_col].piece
                                self.game.death_pieces[piece.color][piece.name] += 1

                            # normal capture
                            self.game.board.move(self.game.dragger.piece, move)
                            checkmated, stalemated = self.game.board.on_mate(self.game.dragger.piece)

                            # en_passant?
                            if self.game.board.log_stack:
                                piece = self.game.board.log_stack[-1][1].final.piece
                                if isinstance(piece, Pawn):
                                    if piece.en_passant:
                                        self.game.death_pieces[piece.color]["pawn"] += 1
                            
                            # sounds
                            self.game.play_sound(captured, checked, stalemated, checkmated)
                            
                            if checkmated or stalemated: self.game_end = True

                            # show
                            self.game.show_bg(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_check(self.screen)
                            self.game.show_pieces(self.screen)
                            self.game.show_interface(self.screen, self.reversed)
                            if self.game_end: self.game.show_game_end(self.screen)

                            # next turn
                            self.game.next_turn()
                    
                    self.game.dragger.undrag_piece()
                
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

                                self.game.next_turn()
                                
                            self.game.board.back_move()

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
                        if self.theme_change: self.game.change_theme()
                        if self.voice_change: self.game.config.change_sound()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()