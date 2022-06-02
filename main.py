import pygame as p
import sys
from Classes.ChessEngine import ChessEngine
import chess
import chess.engine

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FIELD_WIDTH = 80
FPS = 50


def main():
    engine = ChessEngine(SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_WIDTH)
    clock = p.time.Clock()
    game_ended = False
    # game_notation = engine.read_game_from_csv("./Games/#1")
    while not game_ended:
        clock.tick(FPS)
        # handle events
        if engine.is_game_started:
            if engine.white_to_move:
                engine.time_white = engine.time_white - 20
            else:
                engine.time_black = engine.time_black - 20
        for event in p.event.get():
            if event.type == p.QUIT or game_ended:
                sys.exit(0)
            elif event.type == p.MOUSEBUTTONDOWN:
                # make move
                location = p.mouse.get_pos()
                game_ended = engine.handle_click(location)
            elif event.type == p.KEYDOWN and event.key == p.K_BACKSPACE:
                # undo move
                engine.undo_move(validated_move=True)
            elif event.type == p.KEYDOWN and event.key == p.K_0:
                # play saved game
                game_ended = engine.play_saved_game(game_notation)

        # draw chessboard
        engine.draw_chessboard()

    # engine.save_game_to_csv("./Games/#1")


# import asyncio
# import chess
# import chess.engine
# async def test() -> None:
#     transport, engine = await chess.engine.popen_uci(r"./engine/Stockfish")
#
#     board = chess.Board()
#     while not board.is_game_over():
#         result = await engine.play(board, chess.engine.Limit(time=0.1))
#         board.push(result.move)
#
#     await engine.quit()


if __name__ == '__main__':
    engine = ChessEngine(SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_WIDTH)
    computer_engine = chess.engine.SimpleEngine.popen_uci(r".\engine\stockfish_15_x64_avx2.exe")
    uci_notation = engine.convert_board_to_uci_notation()
    chess.Board(uci_notation)
    # main()

    # asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    # asyncio.run(test())
    # engine = chess.engine.SimpleEngine.popen_uci(r"./engine/Stockfish")
    # board = chess.Board()
    # info = engine.analyse(board, chess.engine.Limit(time=0.1))
    # print("Score:", info["score"])

# r n b q k b n r
# p p p p p p p p
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# P P P P P P P P
# R N B Q K B N R