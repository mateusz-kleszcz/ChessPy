import pygame as p
import os


class Piece:

    def __init__(self, is_white, name, is_moved=False):
        if is_white:
            self.color = "W"
        else:
            self.color = "B"
        self.name = name
        self.image = self.load_image()
        self.is_moved = is_moved

    def get_possible_moves(self, chess_board, row, col):
        return []

    def load_image(self):
        return p.image.load(os.path.join(".", "assets", f'{self.color}{self.name}.png'))
