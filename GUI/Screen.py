import pygame

from GUI.Board import Board


class Screen:
    def __init__(self, width, height, field_size, board):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board = Board(board, field_size)

    def draw_board(self, active_square, possible_moves):
        self.board.draw_board(self.screen, active_square, possible_moves)

    def get_square_position(self, location):
        field_size = self.board.field_size
        col = location[0] // field_size
        row = location[1] // field_size
        return col, row

