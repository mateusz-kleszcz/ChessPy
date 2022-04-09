from Pieces.PieceWithLimitedMoveDir import PieceWithLimitedMoveDir
from Pieces.Rook import Rook
from Moves.Castle import Castle


class King(PieceWithLimitedMoveDir):
    moves_dir = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (-1, 0)]

    def __init__(self, is_white):
        super().__init__(is_white, "K")

    def get_possible_moves(self, chess_board, row, col):
        all_possible_moves = super().get_possible_moves(chess_board, row, col)

        king = chess_board[row][col]
        if king.is_moved is False and chess_board[row][col+1:col+3] == [None, None] \
                and isinstance(chess_board[row][col+3], Rook) and chess_board[row][col+3].is_moved is False:

            start_sq, end_sq, rook_start_col, rook_end_col = (row, col), (row, col+2), col+3, col+1
            all_possible_moves.append(Castle(chess_board, start_sq, end_sq, rook_start_col, rook_end_col))

        if king.is_moved is False and chess_board[row][col-3:col] == [None, None, None] \
                and isinstance(chess_board[row][col-4], Rook) and chess_board[row][col-4].is_moved is False:

            start_sq, end_sq, rook_start_col, rook_end_col = (row, col), (row, col-2), col-4, col-1
            all_possible_moves.append(Castle(chess_board, start_sq, end_sq, rook_start_col, rook_end_col))

        return all_possible_moves
