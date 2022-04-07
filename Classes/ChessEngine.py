import pygame as p

from .Move import Move
from GUI.Screen import Screen
from ChessPy.Classes.Pieces import *

WIDTH = 1280
HEIGHT = 720
FIELD_WIDTH = 80 # redundant, taken from Board.py


class ChessEngine:

    def __init__(self):
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
        self.screen = Screen(WIDTH, HEIGHT, self.board)
        self.clicked_squares = []
        self.active_square = ()
        self.game_log = []
        self.possible_move_log = []
        self.all_valid_moves = self.get_all_valid_moves()

    def __get_active_color(self):
        if self.white_to_move:
            return "W"
        else:
            return "B"

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

    def __get_king_pos(self):
        row_nr = len(self.board)
        col_nr = len(self.board[0])
        active_color = self.__get_active_color()
        for r in range(row_nr):
            for c in range(col_nr):
                piece = self.board[r][c]
                if isinstance(piece, King) and piece.color == active_color:
                    return r, c
        return None, None

    def get_all_valid_moves(self):
        all_possible_moves = self.get_all_possible_moves()
        all_valid_moves = []
        for move in all_possible_moves:
            self.make_move(move, validated_move=False)
            valid_move = True
            rival_possible_moves = self.get_all_possible_moves()
            king_row, king_col = self.__get_king_pos()
            if king_row is None or king_col is None:
                self.undo_move(validated_move=False)
                continue
            king_pos_id = 10*king_row + king_col
            for rival_move in rival_possible_moves:
                if rival_move.id % 100 == king_pos_id:
                    valid_move = False
                    break
            if valid_move:
                all_valid_moves.append(move)
            self.undo_move(validated_move=False)
        return all_valid_moves

    def make_move(self, move, validated_move=False):
        self.board[move.startRow][move.startCol] = None
        self.board[move.endRow][move.endCol] = move.movedPiece
        self.white_to_move = not self.white_to_move
        if validated_move:
            move.movedPiece.is_moved = True
            print(move.get_notation())
            self.game_log.append(move)
        else:
            self.possible_move_log.append(move)

    def undo_move(self, validated_move=False):
        if validated_move:
            if len(self.game_log) == 0:
                return
            move = self.game_log.pop()
        else:
            move = self.possible_move_log.pop()
        self.board[move.startRow][move.startCol] = move.movedPiece
        self.board[move.endRow][move.endCol] = move.capturedPiece
        self.white_to_move = not self.white_to_move

    def reset_clicks(self):
        self.active_square = ()
        self.clicked_squares = []

    def handle_click(self, location):
        row_nr = len(self.board)
        col_nr = len(self.board[0])
        col = location[0] // FIELD_WIDTH
        row = location[1] // FIELD_WIDTH

        if col >= col_nr or row >= row_nr or self.active_square == (row, col):
            print("+")
            self.reset_clicks()
        elif len(self.clicked_squares) == 0:
            piece = self.board[row][col]
            if piece is not None and piece.color == self.__get_active_color():
                self.active_square = (row, col)
                self.clicked_squares.append(self.active_square)
        else:
            self.active_square = (row, col)
            self.clicked_squares.append(self.active_square)

        print(f'active square -> {self.active_square}; to move: {self.__get_active_color()}')
        if len(self.clicked_squares) == 2:
            print(self.all_valid_moves)
            move = Move(self.clicked_squares[0], self.clicked_squares[1], self.board)
            self.reset_clicks()
            if move in self.all_valid_moves:
                self.make_move(move, validated_move=True)
                self.all_valid_moves = self.get_all_valid_moves()
            else:
                print(f'Invalid move: {move}')

    def draw_chessboard(self):
        self.screen.draw_board()

