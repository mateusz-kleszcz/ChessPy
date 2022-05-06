from Classes.Pieces.Bishop import Bishop
from Classes.Pieces.Piece import Piece
from Classes.Pieces.Rook import Rook


class Queen(Piece):

    def __init__(self, is_white, is_moved=False):
        super().__init__(is_white, "Q", is_moved)

    def get_possible_moves(self, chess_board, row, col):
        if self.color == "W":
            is_white = True
        else:
            is_white = False

        bishop = Bishop(is_white)
        rook = Rook(is_white)
        return rook.get_possible_moves(chess_board, row, col) + \
               bishop.get_possible_moves(chess_board, row, col)
