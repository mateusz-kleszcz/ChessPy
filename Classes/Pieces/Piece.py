import pygame as p
import os
from ..Move import Move


def __get_possible_moves_for_piece_with_limited_dir(chess_board, row, col, moves_dir, color):
    possible_moves = []
    row_nr = len(chess_board)
    col_nr = len(chess_board[0])

    for move_dir in moves_dir:
        row_dir = move_dir[0]
        col_dir = move_dir[1]
        if 0 <= row + row_dir < row_nr and 0 <= col + col_dir < col_nr:
            piece = chess_board[row + row_dir][col + col_dir]
            if piece is None or piece.color != color:
                start_sq = (row, col)
                end_sq = (row + row_dir, col + col_dir)
                possible_moves.append(Move(start_sq, end_sq, chess_board))

    return possible_moves


class Piece:

    def __init__(self, is_white, name, is_moved=False):
        if is_white:
            self.color = "W"
        else:
            self.color = "B"
        self.name = name
        self.image = self.load_image()
        self.is_moved = is_moved

    def get_possible_moves(self, chess_board, row, col):
        return []

    def load_image(self):
        return p.image.load(os.path.join(".", "assets", f'{self.color}{self.name}.png'))
