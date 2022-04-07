from .PieceWithLimitedMoveDir import PieceWithLimitedMoveDir


class Knight(PieceWithLimitedMoveDir):
    moves_dir = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]

    def __init__(self, is_white):
        super().__init__(is_white, "N")

    def get_possible_moves(self, chess_board, row, col):
        return super().get_possible_moves(chess_board, row, col)
