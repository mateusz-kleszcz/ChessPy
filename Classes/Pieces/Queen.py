from Pieces import Piece
from Pieces.Bishop import Bishop
from Pieces.Rook import Rook


class Queen(Piece):

    def __init__(self, is_white=True, is_moved=False):
        pos_vals = ((-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0),
                    (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0),
                    (-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0),
                    (-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5),
                    (-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5),
                    (-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0),
                    (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0),
                    (-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0))
        super().__init__(is_white, "Q", is_moved=is_moved, val=90, pos_vals=pos_vals)

    def get_possible_moves(self, chess_board, row, col):
        if self.color == "W":
            is_white = True
        else:
            is_white = False

        bishop = Bishop(is_white)
        rook = Rook(is_white)
        return rook.get_possible_moves(chess_board, row, col) + \
               bishop.get_possible_moves(chess_board, row, col)
