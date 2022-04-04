import pygame
import sys
from Classes.ChessEngine import ChessEngine

SIZE = 8

engine = ChessEngine()

while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    # draw chessboard
    engine.draw_chessboard()
