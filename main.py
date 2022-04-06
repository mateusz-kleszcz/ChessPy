import pygame as p
import sys

from Classes.ChessEngine import ChessEngine

SIZE = 8

engine = ChessEngine()

while True:
    # handle events
    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit(0)
        elif event.type == p.MOUSEBUTTONDOWN: # make move
            location = p.mouse.get_pos()
            engine.handle_click(location)
        elif event.type == p.KEYDOWN:
            if event.key == p.K_BACKSPACE: # undo move
                engine.undo_move()

    # draw chessboard
    engine.draw_chessboard()



