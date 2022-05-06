import pygame as p
import os


class Piece:
    def __init__(self, is_white, name, val, pos_vals=None, is_moved=False):
        if is_white:
            self.color = "W"
        else:
            self.color = "B"
        self.name = name
        self.image = self.load_image()
        self.is_moved = is_moved
        if is_white:
            self.val = val
            self.pos_vals = pos_vals
        else:
            self.val = -val
            n, m = len(pos_vals), len(pos_vals[0])
            self.pos_vals = tuple((tuple(-1 * pos_vals[i][j] for i in range(n)) for j in range(m)))

    def get_possible_moves(self, chess_board, row, col):
        return []

    def load_image(self):
        return p.image.load(os.path.join(".", "assets", f'{self.color}{self.name}.png'))

    def __eq__(self, other):
        if type(self) is type(other):
            return self.color == other.color
        return False
