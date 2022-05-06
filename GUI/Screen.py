import pygame

from GUI.Board import Board
from GUI.Controls import Controls
from GUI.Timer import Timer


class Screen:
    def __init__(self, width, height, field_size, board):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board = Board(board, field_size)
        self.game_started = False
        self.time = 10
        self.controls = Controls(self.screen)

    def draw_board(self, active_square, possible_moves, engine):
        if not engine.is_game_started:
            self.controls = Controls(self.screen)
        else:
            self.controls.hide_buttons()
            timer_white = Timer(self.screen, engine.time_white, 200)
            timer_black = Timer(self.screen, engine.time_black, 300)
        self.board.draw_board(self.screen, active_square, possible_moves)

    def get_square_position(self, location):
        field_size = self.board.field_size
        col = location[0] // field_size
        row = location[1] // field_size
        return col, row
