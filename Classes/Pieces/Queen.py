from .Piece import Piece
from .Bishop import Bishop
from .Rook import Rook


class Queen(Piece):

    def __init__(self, is_white):
        super().__init__(is_white, "Q")

    def get_possible_moves(self, chess_board, row, col):
        if self.color == "W":
            is_white = True
        else:
            is_white = False

        bishup = Bishop(is_white)
        rook = Rook(is_white)
        return rook.get_possible_moves(chess_board, row, col) + \
               bishup.get_possible_moves(chess_board, row, col)
