from GUI.ButtonGroup import ButtonGroup
from GUI.Button import Button
import easygui

from Label import Label


def change_game_mode(engine, value):
    engine.game_mode = value


def change_time(engine, value):
    engine.time_white = value * 60 * 1000
    engine.time_black = value * 60 * 1000


def start_game(engine, value):
    engine.start_game()


class Controls:
    def __init__(self, screen):
        game_mode_group = ButtonGroup("gamemode")
        time_group = ButtonGroup("time")
        self.buttons = [
            Button(100, 40, 700, 200, "Hot-seat", "H", change_game_mode, game_mode_group),
            Button(100, 40, 900, 200, "Komputer", "K", change_game_mode, game_mode_group),
            Button(100, 40, 1100, 200, "Serwer", "S", change_game_mode, game_mode_group),
            Button(100, 40, 800, 300, "3 minuty", 3, change_time, time_group),
            Button(100, 40, 1000, 300, "10 minut", 10, change_time, time_group),
            Button(100, 40, 1000, 400, "Graj", None, start_game, None),
            Button(100, 40, 800, 400, "CSV", None, self.analyse_game, None),
        ]
        self.csv_buttons = [
            Button(100, 40, 1020, 250, ">", 1, self.change_move, None),
            Button(100, 40, 820, 250, "<", -1, self.change_move, None),
            Button(100, 40, 894, 350, "Powrót", 0, self.change_move, None),
        ]
        self.fen_label = Label(screen, 900, 150)
        self.screen = screen
        self.game_notation = ""
        self.last_move = ""

    def handle_button_click(self, location, engine):
        x, y = location
        for button in self.buttons:
            if button.x <= x <= button.x + button.size_x and button.y <= y <= button.y + button.size_y:
                button.handle_click(engine)
        for button in self.csv_buttons:
            if button.x <= x <= button.x + button.size_x and button.y <= y <= button.y + button.size_y:
                button.handle_click(engine)

    def hide_buttons(self):
        for button in self.buttons:
            button.hide_button(self.screen)

    def draw_buttons(self):
        for button in self.buttons:
            button.add_to_scene(self.screen)

    def draw_csv_buttons(self):
        for button in self.csv_buttons:
            button.add_to_scene(self.screen)
        self.fen_label.add_to_scene(self.last_move)

    def hide_csv_buttons(self):
        for button in self.csv_buttons:
            button.hide_button(self.screen)
        self.fen_label.hide_label()

    def analyse_game(self, engine, value):
        engine.is_game_analysed = True
        try:
            path = easygui.fileopenbox()
            self.game_notation = engine.read_game_from_csv(path)
        except TypeError as e:
            print(str(e))


    def change_move(self, engine, value):
        print(self.game_notation)
        if value == 1:
            engine.play_saved_game(self.game_notation)
        if value == 0:
            engine.is_game_analysed = False
        if value == -1:
            engine.undo_move(validated_move=True)
        if len(engine.game_notation) != 0:
            self.last_move = engine.game_notation[-1]