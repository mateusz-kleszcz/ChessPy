import pygame as p

from .Move import Move
from GUI.Screen import Screen
from Classes.Pieces import *


class ChessEngine:

    def __init__(self, screen_width, screen_height, row_size):
        self.board = [
            [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)],
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
        self.all_valid_moves = self.get_all_valid_moves()
        self.active_piece_valid_moves = []

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
    def get_all_valid_moves(self):
        all_possible_moves = self.get_all_possible_moves()
        all_valid_moves = []
        for move in all_possible_moves:
            self.make_move(move, validated_move=False)
            valid_move = True
            rival_possible_moves = self.get_all_possible_moves()
            for rival_move in rival_possible_moves:
                if isinstance(rival_move.capturedPiece, King):
                    valid_move = False
                    break
            if valid_move:
                all_valid_moves.append(move)
            self.undo_move(validated_move=False)
        return all_valid_moves

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
            if isinstance(last_moved_piece, Pawn) and abs(last_move.startRow - last_move.endRow) == 2:
                last_moved_piece.en_passant = True

        if last_but_one_move is not None:
            last_but_one_moved_piece = last_but_one_move.movedPiece
            if isinstance(last_but_one_moved_piece, Pawn):
                last_but_one_moved_piece.en_passant = False

    def make_move(self, move, validated_move=False):
        self.board[move.startRow][move.startCol] = None
        # move.capturedPiece = None  # for en passant
        self.board[move.endRow][move.endCol] = move.movedPiece
        if isinstance(move.movedPiece, Pawn) and abs(move.startRow - move.endRow) == 2:
            pass
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
        self.white_to_move = not self.white_to_move
        self.__update_en_passant_pawn(move)
        if validated_move:
            self.all_valid_moves = self.get_all_valid_moves()

    def reset_clicks(self):
        self.active_square = ()
        self.clicked_squares = []
        self.active_piece_valid_moves = []

    def handle_click(self, location):
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
                self.active_piece_valid_moves = [move for move in self.all_valid_moves if
                                                 self.active_square == (move.startRow, move.startCol)]
        else:
            self.active_square = (row, col)
            self.clicked_squares.append(self.active_square)

        if len(self.clicked_squares) == 2:
            move = Move(self.clicked_squares[0], self.clicked_squares[1], self.board)
            self.reset_clicks()
            if move in self.all_valid_moves:
                self.make_move(move, validated_move=True)
                self.all_valid_moves = self.get_all_valid_moves()

    def draw_chessboard(self):
        self.screen.draw_board(self.active_square, self.active_piece_valid_moves)
