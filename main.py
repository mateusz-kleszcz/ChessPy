import pygame as p
import sys
import chess
import chess.engine

from src.chess_classes.chess_engine import ChessEngine

FPS = 50


def main():
    engine = ChessEngine()
    clock = p.time.Clock()
    game_notation = engine.read_game_from_csv("./games/#1")
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
                if engine.game_mode == "H" or engine.game_mode == "K" and engine.white_to_move:
                    engine.handle_click(location)
            elif engine.game_mode == "K" and not engine.white_to_move:
                engine.play_computer_move()
            elif event.type == p.KEYDOWN and event.key == p.K_BACKSPACE:
                # undo move
                engine.undo_move(validated_move=True)

        # draw chessboard
        engine.draw_chessboard()

    # chess_engines.save_game_to_csv("./games/#1")


# import asyncio
# import chess
# import chess.chess_engines
# async def test() -> None:
#     transport, chess_engines = await chess.chess_engines.popen_uci(r"./chess_engines/Stockfish")
#
#     board = chess.Board()
#     while not board.is_game_over():
#         result = await chess_engines.play(board, chess.chess_engines.Limit(time=0.1))
#         board.push(result.move)
#
#     await chess_engines.quit()


if __name__ == '__main__':
    # chess_engines = ChessEngine()
    # computer_engine = chess.chess_engines.SimpleEngine.popen_uci(r".\chess_engines\stockfish_15_x64_avx2.exe")
    # uci_notation = chess_engines.convert_board_to_uci_notation()
    # board = chess.Board(uci_notation)
    # result = computer_engine.play(board, chess.chess_engines.Limit(time=0.1))
    # print(result)
    main()

    # asyncio.set_event_loop_policy(chess.chess_engines.EventLoopPolicy())
    # asyncio.run(test())
    # chess_engines = chess.chess_engines.SimpleEngine.popen_uci(r"./chess_engines/Stockfish")
    # board = chess.Board()
    # info = chess_engines.analyse(board, chess.chess_engines.Limit(time=0.1))
    # print("Score:", info["score"])

# r n b q k b n r
# p p p p p p p p
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# P P P P P P P P
# R N B Q K B N R