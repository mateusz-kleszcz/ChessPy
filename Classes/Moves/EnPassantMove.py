from Moves.Move import Move


class EnPassantMove(Move):
    def __init__(self, board, startSq, endSq, captured_pawn_sq):
        super().__init__(board, startSq, endSq)
        self.captured_pawn_sq = captured_pawn_sq
        self.capture_pawn = board[self.captured_pawn_sq[0]][self.captured_pawn_sq[1]]
