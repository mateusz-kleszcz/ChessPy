from GUI.Screen import Screen

WIDTH = 1280
HEIGHT = 720


class ChessEngine:
    def __init__(self):
        self.board = [
            ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
            ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
            ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
            ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"],
        ]
        self.isWhiteMove = True
        self.screen = Screen(WIDTH, HEIGHT, self.board)

    def draw_chessboard(self):
        self.screen.draw_board()
