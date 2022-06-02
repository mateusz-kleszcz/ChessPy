import pygame as p
import chess
import chess.engine
import csv
from network import Network

from Classes.Pieces import *
from Classes.Moves import *
from GUI import *
from GUI.Screen import Screen

ROW_NR = 8
COL_NR = 8

SCREEN_WIDTH = 1240
SCREEN_HEIGHT = 640
FIELD_WIDTH = 80


def init_all_valid_moves():
    return {(sr, sc, er, ec): None for sr in range(ROW_NR) for sc in range(COL_NR)
            for er in range(ROW_NR) for ec in range(COL_NR)}


def get_init_board():
    init_board = [
        [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)],
        [Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False)],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True)],
        [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)],
    ]
    return init_board


class ChessEngine:
    def __init__(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, field_width=FIELD_WIDTH):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.field_width = field_width
        self.game_mode = "H"
        self.reset()

    def reset(self):
        self.board = get_init_board()
        self.screen = Screen(self.board, self.screen_width, self.screen_height, self.field_width)
        self.white_to_move = True
        self.clicked_squares = []
        self.active_square = ()
        self.game_log = []
        self.possible_move_log = []
        self.all_valid_moves = self.calculate_all_valid_moves()
        self.active_piece_valid_moves = []
        self.board_val = self.calculate_board_val()
        self.is_game_started = False
        self.time_white = 10 * 60 * 1000
        self.time_black = 10 * 60 * 1000
        self.network = Network()
        self.game_notation = []
        self.is_game_over = False
        self.winner = None
        self.is_check = False
        self.color = None
        self.is_player_white = None
        self.last_move_white = ""
        self.last_move_black = ""
        self.is_game_analysed = False

    def calculate_board_val(self):
        board_val = 0
        for row in range(ROW_NR):
            for col in range(COL_NR):
                piece = self.board[row][col]
                if piece is not None:
                    board_val += piece.val
                    board_val += piece.pos_vals[row][col]
        return board_val

    def __check_if_game_is_over(self):
        if len(set(self.all_valid_moves.values())) == 1:
            self.game_over()

    def game_over(self):
        self.white_to_move = not self.white_to_move
        all_moves_at_the_end = self.calculate_all_possible_moves()
        for end_move in all_moves_at_the_end:
            if isinstance(end_move.capturedPiece, King):
                self.is_game_over = True
                self.is_game_started = False
                self.winner = 1 if self.white_to_move else -1
                self.game_notation.append(self.game_notation.pop() + "+")
                winner = "White" if self.white_to_move else "Black"
                print(f'Game is ended. {winner} has won!')
                return
        self.is_game_over = True
        self.is_game_started = False
        self.winner = 0
        print("Game ended with a tie!")

    def __reset_valid_moves(self):
        self.all_valid_moves = {k: None for k, v in self.all_valid_moves.items()}

    def __get_active_color(self):
        if self.white_to_move:
            return "W"
        else:
            return "B"

    # Function returns list of all possible moves (in terms of moving pieces in valid direction) by
    # active player in position determined by board
    def calculate_all_possible_moves(self):
        all_possible_moves = []
        active_color = self.__get_active_color()
        for r in range(ROW_NR):
            for c in range(COL_NR):
                piece = self.board[r][c]
                if piece is not None and piece.color == active_color:
                    all_possible_moves.append(piece.get_possible_moves(self.board, r, c))
        flatten_all_possible_moves = [move for piece_moves in all_possible_moves for move in piece_moves]
        return flatten_all_possible_moves

    # Function returns list of all valid moves by active player. It takes into account situation when
    # move is appropriate in terms of it's direction, but causes opponent to check active player's king.
    def calculate_all_valid_moves(self):
        # self.__reset_valid_moves()
        all_possible_moves = self.calculate_all_possible_moves()
        all_valid_moves = init_all_valid_moves()
        for move in all_possible_moves:
            self.make_move(move, validated_move=False)
            if isinstance(move, Castle):
                min_castle_col = min(move.startCol, move.rook_start_col)
                max_castle_col = max(move.startCol, move.rook_start_col)
                castle_sq = [(move.startRow, col) for col in range(min_castle_col, max_castle_col + 1)]

            is_move_valid = True
            rival_possible_moves = self.calculate_all_possible_moves()
            for rival_move in rival_possible_moves:
                if isinstance(rival_move.capturedPiece, King) or \
                        (isinstance(move, Castle) and (rival_move.endRow, rival_move.endCol) in castle_sq):
                    is_move_valid = False
                    break

            if is_move_valid:
                all_valid_moves[(move.startRow, move.startCol, move.endRow, move.endCol)] = move
            self.undo_move(validated_move=False)
        return all_valid_moves

    def __update_en_passant_pawn(self, undo_move_piece=None):
        if undo_move_piece is not None and isinstance(undo_move_piece, Pawn):
            undo_move_piece.en_passant = False

        last_move, last_but_one_move = None, None
        if len(self.possible_move_log) > 0:
            last_move = self.possible_move_log[-1]
            if len(self.game_log) > 0:
                last_but_one_move = self.game_log[-1]
        elif len(self.game_log) > 0:
            last_move = self.game_log[-1]
            if len(self.game_log) > 1:
                last_but_one_move = self.game_log[-2]

        if last_move is not None:
            last_moved_piece = last_move.movedPiece
            if isinstance(last_moved_piece, Pawn):
                last_moved_piece.en_passant = abs(last_move.startRow - last_move.endRow) == 2

        if last_but_one_move is not None:
            last_but_one_moved_piece = last_but_one_move.movedPiece
            if isinstance(last_but_one_moved_piece, Pawn):
                last_but_one_moved_piece.en_passant = False

    def make_move(self, move, validated_move=False, read=False, enemy=False):
        self.board[move.startRow][move.startCol] = None
        self.board[move.endRow][move.endCol] = move.movedPiece
        if isinstance(move, EnPassantMove):
            self.board[move.captured_pawn_sq[0]][move.captured_pawn_sq[1]] = None
        elif isinstance(move, Castle):
            rook = self.board[move.startRow][move.rook_start_col]
            self.board[move.startRow][move.rook_start_col] = None
            rook.is_moved = True
            self.board[move.startRow][move.rook_end_col] = rook
        elif isinstance(move, PawnPromotion) and validated_move:
            if not read:
                print("Choose promoted piece:\n[Q] -> Queen\n[R] -> Rook\n[B] -> Bishup\n[K] -> Knight\n")

                def choose_promoted_piece():
                    paused = True
                    promoted_piece_type = None
                    FPS = 50
                    clock = p.time.Clock()
                    # TODO: interactive menu
                    while paused:
                        clock.tick(FPS)
                        for event in p.event.get():
                            if event.type == p.KEYDOWN:
                                if event.key == p.K_q:
                                    promoted_piece_type = Queen
                                elif event.key == p.K_r:
                                    promoted_piece_type = Rook
                                elif event.key == p.K_b:
                                    promoted_piece_type = Bishop
                                elif event.key == p.K_k:
                                    promoted_piece_type = Knight
                                paused = False
                    return promoted_piece_type
                move.promotedPieceType = choose_promoted_piece()

            self.board[move.endRow][move.endCol] = move.promotedPieceType(move.movedPiece.color, is_moved=True)
        self.white_to_move = not self.white_to_move
        if validated_move:
            move.movedPiece.is_moved = True
            self.check_if_check()
            self.game_log.append(move)
            move_notation = self.make_move_notation(move)
            self.game_notation.append(move_notation)
            if not enemy:
                if self.is_player_white:
                    self.last_move_white = move_notation
                else:
                    self.last_move_black = move_notation
            else:
                if self.is_player_white:
                    self.last_move_black = move_notation
                else:
                    self.last_move_white = move_notation
            self.__update_en_passant_pawn()
            self.all_valid_moves = self.calculate_all_valid_moves()
            self.__check_if_game_is_over()
        else:
            self.__update_en_passant_pawn()
            self.possible_move_log.append(move)
            # self.board_val = self.calculate_board_val()

    def undo_move(self, validated_move=False):
        if validated_move:
            if len(self.game_log) == 0:
                return
            move = self.game_log.pop()
            self.game_notation.pop()
        else:
            move = self.possible_move_log.pop()
        self.board[move.startRow][move.startCol] = move.movedPiece
        self.board[move.endRow][move.endCol] = move.capturedPiece
        move.movedPiece.is_moved = not move.piece_first_move
        if isinstance(move, EnPassantMove):
            self.board[move.captured_pawn_sq[0]][move.captured_pawn_sq[1]] = move.capture_pawn
        elif isinstance(move, Castle):
            rook = self.board[move.startRow][move.rook_end_col]
            self.board[move.startRow][move.rook_end_col] = None
            self.board[move.startRow][move.rook_start_col] = rook
            rook.is_moved = False
        elif isinstance(move, PawnPromotion):
            move.movedPiece = Pawn(move.movedPiece.color, is_moved=True)
        self.white_to_move = not self.white_to_move
        self.__update_en_passant_pawn(move.movedPiece)
        self.board_val = self.calculate_board_val()
        if validated_move:
            self.all_valid_moves = self.calculate_all_valid_moves()

    def make_move_notation(self, move):
        if self.is_check:
            check = "+"
        else:
            check = ""
        if isinstance(move, Castle):
            if move.endCol == 6:
                return '0-0' + check
            elif move.endCol == 2:
                return '0-0-0' + check
            else:
                raise ValueError('Invalid castle move!')

        pawn_promotion = move.promotedPieceType().name if isinstance(move, PawnPromotion) else ""
        move_notation = move.get_notation()
        from operator import itemgetter
        moves_to_end_sq = itemgetter(
            *[(i, j, move.endRow, move.endCol) for i in range(ROW_NR) for j in range(COL_NR)])(self.all_valid_moves)
        moves_by_same_piece_to_end_sq = tuple(
            filter(lambda move_: move_ is not None and move_.movedPiece.name == move.movedPiece.name, moves_to_end_sq))

        if len(moves_by_same_piece_to_end_sq) != 1:
            moves_from_same_col = \
                tuple(filter(lambda move_: move_.startCol == move.startCol, moves_by_same_piece_to_end_sq))
            if len(moves_from_same_col) == 1:
                move_notation = move_notation[:1] + move.colsToFiles[move.startCol] + move_notation[1:]
            else:
                moves_from_same_row = \
                    tuple(filter(lambda move_: move_.startRow == move.startRow, moves_by_same_piece_to_end_sq))
                if len(moves_from_same_row) == 1:
                    move_notation = move_notation[:1] + move.rowsToRanks[move.startRow] + move_notation[1:]
                else:
                    move_notation = move_notation[:1] + move.get_file_rank(move.startRow,
                                                                           move.startCol) + move_notation[1:]
        if move.capturedPiece is not None:
            move_notation = move_notation[:-2] + "x" + move_notation[-2:]
        if move_notation[0] == Pawn().name:
            move_notation = move_notation[1:]
        return move_notation + pawn_promotion + check

    def check_if_check(self):
        self.white_to_move = not self.white_to_move
        moves = self.calculate_all_possible_moves()
        self.is_check = len(set(filter(lambda move: move is not None and isinstance(move.capturedPiece, King), moves))) > 0
        self.white_to_move = not self.white_to_move

    def get_move_from_notation(self, notation):
        if notation == '0-0':
            if self.white_to_move:
                return self.all_valid_moves.get((7, 4, 7, 6))
            else:
                return self.all_valid_moves.get((0, 4, 0, 6))
        elif notation == '0-0-0':
            if self.white_to_move:
                return self.all_valid_moves.get((7, 4, 7, 2))
            else:
                return self.all_valid_moves.get((0, 4, 0, 4))
        notation = notation.replace('x', '').replace('+', '').replace('=', '')
        promoted_piece_name = ''
        if '8' < notation[-1] < 'a':
            promoted_piece_name = notation[-1]
            notation = notation[:-1]
        piece = None
        color = self.white_to_move
        if notation[0] < 'a':
            piece_name = notation[0]
            notation = notation[1:]
            if piece_name == Knight().name:
                piece = Knight(is_white=color)
            elif piece_name == Bishop().name:
                piece = Bishop(is_white=color)
            elif piece_name == Rook().name:
                piece = Rook(is_white=color)
            elif piece_name == Queen().name:
                piece = Queen(is_white=color)
            elif piece_name == King().name:
                piece = King(is_white=color)
            else:
                raise ValueError('Invalid move notation -> unknown Piece symbol!')
        else:
            piece = Pawn(is_white=color)

        end_col = Move.filesToCols.get(notation[-2])
        end_row = Move.ranksToRows.get(notation[-1])
        from operator import itemgetter
        moves_to_end_sq = itemgetter(
            *[(i, j, end_row, end_col) for i in range(ROW_NR) for j in range(COL_NR)])(self.all_valid_moves)

        moves = list(filter(lambda move_: move_ is not None and move_.movedPiece == piece, moves_to_end_sq))
        if len(notation) == 2:
            pass
        elif len(notation) == 3:
            if notation[0] < 'a':
                start_row = Move.rowsToRanks.get(notation[0])
                moves = list(filter(lambda move_: move_.startRow == start_row, moves))
            else:
                start_col = Move.filesToCols.get(notation[0])
                moves = list(filter(lambda move_: move_.startCol == start_col, moves))
        elif len(notation) == 3:
            start_col = Move.filesToCols.get(notation[0])
            start_row = Move.rowsToRanks.get(notation[1])
            moves = list(filter(lambda move_: move_.startCol == start_col and move_.start_row == start_row, moves))
        else:
            raise ValueError("Invalid move notation length!")
        if len(moves) == 1:
            move = moves[0]
            if promoted_piece_name:
                if promoted_piece_name == 'N':
                    promoted_piece_type = Knight
                elif promoted_piece_name == 'B':
                    promoted_piece_type = Bishop
                elif promoted_piece_name == 'R':
                    promoted_piece_type = Rook
                elif promoted_piece_name == 'Q':
                    promoted_piece_type = Queen
                move.promotedPieceType = promoted_piece_type
            return move
        elif len(moves) == 0:
            raise ValueError("None valid move was parsed from notation!")
        else:
            raise ValueError("More than one valid move were parsed from notation!")

    def play_saved_game(self, saved_game_notation):
        saved_game_len = len(saved_game_notation)
        current_game_len = len(self.game_notation)
        if current_game_len < saved_game_len:
            move_notation = saved_game_notation[current_game_len]
            move = self.get_move_from_notation(move_notation)
            self.make_move(move, validated_move=True, read=True)
        return self.is_game_over

    def save_game_to_csv(self, path):
        with open(path, 'w') as game_notation_file:
            csv_writer = csv.writer(game_notation_file)
            for move_nr in range(0, len(self.game_notation), 2):
                csv_writer.writerow(self.game_notation[move_nr:move_nr+2])
            result = None
            if self.winner == 1:
                result = "1-0"
            elif self.winner == -1:
                result = "0-1"
            elif self.winner == 0:
                result = "0.5-0.5"
            csv_writer.writerow([result])

    @staticmethod
    def read_game_from_csv(path):
        with open(path, 'r') as game_notation_file:
            moves = []
            csv_read = csv.reader(game_notation_file)
            for row in csv_read:
                moves.extend(row)
        return moves[:-1]  # without result

    def reset_clicks(self):
        self.active_square = ()
        self.clicked_squares = []
        self.active_piece_valid_moves = []

    def handle_click(self, location):
        # check is controls clicked
        self.screen.controls.handle_button_click(location, self)

        if self.is_game_started:
            if self.game_mode != "S" or self.is_player_white == self.white_to_move:
                col, row = self.screen.get_square_position(location)

                if col >= COL_NR or row >= ROW_NR or self.active_square == (row, col):
                    self.reset_clicks()
                elif len(self.clicked_squares) == 0:
                    piece = self.board[row][col]
                    if piece is not None and piece.color == self.__get_active_color():
                        self.active_square = (row, col)
                        self.clicked_squares.append(self.active_square)
                        # show possible moves
                        self.active_piece_valid_moves = [move for pos, move in self.all_valid_moves.items() if
                                                         self.active_square == (pos[0], pos[1]) and move is not None]
                else:
                    self.active_square = (row, col)
                    self.clicked_squares.append(self.active_square)

                    # show possible moves
                    self.active_piece_valid_moves = [move for pos, move in self.all_valid_moves.items() if
                                                     self.active_square == (pos[0], pos[1]) and move is not None]

        if len(self.clicked_squares) == 2:
            move = self.all_valid_moves[(*self.clicked_squares[0], *self.clicked_squares[1])]
            self.reset_clicks()
            if move is not None:
                self.make_move(move, validated_move=True)
        return self.is_game_over

    def play_computer_move(self, computer_engine):
        move = self.calculate_engine_move(computer_engine)
        self.make_move(move, validated_move=True, read=True)
        return self.is_game_over

    def calculate_engine_move(self, computer_engine):
        uci_board = self.convert_board_to_uci_notation()
        computer_engine_board = chess.Board(uci_board)
        uci_move = computer_engine.play(computer_engine_board, chess.engine.Limit(time=0.8))
        move = self.get_move_from_uci_notation(str(uci_move.move))
        return move


    # def calculate_engine_move(self, max_lvl, lvl=0):
    #     if lvl >= max_lvl:
    #         return self.board_val
    #     valid_moves = tuple(filter(lambda move: move is not None, self.all_valid_moves.values()))
    #     best_move = None
    #     best_val = None
    #     if self.white_to_move:
    #         max_ = float('-inf')
    #         for move in valid_moves:
    #             self.make_move(move, validated_move=True)
    #             if self.calculate_engine_move(max_lvl, lvl+1) > max_:
    #                 best_move = move
    #                 max_ = self.calculate_engine_move(max_lvl, lvl+1)
    #             self.undo_move(validated_move=True)
    #         best_val = max_
    #     else:
    #         min_ = float('inf')
    #         for move in valid_moves:
    #             self.make_move(move, validated_move=True)
    #             move_val = self.calculate_engine_move(max_lvl, lvl+1)
    #             if move_val < min_:
    #                 best_move = move
    #                 min_ = move_val
    #             self.undo_move(validated_move=True)
    #         best_val = min_
    #     if lvl == 0:
    #         return best_move
    #     else:
    #         return best_val

    def draw_chessboard(self):
        self.screen.draw_board(self.active_square, self.active_piece_valid_moves, self)

    def start_game(self):
        self.reset()
        if self.game_mode == "H":
            self.is_game_started = True
        elif self.game_mode == "K":
            None
        elif self.game_mode == "S":
            self.network.connect()

    def end_game(self):
        self.is_game_started = False

    def convert_board_to_uci_notation(self):
        uci_notation_list = []
        for r in range(ROW_NR):
            uci_notation_list.append([])
            for c in range(COL_NR):
                piece = self.board[r][c]
                if piece is not None:
                    uci_notation_list[-1].append(piece.name if piece.color == "W" else piece.name.lower())
                elif c == 0 or not uci_notation_list[-1][-1].isnumeric():
                    uci_notation_list[-1].append("1")
                else:
                    pawn_in_row_ctr = int(uci_notation_list[-1].pop()) + 1
                    uci_notation_list[-1].append(str(pawn_in_row_ctr))
        uci_notation = '/'.join([''.join(field) for field in uci_notation_list])
        if self.white_to_move:
            to_move = "w"
        else:
            to_move = "b"
        footer = "KQkq - 0 " + str(int(len(self.game_notation) / 2 + 1))
        uci_notation = uci_notation + " " + to_move + " " + footer
        return uci_notation

    def get_move_from_uci_notation(self, uci_notation):
        start_col = Move.filesToCols.get(uci_notation[0])
        start_row = Move.ranksToRows.get(uci_notation[1])
        end_col = Move.filesToCols.get(uci_notation[2])
        end_row = Move.ranksToRows.get(uci_notation[3])
        move = self.all_valid_moves.get((start_row, start_col, end_row, end_col))
        return move

    def receive_from_server(self):
        data = "WAITING"
        if self.is_game_started:
            data = "W:" + self.last_move_white if self.is_player_white else "B:" + self.last_move_black
        if self.is_game_over:
            data = "END"
        reply = self.network.send(data)
        if reply == "WAITING":
            None
        elif reply == "END":
            self.network.disconnect()
            self.game_over()
        elif reply == "START":
            self.is_game_started = True
            self.is_player_white = self.network.id == "0"
        else:
            self.check_is_enemy_moved(reply)

    def check_is_enemy_moved(self, reply):
        move_white, move_black = reply.split(":")
        last_enemy_move = move_black if self.is_player_white else move_white
        if last_enemy_move != self.last_move_white and last_enemy_move != self.last_move_black:
            move = self.get_move_from_notation(last_enemy_move)
            self.make_move(move, validated_move=True, read=True, enemy=True)

