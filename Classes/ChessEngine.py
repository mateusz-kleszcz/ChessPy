import pygame as p

from .Move import Move
from GUI.Screen import Screen
from Classes.Pieces import *

WIDTH = 1280
HEIGHT = 720
FIELD_WIDTH = 80 # redundant, taken from Board.py


class ChessEngine:
    def __init__(self):
        self.board = [
            [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)],
            [Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True)],
            [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)],
        ]
        self.isWhiteMove = True
        self.screen = Screen(WIDTH, HEIGHT, self.board)
        self.clickedSquares = []
        self.activeSquare = ()
        self.gameLog = []

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = None
        self.board[move.endRow][move.endCol] = move.movedPiece
        print(move.get_notation())
        self.gameLog.append(move)
        self.isWhiteMove = not self.isWhiteMove

    def undo_move(self):
        if len(self.gameLog) == 0:
            return
        move = self.gameLog.pop()
        self.board[move.startRow][move.startCol] = move.movedPiece
        self.board[move.endRow][move.endCol] = move.capturedPiece

    def reset_clicks(self):
        self.activeSquare = ()
        self.clickedSquares = []

    def handle_click(self, location):
        col = location[0] // FIELD_WIDTH
        row = location[1] // FIELD_WIDTH
        if self.activeSquare == (row, col):
            self.reset_clicks()
        else:
            self.activeSquare = (row, col)
            self.clickedSquares.append(self.activeSquare)
        if len(self.clickedSquares) == 2:
            move = Move(self.clickedSquares[0], self.clickedSquares[1], self.board)
            self.make_move(move)
            self.reset_clicks()

    def draw_chessboard(self):
        self.screen.draw_board()

