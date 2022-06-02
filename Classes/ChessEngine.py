import pygame as p

# from Classes.Pieces.Pawn import Pawn
# from Classes.Pieces.Knight import Knight
# from Classes.Pieces.Bishop import Bishop
# from Classes.Pieces.Rook import Rook
# from Classes.Pieces.Queen import Queen
# from Classes.Pieces.King import King

from Pieces import *
from Moves import *
from GUI import *
from Screen import Screen
from network import Network
import csv

ROW_NR = 8
COL_NR = 8


def init_all_valid_moves():
    return {(sr, sc, er, ec): None for sr in range(ROW_NR) for sc in range(COL_NR)
            for er in range(ROW_NR) for ec in range(COL_NR)}


class ChessEngine:
    def __init__(self, screen_width, screen_height, row_size):
        self.board = [
            [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False),
             Rook(False)],
            [Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True)],
            [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)],
        ]
        self.white_to_move = True
        self.screen = Screen(screen_width, screen_height, row_size, self.board)
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
        self.game_mode = "H"
        self.network = Network()
        self.game_notation = []
        self.is_game_over = False
        self.winner = None
        self.is_check = False

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
            self.white_to_move = not self.white_to_move
            all_moves_at_the_end = self.calculate_all_possible_moves()
            for end_move in all_moves_at_the_end:
                if isinstance(end_move.capturedPiece, King):
                    self.is_game_over = True
                    self.winner = 1 if self.white_to_move else -1
                    self.game_notation.append(self.game_notation.pop() + "+")
                    winner = "White" if self.white_to_move else "Black"
                    print(f'Game is ended. {winner} has won!')
                    return
            self.is_game_over = True
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

    def make_move(self, move, validated_move=False, read=False):
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
            self.game_notation.append(self.make_move_notation(move))
            self.__update_en_passant_pawn()
            self.all_valid_moves = self.calculate_all_valid_moves()
            try:
                if self.game_mode == "S":
                    data = self.game_notation[-1]
                    print(data)
                    reply = self.network.send(data)
            except:
                None
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
                    move_notation = move_notation[:1] + move.get_file_rank(move.startRow, move.startCol) + move_notation[1:]
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

    def play_saved_game(self, game_notation):
        move_notation = game_notation[len(self.game_notation)]
        move = self.get_move_from_notation(move_notation)
        self.make_move(move, validated_move=True, read=True)
        self.__check_if_game_is_over()
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
            row_nr = len(self.board)
            col_nr = len(self.board[0])
            col, row = self.screen.get_square_position(location)

            if col >= col_nr or row >= row_nr or self.active_square == (row, col):
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
                self.__check_if_game_is_over()
        return self.is_game_over

    def make_engine_move(self):
        # move = random.choice(tuple(filter(lambda move: move is not None, self.all_valid_moves.values())))
        move = self.calculate_engine_move(max_lvl=2)
        self.make_move(move, validated_move=True)

    def calculate_engine_move(self, max_lvl, lvl=0):
        if lvl >= max_lvl:
            return self.board_val
        valid_moves = tuple(filter(lambda move: move is not None, self.all_valid_moves.values()))
        best_move = None
        best_val = None
        if self.white_to_move:
            max_ = float('-inf')
            for move in valid_moves:
                self.make_move(move, validated_move=True)
                if self.calculate_engine_move(max_lvl, lvl+1) > max_:
                    best_move = move
                    max_ = self.calculate_engine_move(max_lvl, lvl+1)
                self.undo_move(validated_move=True)
            best_val = max_
        else:
            min_ = float('inf')
            for move in valid_moves:
                self.make_move(move, validated_move=True)
                move_val = self.calculate_engine_move(max_lvl, lvl+1)
                if move_val < min_:
                    best_move = move
                    min_ = move_val
                self.undo_move(validated_move=True)
            best_val = min_
        if lvl == 0:
            return best_move
        else:
            return best_val

    def draw_chessboard(self):
        self.screen.draw_board(self.active_square, self.active_piece_valid_moves, self)

    def start_game(self):
        if self.game_mode == "H":
            self.is_game_started = True
        elif self.game_mode == "K":
            None
        elif self.game_mode == "S":
            self.network.connect()
            self.is_game_started = True

    def end_game(self):
        self.is_game_started = False
