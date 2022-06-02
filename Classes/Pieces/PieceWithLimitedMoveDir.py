from Classes.Pieces.Piece import Piece
from Classes.Moves.Move import Move


class PieceWithLimitedMoveDir(Piece):
    moves_dir = []

    def __init__(self, is_white, name, is_moved=False, val=0, pos_vals=None):
        super().__init__(is_white, name, is_moved=is_moved, val=val, pos_vals=pos_vals)

    def get_possible_moves(self, chess_board, row, col):
        possible_moves = []
        row_nr = len(chess_board)
        col_nr = len(chess_board[0])

        for move_dir in self.moves_dir:
            row_dir = move_dir[0]
            col_dir = move_dir[1]
            if 0 <= row + row_dir < row_nr and 0 <= col + col_dir < col_nr:
                piece = chess_board[row + row_dir][col + col_dir]
                if piece is None or piece.color != self.color:
                    start_sq = (row, col)
                    end_sq = (row + row_dir, col + col_dir)
                    possible_moves.append(Move(chess_board, start_sq, end_sq))

        return possible_moves
