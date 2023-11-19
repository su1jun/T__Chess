from square import Square
from piece import *
from move import Move
from setting import *

class Board:
    def __init__(self, config):
        # set of first board set
        self.squares = [[0] * ROWS for _ in range(COLS)]
        self.check_locs = []
        self.config = config
        self.log_stack = []
        self.last_checked = []
        self._create()
        self._add_pieces('white') # set of first white piece
        self._add_pieces('black') # set of first black piece

    def move(self, piece, move, testing=False):
        # print("start move") #$%
        #@!
        logmessage = f"{piece} 의 {move}"
        if testing:
            logmessage += "test_move"
        else:
            logmessage += "_____move"
        print(logmessage)    
        #@!

        initial = move.initial
        final = move.final

        flags = {
            "moved" :  False,
            "checked" : [],
            "enpassant" : False,
            "castling": False,
        }
        
        # console board move update
        if testing:
            en_passant_bool = initial.is_en_passant()
            if en_passant_bool:
                diff = final.col - initial.col
                self.squares[initial.row][initial.col].piece = None
                self.squares[final.row][final.col - diff].piece = initial.piece
            else:
                self.squares[initial.row][initial.col].piece = initial.piece
        else:
            self.squares[initial.row][initial.col].piece = None

        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0:
                en_passant_bool = final.is_en_passant()
                if en_passant_bool:
                    # console board move update
                    self.squares[initial.row][initial.col + diff].piece = None
                    if not testing:
                        flags["enpassant"] = True
                        sound = self.config.capture_sound
                        voice = self.config.en_passant_voice
                        sound.play()
                        voice.play()

            if not testing:
                # reset_enpassant
                for row in range(ROWS):
                    for col in range(COLS):
                        if isinstance(self.squares[row][col].piece, Pawn):
                            self.squares[row][col].piece.en_passant = False

            # set_enpassant
            r = 4 if piece.color == 'white' else 3
            if not piece.moved and final.row == r:
                for c in [1, -1]:
                    if Square.in_range(move.final.col+c):
                        check_piece = self.squares[r][move.final.col+c].piece
                        if isinstance(check_piece, Pawn) and piece.color != check_piece.color:
                            piece.en_passant = True

            # pawn promotion
            check_promotion = (final.row == 0 or final.row == 7)
            if check_promotion:
                self.squares[final.row][final.col].piece = Queen(piece.color)
                if not testing:
                    sound = self.config.promotion_sound
                    voice = self.config.promotion_voice
                    sound.play()
                    voice.play()

        if not testing:
            # king castling
            if isinstance(piece, King):
                castling_bool = (abs(initial.col - final.col) == 2)
                if castling_bool:
                    diff = final.col - initial.col
                    side = diff < 0 # True : left, False : right
                    if side:
                        rook = self.squares[final.row][0].piece
                        # rook move
                        initial = Square(final.row, 0)
                        final = Square(final.row, 3)
                        move_Rook = Move(initial, final)
                        voice = self.config.queen_castling_voice
                    else:
                        rook = self.squares[final.row][7].piece
                        # rook move
                        initial = Square(final.row, 7)
                        final = Square(final.row, 5)
                        move_Rook = Move(initial, final)
                        voice = self.config.king_castling_voice

                    self.move(rook, move_Rook)

                    flags["castling"] = True
                    sound = self.config.castling_sound
                    sound.play()
                    voice.play()
            
            # move
            if not piece.moved: flags["moved"] = True
            piece.moved = True

            # check?
            if self.last_checked: flags["checked"] = self.last_checked

            # add stack
            self.log_stack.append([piece, move, flags])

        # print("end move") #$%

    def back_move(self):
        if self.log_stack:
            piece, move, flags = self.log_stack.pop()
            death_piece = move.final.piece
            move.initial, move.final = move.final, move.initial

            # print("start back_move") #$%

            initial = move.initial
            final = move.final

            # console board move update
            self.squares[initial.row][initial.col].piece = death_piece
            self.squares[final.row][final.col].piece = piece

            if isinstance(death_piece, Pawn):
                # reset_enpassant
                for row in range(ROWS):
                    for col in range(COLS):
                        if isinstance(self.squares[row][col].piece, Pawn):
                            self.squares[row][col].piece.en_passant = False

                # en passant capture
                diff = final.col - initial.col
                if flags["enpassant"]:
                    # console board move update
                    self.squares[initial.row][initial.col].piece = None
                    self.squares[final.row][final.col - diff].piece = death_piece
                    # set_enpassant
                    death_piece.en_passant = True

            # king castling
            if isinstance(piece, King):
                castling_bool = (abs(initial.col - final.col) == 2)
                if flags["castling"]:
                    self.back_move()
                
            if flags["moved"]: piece.moved = False
            self.check_locs = flags["checked"]

            # print("end back_move") #$%

    def valid_move(self, piece, move):
        for piece_move in piece.moves:
            if move == piece_move:
                return piece_move

        return False

    def in_check(self, piece, move):
        # print("start in_check") #$%
        # print(f"{piece}, {move}, in_check() -> forward_move(True)") #$%
        self.move(piece, move, testing=True)
        resulted = False
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_enemy_piece(piece.color):
                    enemy_piece = self.squares[row][col].piece
                    # print(f"{enemy_piece}, in_check() -> calc_moves(True)") #$%
                    self.calc_moves(enemy_piece, row, col, testing=True)
                    for m in enemy_piece.moves:
                        # print(f"in_check : {enemy_piece}, {m}") #@!
                        if isinstance(m.final.piece, King):
                            # print("end in_check") #$%
                            resulted = True
        
        move.initial, move.final = move.final, move.initial
        # print(f"{piece}, {move}, in_check() -> backwoard_move(True)") #$%
        self.move(piece, move, testing=True)
        move.initial, move.final = move.final, move.initial
        if not resulted: #@!
            print(f"{piece} 의 {move} checkIn? : {resulted}") #@!
        # print("end in_check") #$%
        return resulted
    
    def on_check(self, piece, move):
        # print("start on_check") #$%
        # when rewind memmory check location
        self.last_checked = self.check_locs if self.check_locs else []

        self.check_locs = []
        king_loc = None
        # print(f"{piece}, {move}, on_check() -> forward_move(True)") #$%
        self.move(piece, move, testing=True)
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(piece.color):
                    team_piece = self.squares[row][col].piece
                    # print(f"{team_piece}, on_check() -> calc_moves(True)") #$%
                    self.calc_moves(team_piece, row, col, testing=True)
                    for m in team_piece.moves:
                        if isinstance(m.final.piece, King):
                            self.check_locs.append(m.initial)
                            king_loc = m.final
        
        move.initial, move.final = move.final, move.initial
        # print(f"{piece}, {move}, on_check() -> backwoard_move(True)") #$%
        self.move(piece, move, testing=True)
        move.initial, move.final = move.final, move.initial

        if self.check_locs:
            print(f"{piece} 의 {move} checkOn? : True") #@!
            self.check_locs.append(king_loc)
        else:
            print(f"{piece} 의 {move} checkOn? : False") #@!
        # print("end on_check") #$%
        return self.check_locs != []
    
    def on_mate(self, piece):
        # print("start on_mate") #$%
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_enemy_piece(piece.color):
                    enemy_piece = self.squares[row][col].piece
                    # print(f"{enemy_piece}, on_mate() -> calc_moves_move(True)") #$%
                    self.calc_moves(enemy_piece, row, col, testing=True)
                    for m in enemy_piece.moves:
                        # print(f"{enemy_piece}, {m}, on_mate() -> in_check()") #$%
                        if not self.in_check(enemy_piece, m):
                            # print("end on_mate") #$%
                            return (False, False)
        # print("end on_mate") #$%
        
        if self.check_locs:
            return (True, False)
        else:
            # print("end on_mate") #$%
            return (False, True)
        
    def calc_moves(self, piece, row, col, testing=False):
        '''
            Calculate all the possible (valid) moves of an specific piece on a specific position
        '''
        # print("start calc_moves") #$%
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
                            # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
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
                            # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
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
                            final = Square(fr, col-1, p)
                            # create a new move
                            move = Move(initial, final)
                            
                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
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
                            final = Square(fr, col+1, p)
                            # create a new move
                            move = Move(initial, final)
                            
                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
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
                            # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
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
                            # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
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
                                # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
                                if not self.in_check(piece, move):
                                    piece.add_move(move) # append new move

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potencial checks
                            if testing:
                                piece.add_move(move) # append new move
                            else:
                                # print(f"{piece}, {move}, calc_moves(False) -> in_check()") #$%
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
                            # print(f"{piece}, {move}, calc_moves(False) -> in_check()")#$%#@!
                            if not self.in_check(piece, move):
                                piece.add_move(move) # append new move

            # castling moves
            if not testing and not piece.moved:
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
                            final = Square(row, 3)
                            moveK = Move(initial, final)

                            # print(f"{piece}, {moveK}, calc_moves(False) -> in_check()") #$%

                            if not self.in_check(piece, moveK):

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # print(f"{piece}, {moveK}, calc_moves(False) -> in_check()") #$%

                                # check potencial checks
                                if not self.in_check(piece, moveK):
                                    # append new move
                                    piece.add_move(moveK)
                                    piece.castling = True

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
                            final = Square(row, 5)
                            moveK = Move(initial, final)

                            # print(f"{piece}, {moveK}, calc_moves(False) -> in_check()") #$%

                            if not self.in_check(piece, moveK):

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # print(f"{piece}, {moveK}, calc_moves(False) -> in_check()") #$%

                                # check potencial checks
                                if not self.in_check(piece, moveK):
                                    # append new move
                                    piece.add_move(moveK)
                                    piece.castling = True


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

        # print("end calc_moves") #$%

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