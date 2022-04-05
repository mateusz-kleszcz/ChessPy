import pygame

from GUI.Piece import Piece

BOARD_SIZE = 8
FIELD_WIDTH = 80


def get_color(is_field_black):
    if is_field_black:
        return 75, 115, 153
    else:
        return 234, 233, 210


class Board:
    def __init__(self, board):
        self.board = board
        self.pieces = []

    def draw_board(self, screen):
        for i, row in enumerate(self.board):
            is_field_black = i % 2
            for j, piece in enumerate(row):
                square = pygame.Surface((FIELD_WIDTH, FIELD_WIDTH))
                background = pygame.Rect(0, 0, FIELD_WIDTH, FIELD_WIDTH)
                pygame.draw.rect(square, get_color(is_field_black), background)
                if piece is not None:
                    self.pieces.append(piece)
                    piece_image = pygame.transform.scale(piece.image, (FIELD_WIDTH, FIELD_WIDTH))
                    square.blit(piece_image, (0, 0))
                screen.blit(square, (j * FIELD_WIDTH, i * FIELD_WIDTH))
                is_field_black = not is_field_black
        pygame.display.flip()
