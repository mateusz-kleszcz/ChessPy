from Moves.Move import Move


class Castle(Move):
    def __init__(self, board, startSq, endSq, rook_start_col, rook_end_col):
        super().__init__(board, startSq, endSq)
        self.rook_start_col = rook_start_col
        self.rook_end_col = rook_end_col
