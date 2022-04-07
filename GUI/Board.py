import pygame

from GUI.Field import Field

BOARD_SIZE = 8


def get_color(is_field_black):
    if is_field_black:
        return 75, 115, 153
    else:
        return 234, 233, 210


class Board:
    def __init__(self, board):
        self.board = board
        self.fields = []

    # draw board first time on first render
    def draw_board(self, screen):
        for i, row in enumerate(self.board):
            is_field_black = i % 2
            row_fields = []
            for j, piece in enumerate(row):
                # create field
                color = get_color(is_field_black)
                square = Field(color, j, i, piece)
                screen.blit(square.get_surface(), square.get_screen_position())
                is_field_black = not is_field_black
                # add field to list
                row_fields.append(square)
            self.fields.append(row_fields)
        self.mark_allowed_field(3, 3, screen)
        pygame.display.flip()

    # mark field as allowed, function takes two arguments, i - row, j - column that should be allowed
    def mark_allowed_field(self, i, j, screen):
        if not (0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE):
            return
        field = self.fields[i][j]
        color = (100, 100, 100)
        pygame.draw.circle(screen, color, (20, 20), 100)
        pygame.display.update()
