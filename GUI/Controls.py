from ButtonGroup import ButtonGroup
from GUI.Button import Button


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
            Button(100, 40, 900, 400, "Graj", None, start_game, None),
        ]
        self.screen = screen

    def handle_button_click(self, location, engine):
        x, y = location
        for button in self.buttons:
            if button.x <= x <= button.x + button.size_x and button.y <= y <= button.y + button.size_y:
                button.handle_click(engine)

    def hide_buttons(self):
        for button in self.buttons:
            button.hide_button(self.screen)

    def draw_buttons(self):
        for button in self.buttons:
            button.add_to_scene(self.screen)
