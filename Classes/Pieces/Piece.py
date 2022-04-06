import pygame as p
import os


class Piece:
    def __init__(self, isWhite, name):
        if isWhite:
            self.color = "W"
        else:
            self.color = "B"
        self.name = name
        self.image = self.load_image()
        self.moves = []

    def possible_moves(self, chess_engine):
        pass

    def load_image(self):
        return p.image.load(os.path.join(".", "assets", f'{self.color}{self.name}.png'))
