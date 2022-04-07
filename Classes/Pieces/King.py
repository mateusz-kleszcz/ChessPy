from .PieceWithLimitedMoveDir import PieceWithLimitedMoveDir


class King(PieceWithLimitedMoveDir):
    moves_dir = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (-1, 0)]

    def __init__(self, is_white):
        super().__init__(is_white, "K")

    def get_possible_moves(self, chess_board, row, col):
        return super().get_possible_moves(chess_board, row, col)
