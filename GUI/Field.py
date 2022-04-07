import pygame
FIELD_WIDTH = 80


class Field:
    def __init__(self, color, row, column, piece):
        self.color = color
        self.row = row
        self.column = column
        # create field surface
        self.square = pygame.Surface((FIELD_WIDTH, FIELD_WIDTH))
        # color background of field
        self.background = pygame.Rect(0, 0, FIELD_WIDTH, FIELD_WIDTH)
        pygame.draw.rect(self.square, self.color, self.background)
        # if on field is piece draw it
        if piece is not None:
            piece_image = pygame.transform.scale(piece.image, (FIELD_WIDTH, FIELD_WIDTH))
            self.draw_inside_field(piece_image, (0, 0))

    def get_surface(self):
        return self.square

    def get_screen_position(self):
        return self.row * FIELD_WIDTH, self.column * FIELD_WIDTH

    def draw_inside_field(self, obj, pos):
        self.square.blit(obj, pos)