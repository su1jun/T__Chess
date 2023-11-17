from square import Square
from piece import *
from move import Move
from setting import *

class Board:
    def __init__(self, config):
        # set of first board set
        self.squares = [[0] * ROWS for _ in range(COLS)]
        self.last_move = None
        self.config = config
        self._create()
        self._add_pieces('white') # set of first white piece
        self._add_pieces('black') # set of first black piece

    def move(self, piece, move, testing=False):
        #@!
        if testing:
            logmessage = "test_"
        else:
            logmessage = ""
        logmessage += f"move/{piece.__class__.__name__} 의" + \
              f"{move.initial.alphacol}{move.initial.row} -> {move.final.alphacol}{move.final.row} 이동"
        if move.initial.has_piece():
            logmessage += f"/{move.initial.piece.__class__.__name__}, {move.initial.piece.color}"
        else:
            logmessage += "/None"

        if move.final.has_piece():
            logmessage += f"/{move.final.piece.__class__.__name__}, {move.final.piece.color}"
        else:
            logmessage += "/None"
        print(logmessage)    
        # print(f"testing 요청 여부 : {testing}") #@!
        
        initial = move.initial
        final = move.final

        # console board move update
        if testing:
            pass
            self.squares[initial.row][initial.col].piece = initial.piece
        else:
            self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0:
                en_passant_empty = self.squares[final.row][final.col].isempty()
                if en_passant_empty:
                    # console board move update
                    # if testing:
                    #     self.squares[initial.row][initial.col].piece = None
                    self.squares[initial.row][initial.col + diff].piece = None
                    self.squares[final.row][final.col].piece = piece
                    if not testing:
                        sound = self.config.capture_sound
                        print("몇 번뜨니? capture_sound") #@!
                        sound.play()
            
            # pawn promotion
            else:
                check_promotion = (final.row == 0 or final.row == 7)
                if check_promotion:
                    self.squares[final.row][final.col].piece = Queen(piece.color)
                    if not testing:
                        sound = self.config.promotion_sound
                        voice = self.config.promotion_voice
                        print("몇 번뜨니? promote_sound") #@!
                        sound.play()
                        voice.play()

        if not testing:
            # king castling
            if isinstance(piece, King):
                castling_bool = (abs(initial.col - final.col) == 2)
                if castling_bool:
                    diff = final.col - initial.col
                    rook = piece.left_rook if (diff < 0) else piece.right_rook
                    self.move(rook, rook.moves[-1])

                    sound = self.config.castling_sound
                    voice = self.config.castling_voice
                    sound.play()
                    voice.play()

            # move
            piece.moved = True

            # set last move
            self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True

    def in_check(self, piece, move):
        self.move(piece, move, testing=True)
        resulted = False
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_enemy_piece(piece.color):
                    enemy_piece = self.squares[row][col].piece
                    self.calc_moves(enemy_piece, row, col, testing=True)
                    for m in enemy_piece.moves:
                        if isinstance(m.final.piece, King):
                            print(f"check2/{piece.__class__.__name__} 의 {move.initial.alphacol}{move.initial.row} -> {move.final.alphacol}{move.final.row} 이동 결과 : Checked") #@!
                            resulted = True
        
        move.initial, move.final = move.final, move.initial
        self.move(piece, move, testing=True)
        move.initial, move.final = move.final, move.initial
        if not resulted: #@!
            print(f"check2/{piece.__class__.__name__} 의 {move.initial.alphacol}{move.initial.row} -> {move.final.alphacol}{move.final.row} 이동 결과 : Not Check") #@!
        return resulted
    
    def in_check_on(self, piece, move):
        self.move(piece, move, testing=True)
        resulted = False
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(piece.color):
                    team_piece = self.squares[row][col].piece
                    self.calc_moves(team_piece, row, col, testing=True)
                    for m in team_piece.moves:
                        if isinstance(m.final.piece, King):
                            print(f"check1/{piece.__class__.__name__} 의 {move.initial.alphacol}{move.initial.row} -> {move.final.alphacol}{move.final.row} 이동 결과 : Checked") #@!
                            resulted = True
        
        move.initial, move.final = move.final, move.initial
        self.move(piece, move, testing=True)
        move.initial, move.final = move.final, move.initial
        if not resulted: #@!
            print(f"check1/{piece.__class__.__name__} 의 {move.initial.alphacol}{move.initial.row} -> {move.final.alphacol}{move.final.row} 이동 결과 : Not Check") #@!
        return resulted
    
    def calc_moves(self, piece, row, col, testing=False):
        '''
            Calculate all the possible (valid) moves of an specific piece on a specific position
        '''
        def pawn_moves():
            steps = 1 if piece.moved else 2 # steps

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if testing:
                            piece.add_move(move) # append new move
                        else:
                            if not self.in_check(piece, move):
                                piece.add_move(move) # append new move
                            
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if testing:
                            piece.add_move(move) # append new move
                        else:
                            if not self.in_check(piece, move):
                                piece.add_move(move) # append new move

            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en pessant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col-1, enpassant=True)
                            # create a new move
                            move = Move(initial, final)
                            
                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                if not self.in_check(piece, move):
                                    piece.add_move(move) # append new move
            
            # right en pessant
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col+1, enpassant=True)
                            # create a new move
                            move = Move(initial, final)
                            
                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                if not self.in_check(piece, move):
                                    piece.add_move(move) # append new move


        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move_row, possible_move_col in possible_moves:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty():
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if testing:
                            piece.add_move(move) # append new move
                        else:
                            if not self.in_check(piece, move):
                                piece.add_move(move) # append new move

                    elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if testing:
                            piece.add_move(move) # append new move
                        else:
                            if not self.in_check(piece, move):
                                piece.add_move(move) # append new move

        def straightline_moves(incrs):
            for row_incr, col_incr in incrs:
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                if not self.in_check(piece, move):
                                    piece.add_move(move) # append new move

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                if not self.in_check(piece, move):
                                    piece.add_move(move) # append new move
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else: break

                    # incrementing incrs
                    possible_move_row += row_incr
                    possible_move_col += col_incr

        def king_moves():
            # 8 possible moves
            possible_moves = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move_row, possible_move_col in possible_moves:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)
                        # check potencial checks
                        if testing:
                            piece.add_move(move) # append new move
                        else:
                            if not self.in_check(piece, move):
                                piece.add_move(move) # append new move

            # castling moves
            if not piece.moved:
                # left side castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            else:
                                # king move
                                initial = Square(row, col)
                                final = Square(row, c)
                                moveK = Move(initial, final)

                                if self.in_check(piece, moveK):
                                    break

                        else:
                            # adds left rook to king
                            piece.left_rook = left_rook

                            # rook move
                            initial = Square(row, 0)
                            final = Square(row, 3)
                            moveR = Move(initial, final)

                            # king move
                            initial = Square(row, col)
                            final = Square(row, 2)
                            moveK = Move(initial, final)

                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                if not self.in_check(piece, move):
                                    piece.add_move(move) # append new move

                # right side castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            else:
                                # king move
                                initial = Square(row, col)
                                final = Square(row, c)
                                moveK = Move(initial, final)

                                if self.in_check(piece, moveK):
                                    break

                        else:
                            # adds right rook to king
                            piece.right_rook = right_rook

                            # rook move
                            initial = Square(row, 7)
                            final = Square(row, 5)
                            moveR = Move(initial, final)

                            # king move
                            initial = Square(row, col)
                            final = Square(row, 6)
                            moveK = Move(initial, final)

                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                if not self.in_check(piece, move):
                                    piece.add_move(move) # append new move
        # clear valid moves
        piece.clear_moves()

        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ])

        elif isinstance(piece, King): 
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))