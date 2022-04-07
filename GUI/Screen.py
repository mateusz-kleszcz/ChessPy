import pygame

from GUI.Board import Board


class Screen:
    def __init__(self, width, height, board):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board = Board(board)

    def draw_board(self, active_square, possible_moves):
        self.board.draw_board(self.screen, active_square, possible_moves)
