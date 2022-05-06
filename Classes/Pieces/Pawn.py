from Classes.Moves.EnPassantMove import EnPassantMove
from Classes.Moves.Move import Move
from Classes.Moves.PawnPromotion import PawnPromotion
from Classes.Pieces.Piece import Piece


class Pawn(Piece):

    def __init__(self, is_white, is_moved=False):
        super().__init__(is_white, "P", is_moved)
        self.en_passant = False

    def get_possible_moves(self, chess_board, row, col):
        possible_moves = []
        row_nr = len(chess_board)
        col_nr = len(chess_board[0])
        if self.color == 'W':
            row_dir = -1
        else:
            row_dir = 1

        # moving forward
        if 0 <= row + row_dir < row_nr and 0 <= col < col_nr and chess_board[row + row_dir][col] is None:
            start_sq = (row, col)
            end_sq = (row + row_dir, col)
            if end_sq[0] == 0 or end_sq[0] == row_nr - 1:
                possible_moves.append(PawnPromotion(chess_board, start_sq, end_sq))
            else:
                possible_moves.append(Move(chess_board, start_sq, end_sq))
                if not self.is_moved and 0 <= row + 2 * row_dir < row_nr and 0 <= col < col_nr and \
                        chess_board[row + 2 * row_dir][col] is None:
                    start_sq = (row, col)
                    end_sq = (row + 2 * row_dir, col)
                    possible_moves.append(Move(chess_board, start_sq, end_sq))

        # capturing piece
        for col_dir in (-1, 1):
            if 0 <= row + row_dir < row_nr and 0 <= col + col_dir < col_nr and \
                    chess_board[row + row_dir][col + col_dir] is not None:

                captured_piece = chess_board[row + row_dir][col + col_dir]
                if self.color != captured_piece.color:
                    start_sq = (row, col)
                    end_sq = (row + row_dir, col + col_dir)
                    if row + row_dir == 0 or row + row_dir == row_nr - 1:
                        possible_moves.append(PawnPromotion(chess_board, start_sq, end_sq))
                    else:
                        possible_moves.append(Move(chess_board, start_sq, end_sq))

        # en passant
        for col_dir in (-1, 1):
            if 0 <= row + row_dir < row_nr and 0 <= col + col_dir < col_nr and \
                    chess_board[row + row_dir][col + col_dir] is None and \
                    isinstance(chess_board[row][col + col_dir], Pawn):

                captured_pawn = chess_board[row][col + col_dir]
                if self.color != captured_pawn.color and captured_pawn.en_passant:
                    start_sq = (row, col)
                    end_sq = (row + row_dir, col + col_dir)
                    captured_pawn_sq = (row, col + col_dir)
                    possible_moves.append(EnPassantMove(chess_board, start_sq, end_sq, captured_pawn_sq))

        return possible_moves
