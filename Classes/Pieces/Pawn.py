from .Piece import Piece
from ..Move import Move


class Pawn(Piece):

    def __init__(self, is_white):
        super().__init__(is_white, "P")
        self.en_passant = False

    def get_possible_moves(self, chess_board, row, col):
        possible_moves = []
        row_nr = len(chess_board)
        col_nr = len(chess_board[0])
        if self.color == 'W':
            row_dir = -1
        else:
            row_dir = 1

        # moving forward
        if 0 <= row + row_dir < row_nr and 0 <= col < col_nr and chess_board[row + row_dir][col] is None:
            start_sq = (row, col)
            end_sq = (row + row_dir, col)
            possible_moves.append(Move(start_sq, end_sq, chess_board))
            if not self.is_moved and 0 <= row + 2 * row_dir < row_nr and 0 <= col < col_nr and \
                    chess_board[row + 2 * row_dir][col] is None:
                start_sq = (row, col)
                end_sq = (row + 2 * row_dir, col)
                possible_moves.append(Move(start_sq, end_sq, chess_board))

        # capturing piece
        for col_dir in (-1, 1):
            if 0 <= row + row_dir < row_nr and 0 <= col + col_dir < col_nr and \
                    chess_board[row + row_dir][col + col_dir] is not None:

                captured_piece = chess_board[row + row_dir][col + col_dir]
                if self.color != captured_piece.color:
                    start_sq = (row, col)
                    end_sq = (row + row_dir, col + col_dir)
                    possible_moves.append(Move(start_sq, end_sq, chess_board))

        # en passant
        for col_dir in (-1, 1):
            if 0 <= row + row_dir < row_nr and 0 <= col + col_dir < col_nr and \
                    chess_board[row + row_dir][col + col_dir] is None and \
                    isinstance(chess_board[row][col + col_dir], Pawn):

                captured_pawn = chess_board[row][col + col_dir]
                if self.color != captured_pawn.color and captured_pawn.en_passant:
                    start_sq = (row, col)
                    end_sq = (row + row_dir, col + col_dir)
                    possible_moves.append(Move(start_sq, end_sq, chess_board))

        return possible_moves
