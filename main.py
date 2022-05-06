import pygame as p
import sys
from Classes.ChessEngine import ChessEngine


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FIELD_WIDTH = 80
FPS = 50


def main():
    engine = ChessEngine(SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_WIDTH)
    clock = p.time.Clock()
    game_ended = False
    computer_move = False
    while True:
        clock.tick(FPS)
        computer_move = not engine.white_to_move
        # handle events
        if engine.is_game_started:
            if engine.white_to_move:
                engine.time_white = engine.time_white - 20
            else:
                engine.time_black = engine.time_black - 20
        for event in p.event.get():
            if event.type == p.QUIT or game_ended:
                sys.exit(0)
            elif event.type == p.MOUSEBUTTONDOWN and not computer_move:
                # make move
                location = p.mouse.get_pos()
                game_ended = engine.handle_click(location)
            elif event.type == p.KEYDOWN and event.key == p.K_BACKSPACE and not computer_move:
                # undo move
                engine.undo_move(validated_move=True)
            elif computer_move:
                engine.make_engine_move()

        # draw chessboard
        engine.draw_chessboard()


if __name__ == '__main__':
    main()
