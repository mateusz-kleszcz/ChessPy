from Pieces.PieceWithLimitedMoveDir import PieceWithLimitedMoveDir


class Knight(PieceWithLimitedMoveDir):
    moves_dir = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]

    def __init__(self, is_white, is_moved=False):
        pos_vals = ((-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0),
                    (-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0),
                    (-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0),
                    (-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0),
                    (-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0),
                    (-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0),
                    (-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0),
                    (-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0))
        super().__init__(is_white, "N", is_moved=is_moved, val=30, pos_vals=pos_vals)

    def get_possible_moves(self, chess_board, row, col):
        return super().get_possible_moves(chess_board, row, col)
