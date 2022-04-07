from .Piece import Piece
from ..Move import Move


class Rook(Piece):

    def __init__(self, is_white):
        super().__init__(is_white, "R")

    def get_possible_moves(self, chess_board, row, col):
        possible_moves = []
        row_nr = len(chess_board)
        col_nr = len(chess_board[0])
        for row_dir in (1, -1):
            row_len = 1
            while 0 <= row + row_dir*row_len < row_nr and 0 <= col < col_nr:
                piece = chess_board[row + row_dir*row_len][col]
                start_sq = (row, col)
                end_sq = (row + row_dir*row_len, col)
                if piece is None:
                    row_len += 1
                    possible_moves.append(Move(start_sq, end_sq, chess_board))
                    continue
                elif piece.color != self.color:
                    possible_moves.append(Move(start_sq, end_sq, chess_board))
                break

        for col_dir in (1, -1):
            col_len = 1
            while 0 <= row < row_nr and 0 <= col + col_dir*col_len < col_nr:
                piece = chess_board[row][col + col_dir*col_len]
                start_sq = (row, col)
                end_sq = (row, col + col_dir*col_len)
                if piece is None:
                    col_len += 1
                    possible_moves.append(Move(start_sq, end_sq, chess_board))
                    continue
                elif piece.color != self.color:
                    possible_moves.append(Move(start_sq, end_sq, chess_board))
                break

        return possible_moves



