# from .Pieces import *


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.id = 1000 * self.startRow + 100 * self.startCol + 10 * self.endRow + self.endCol
        self.movedPiece = board[self.startRow][self.startCol]
        self.capturedPiece = board[self.endRow][self.endCol]
        # if isinstance(self.movedPiece, Pawn) and self.startCol != self.endCol and self.capturedPiece is None:
        #     # en passant
        #     self.id += 10000
        #     if self.movedPiece.color == "W":
        #         self.capturedPiece = board[self.endRow + 1][self.endCol]
        #     else:
        #         self.capturedPiece = board[self.endRow - 1][self.endCol]
        self.piece_first_move = not self.movedPiece.is_moved

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.id == other.id
        return False

    def get_file_rank(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row]

    def get_notation(self):
        return self.get_file_rank(self.startRow, self.startCol) + " -> " + self.get_file_rank(self.endRow, self.endCol)

    def __str__(self):
        return self.get_notation()
