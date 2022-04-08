import pygame as p
import sys
from Classes.ChessEngine import ChessEngine


def main():
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FIELD_WIDTH = 80
    FPS = 60
    engine = ChessEngine(SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_WIDTH)
    clock = p.time.Clock()

    while True:
        clock.tick(FPS)
        # handle events
        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit(0)
            elif event.type == p.MOUSEBUTTONDOWN:
                # make move
                location = p.mouse.get_pos()
                engine.handle_click(location)
            elif event.type == p.KEYDOWN and event.key == p.K_BACKSPACE:
                # undo move
                engine.undo_move(validated_move=True)

        # draw chessboard
        engine.draw_chessboard()


if __name__ == '__main__':
    main()
