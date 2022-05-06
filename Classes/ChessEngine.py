import pygame as p

from Classes.Moves.Castle import Castle
from Classes.Moves.EnPassantMove import EnPassantMove
from Classes.Moves.PawnPromotion import PawnPromotion
from Classes.Pieces import *
from GUI.Screen import Screen


def init_all_valid_moves():
    return {(sr, sc, er, ec): None for sr in range(ChessEngine.ROW_NR) for sc in range(ChessEngine.COL_NR)
            for er in range(ChessEngine.ROW_NR) for ec in range(ChessEngine.COL_NR)}


class ChessEngine:
    ROW_NR = 8
    COL_NR = 8

    def __init__(self, screen_width, screen_height, row_size):
        self.board = [
            [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False),
             Rook(False)],
            [Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True)],
            [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)],
        ]
        self.white_to_move = True
        self.screen = Screen(screen_width, screen_height, row_size, self.board)
        self.clicked_squares = []
        self.active_square = ()
        self.game_log = []
        self.possible_move_log = []
        self.all_valid_moves = init_all_valid_moves()
        self.update_all_valid_moves()
        self.active_piece_valid_moves = []
        self.is_game_started = False
        self.time_white = 10 * 60 * 1000
        self.time_black = 10 * 60 * 1000

    def __reset_valid_moves(self):
        self.all_valid_moves = {k: None for k, v in self.all_valid_moves.items()}

    def __get_active_color(self):
        if self.white_to_move:
            return "W"
        else:
            return "B"

    # Function returns list of all possible moves (in terms of moving pieces in valid direction) by
    # active player in position determined by board
    def get_all_possible_moves(self):
        row_nr = len(self.board)
        col_nr = len(self.board[0])
        all_possible_moves = []
        active_color = self.__get_active_color()
        for r in range(row_nr):
            for c in range(col_nr):
                piece = self.board[r][c]
                if piece is not None and piece.color == active_color:
                    all_possible_moves.append(piece.get_possible_moves(self.board, r, c))
        flatten_all_possible_moves = [move for piece_moves in all_possible_moves for move in piece_moves]
        return flatten_all_possible_moves

    # Function returns list of all valid moves by active player. It takes into account situation when
    # move is appropriate in terms of it's direction, but causes opponent to check active player's king.
    def update_all_valid_moves(self):
        self.__reset_valid_moves()
        all_possible_moves = self.get_all_possible_moves()
        for move in all_possible_moves:
            self.make_move(move, validated_move=False)
            if isinstance(move, Castle):
                min_castle_col = min(move.startCol, move.rook_start_col)
                max_castle_col = max(move.startCol, move.rook_start_col)
                castle_sq = [(move.startRow, col) for col in range(min_castle_col, max_castle_col + 1)]

            valid_move = True
            rival_possible_moves = self.get_all_possible_moves()
            for rival_move in rival_possible_moves:
                if isinstance(rival_move.capturedPiece, King) or \
                        (isinstance(move, Castle) and (rival_move.endRow, rival_move.endCol) in castle_sq):
                    valid_move = False
                    break

            if valid_move:
                self.all_valid_moves[(move.startRow, move.startCol, move.endRow, move.endCol)] = move
            self.undo_move(validated_move=False)

    def __update_en_passant_pawn(self, undo_move_piece=None):
        if undo_move_piece is not None and isinstance(undo_move_piece, Pawn):
            undo_move_piece.en_passant = False

        last_move, last_but_one_move = None, None
        if len(self.possible_move_log) > 0:
            last_move = self.possible_move_log[-1]
            if len(self.game_log) > 0:
                last_but_one_move = self.game_log[-1]
        elif len(self.game_log) > 0:
            last_move = self.game_log[-1]
            if len(self.game_log) > 1:
                last_but_one_move = self.game_log[-2]

        if last_move is not None:
            last_moved_piece = last_move.movedPiece
            if isinstance(last_moved_piece, Pawn):
                last_moved_piece.en_passant = abs(last_move.startRow - last_move.endRow) == 2

        if last_but_one_move is not None:
            last_but_one_moved_piece = last_but_one_move.movedPiece
            if isinstance(last_but_one_moved_piece, Pawn):
                last_but_one_moved_piece.en_passant = False

    def make_move(self, move, validated_move=False):
        self.board[move.startRow][move.startCol] = None
        self.board[move.endRow][move.endCol] = move.movedPiece
        if isinstance(move, EnPassantMove):
            self.board[move.captured_pawn_sq[0]][move.captured_pawn_sq[1]] = None
        elif isinstance(move, Castle):
            rook = self.board[move.startRow][move.rook_start_col]
            self.board[move.startRow][move.rook_start_col] = None
            rook.is_moved = True
            self.board[move.startRow][move.rook_end_col] = rook
        elif isinstance(move, PawnPromotion) and validated_move:
            # print("Choose promoted piece:\n[Q] -> Queen\n[R] -> Rook\n[B] -> Bishup\n[K] -> Knight\n")
            # t = True
            # while t:
            #     for event in p.event.get():
            #         if event.type == p.KEYDOWN:
            #             if event.key == p.K_q:
            #                 promoted_piece_type = Queen
            #             elif event.key == p.K_r:
            #                 promoted_piece_type = Rook
            #             elif event.key == p.K_b:
            #                 promoted_piece_type = Bishop
            #             elif event.key == p.K_k:
            #                 promoted_piece_type = Knight
            #             t = False
            #             break
            promoted_piece_type = Queen
            # if promoted_piece == "Q":
            #     promoted_piece_type = Queen
            # elif promoted_piece == "R":
            #     promoted_piece_type = Rook
            # elif promoted_piece == "B":
            #     promoted_piece_type = Bishop
            # elif promoted_piece == "K":
            #     promoted_piece_type = Knight
            # else:
            #     raise KeyError("No valid piece was promoted")
            self.board[move.endRow][move.endCol] = promoted_piece_type(move.movedPiece.color, is_moved=True)
        self.white_to_move = not self.white_to_move
        if validated_move:
            move.movedPiece.is_moved = True
            self.game_log.append(move)
        else:
            self.possible_move_log.append(move)
        self.__update_en_passant_pawn()

    def undo_move(self, validated_move=False):
        if validated_move:
            if len(self.game_log) == 0:
                return
            move = self.game_log.pop()
        else:
            move = self.possible_move_log.pop()
        self.board[move.startRow][move.startCol] = move.movedPiece
        self.board[move.endRow][move.endCol] = move.capturedPiece
        move.movedPiece.is_moved = not move.piece_first_move
        if isinstance(move, EnPassantMove):
            self.board[move.captured_pawn_sq[0]][move.captured_pawn_sq[1]] = move.capture_pawn
        elif isinstance(move, Castle):
            rook = self.board[move.startRow][move.rook_end_col]
            self.board[move.startRow][move.rook_end_col] = None
            self.board[move.startRow][move.rook_start_col] = rook
            rook.is_moved = False
        elif isinstance(move, PawnPromotion):
            move.movedPiece = Pawn(move.movedPiece.color, is_moved=True)
        self.white_to_move = not self.white_to_move
        self.__update_en_passant_pawn(move.movedPiece)
        if validated_move:
            self.update_all_valid_moves()

    def reset_clicks(self):
        self.active_square = ()
        self.clicked_squares = []
        self.active_piece_valid_moves = []

    def handle_click(self, location):
        # check is controls clicked
        self.screen.controls.handle_button_click(location, self)

        if self.is_game_started:
            row_nr = len(self.board)
            col_nr = len(self.board[0])
            col, row = self.screen.get_square_position(location)

            if col >= col_nr or row >= row_nr or self.active_square == (row, col):
                self.reset_clicks()
            elif len(self.clicked_squares) == 0:
                piece = self.board[row][col]
                if piece is not None and piece.color == self.__get_active_color():
                    self.active_square = (row, col)
                    self.clicked_squares.append(self.active_square)
                    # show possible moves
                    self.active_piece_valid_moves = [move for pos, move in self.all_valid_moves.items() if
                                                     self.active_square == (pos[0], pos[1]) and move is not None]
            else:
                self.active_square = (row, col)
                self.clicked_squares.append(self.active_square)

            if len(self.clicked_squares) == 2:
                move = self.all_valid_moves[(*self.clicked_squares[0], *self.clicked_squares[1])]
                self.reset_clicks()
                if move is not None:
                    self.make_move(move, validated_move=True)
                    self.update_all_valid_moves()
                    if len(list(set(list(self.all_valid_moves.values())))) == 1:
                        self.white_to_move = not self.white_to_move
                        all_moves_at_the_end = self.get_all_possible_moves()
                        for end_move in all_moves_at_the_end:
                            if isinstance(end_move.capturedPiece, King):
                                winner = "White" if self.white_to_move else "Black"
                                print(f'Game is ended. {winner} has won!')
                                return True
                        print("Game ended with a tie!")
                        return True
            return False

    def draw_chessboard(self):
        self.screen.draw_board(self.active_square, self.active_piece_valid_moves, self)

    def start_game(self):
        self.is_game_started = True

    def end_game(self):
        self.is_game_started = False