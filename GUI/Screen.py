import pygame

from GUI.Board import Board
from GUI.Controls import Controls
from GUI.Timer import Timer
from Label import Label


class Screen:
    def __init__(self, board, width=1240, height=640, field_size=80):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board = Board(board, field_size)
        self.game_started = False
        self.time = 10
        self.controls = Controls(self.screen)
        self.game_over_label = Label(self.screen, 870, 100)
        self.waiting_label = Label(self.screen, 800, 250)
        self.timer_white = Timer(200, "Czas białego:", self.screen)
        self.timer_black = Timer(300, "Czas czarnego:", self.screen)

    def draw_board(self, active_square, possible_moves, engine):
        if engine.is_game_analysed:
            self.game_over_label.hide_label()
            self.waiting_label.hide_label()
            self.controls.hide_buttons()
            self.timer_white.hide_timer()
            self.timer_black.hide_timer()
            self.controls.draw_csv_buttons()
        else:
            self.controls.hide_csv_buttons()
            if engine.is_game_over:
                if engine.winner == 1:
                    self.game_over_label.add_to_scene("Wygrały białe")
                else:
                    self.game_over_label.add_to_scene("Wygrały czarne")
                self.waiting_label.hide_label()
            if not engine.is_game_started:
                if engine.game_mode == "S" and engine.network.id != "-1":
                    self.waiting_label.add_to_scene("Oczekuję na drugiego gracza")
                    self.controls.hide_buttons()
                else:
                    self.timer_white.hide_timer()
                    self.timer_black.hide_timer()
                    self.controls.draw_buttons()
                    self.waiting_label.hide_label()
            else:
                self.controls.hide_buttons()
                self.timer_white.draw_timer(engine.time_white)
                self.timer_black.draw_timer(engine.time_black)
                self.waiting_label.hide_label()
        self.board.draw_board(self.screen, active_square, possible_moves)

    def get_square_position(self, location):
        field_size = self.board.field_size
        col = location[0] // field_size
        row = location[1] // field_size
        return col, row
