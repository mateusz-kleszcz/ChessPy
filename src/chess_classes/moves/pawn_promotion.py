from src.chess_classes.moves.move import Move


class PawnPromotion(Move):
    def __init__(self, board, startSq, endSq):
        super().__init__(board, startSq, endSq)
        self.promotedPieceType = None
