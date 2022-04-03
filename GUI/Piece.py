import pygame


def load_image(name):
    return pygame.image.load(f'./assets/{name}.png')


class Piece:
    def __init__(self, name):
        self.name = name
        self.image = load_image(name)
