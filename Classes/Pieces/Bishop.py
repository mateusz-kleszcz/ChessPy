from Classes.Pieces.Piece import Piece
from Classes.Moves.Move import Move


class Bishop(Piece):
    def __init__(self, is_white=True, is_moved=False):
        pos_vals = ((-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0),
                    (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0),
                    (-1.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.0, -1.0),
                    (-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0),
                    (-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0),
                    (-1.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.0, -1.0),
                    (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0),
                    (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0))
        super().__init__(is_white, "B", is_moved=is_moved, val=30, pos_vals=pos_vals)

    def get_possible_moves(self, chess_board, row, col):
        possible_moves = []
        row_nr = len(chess_board)
        col_nr = len(chess_board[0])
        for row_dir in (1, -1):
            for col_dir in (1, -1):
                dir_len = 1
                while 0 <= row + row_dir*dir_len < row_nr and 0 <= col + col_dir*dir_len < col_nr:
                    piece = chess_board[row + row_dir*dir_len][col + col_dir*dir_len]
                    start_sq = (row, col)
                    end_sq = (row + row_dir*dir_len, col + col_dir*dir_len)
                    if piece is None:
                        dir_len += 1
                        possible_moves.append(Move(chess_board, start_sq, end_sq))
                        continue
                    elif piece.color != self.color:
                        possible_moves.append(Move(chess_board, start_sq, end_sq))
                    break
        return possible_moves
