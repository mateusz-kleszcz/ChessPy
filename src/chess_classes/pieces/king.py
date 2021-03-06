from src.chess_classes.moves.castle import Castle
from src.chess_classes.pieces.piece_with_const_move_dir import PieceWithConstMoveDir
from src.chess_classes.pieces.rook import Rook


class King(PieceWithConstMoveDir):
    moves_dir = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (-1, 0)]

    def __init__(self, is_white=True):
        pos_vals = ((-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
                    (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
                    (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
                    (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
                    (-2.0, -3.0, -3.0, -4.0, -4.0, -4.0, -4.0, -2.0),
                    (-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0),
                    (2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0),
                    (2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0))
        super().__init__(is_white, "K", val=900, pos_vals=pos_vals)

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
