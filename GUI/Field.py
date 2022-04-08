import pygame


class Field:
    def __init__(self, size, color, row, column, piece):
        self.size = size
        self.color = color
        self.row = row
        self.column = column
        # create field surface
        self.square = pygame.Surface((self.size, self.size))
        # color background of field
        self.background = pygame.Rect(0, 0, self.size, self.size)
        pygame.draw.rect(self.square, self.color, self.background)
        # if on field is piece draw it
        if piece is not None:
            piece_image = pygame.transform.scale(piece.image, (self.size, self.size))
            self.draw_inside_field(piece_image, (0, 0))

    def get_surface(self):
        return self.square

    def get_screen_position(self):
        return self.row * self.size, self.column * self.size

    def draw_inside_field(self, obj, pos):
        self.square.blit(obj, pos)

    def change_background_color(self, color):
        pygame.draw.rect(self.square, color, self.background)

    def mark_field_as_possible_move(self):
        x = 0.5 * self.size
        y = 0.5 * self.size
        pos = (x, y)
        radius = 10
        color = (100, 100, 100)
        pygame.draw.circle(self.square, color, pos, radius)