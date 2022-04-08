import pygame

from GUI.Field import Field

BOARD_SIZE = 8
ACTIVE_BACKGROUND = (117, 199, 232)


def get_color(is_field_black):
    if is_field_black:
        return 75, 115, 153
    else:
        return 234, 233, 210


class Board:
    def __init__(self, board, field_size):
        self.board = board
        self.field_size = field_size
        self.fields = []

    # draw board first time on first render
    def draw_board(self, screen, active_square, valid_moves):
        # create fields
        for i, row in enumerate(self.board):
            is_field_black = i % 2
            row_fields = []
            for j, piece in enumerate(row):
                color = get_color(is_field_black)
                # if square is active change background color
                if active_square != ():
                    x, y = active_square
                    if x == i and y == j:
                        color = ACTIVE_BACKGROUND
                square = Field(self.field_size, color, j, i, piece)
                is_field_black = not is_field_black
                # add field to list
                row_fields.append(square)
                # mark fields that are possible moves
                for move in valid_moves:
                    if move.endRow == i and move.endCol == j:
                        square.mark_field_as_possible_move()
                screen.blit(square.get_surface(), square.get_screen_position())
            self.fields.append(row_fields)
        # add fields to screen
        pygame.display.flip()
