import pygame as p
import sys
from Classes.ChessEngine import ChessEngine

FPS = 50


def main():
    engine = ChessEngine()
    clock = p.time.Clock()
    game_notation = engine.read_game_from_csv("./Games/#1")
    while True:
        clock.tick(FPS)
        # handle events
        if engine.game_mode == "S" and engine.network.id != "-1":
            engine.receive_from_server()

        if engine.is_game_started:
            if engine.white_to_move:
                engine.time_white = engine.time_white - 20
            else:
                engine.time_black = engine.time_black - 20
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
    main()

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