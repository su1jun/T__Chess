import pygame, sys
from game import Game
from square import Square
from move import Move
from setting import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT + HEIGHT_IN * 2) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        while True:
            # show
            self.game.show_bg(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)
            self.game.show_hover(self.screen)
            

            if self.game.dragger.dragging:
                self.game.dragger.update_blit(self.screen)

            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.MOUSEBUTTONDOWN: # click
                    self.game.dragger.update_mouse(event.pos) # position
                    
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
                            self.game.board.calc_moves(piece, clicked_row, clicked_col, testing=True)
                            self.game.dragger.save_initial(event.pos)
                            self.game.dragger.drag_piece(piece)
                            
                    # show
                    self.game.show_bg(self.screen)
                    self.game.show_last_move(self.screen)
                    self.game.show_moves(self.screen)
                    self.game.show_pieces(self.screen)
                    self.game.show_hover(self.screen)
                
                elif event.type == pygame.MOUSEMOTION: # mouse motion
                    motion_row = (event.pos[1] - HEIGHT_IN) // SQSIZE
                    motion_row = max(motion_row, 0)
                    motion_row = min(motion_row, 7)
                    motion_col = event.pos[0] // SQSIZE

                    self.game.set_hover(motion_row, motion_col)

                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos)

                        # show
                        self.game.show_bg(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)
                        self.game.show_hover(self.screen)

                        self.game.dragger.update_blit(self.screen)
                
                elif event.type == pygame.MOUSEBUTTONUP: # click release
                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos)

                        released_row = (self.game.dragger.mouseY - HEIGHT_IN) // SQSIZE
                        released_row = max(released_row, 0)
                        released_row = min(released_row, 7)
                        released_col = self.game.dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(self.game.dragger.initial_row, self.game.dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if self.game.board.valid_move(self.game.dragger.piece, move):
                            # normal capture
                            captured = self.game.board.squares[released_row][released_col].has_piece()
                            self.game.board.move(self.game.dragger.piece, move)

                            self.game.board.set_true_en_passant(self.game.dragger.piece)                            

                            # sounds
                            self.game.play_sound(captured)

                            # show
                            self.game.show_bg(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_pieces(self.screen)

                            # next turn
                            self.game.next_turn()
                    
                    self.game.dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        self.game.change_theme()

                     # changing themes
                    if event.key == pygame.K_r:
                        self.game.reset()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()