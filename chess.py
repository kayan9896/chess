from piece import Piece
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn

class Chess:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def initialize_board(self):
        # Place white pieces
        self.board[0][0] = Rook(0, 0, 'white')
        self.board[0][1] = Knight(0, 1, 'white')
        self.board[0][2] = Bishop(0, 2, 'white')
        self.board[0][3] = Queen(0, 3, 'white')
        self.board[0][4] = King(0, 4, 'white')
        self.board[0][5] = Bishop(0, 5, 'white')
        self.board[0][6] = Knight(0, 6, 'white')
        self.board[0][7] = Rook(0, 7, 'white')
        for i in range(8):
            self.board[1][i] = Pawn(1, i, 'white')

        # Place black pieces (mirrored)
        self.board[7][0] = Rook(7, 0, 'black')
        self.board[7][1] = Knight(7, 1, 'black')
        self.board[7][2] = Bishop(7, 2, 'black')
        self.board[7][3] = Queen(7, 3, 'black')
        self.board[7][4] = King(7, 4, 'black')
        self.board[7][5] = Bishop(7, 5, 'black')
        self.board[7][6] = Knight(7, 6, 'black')
        self.board[7][7] = Rook(7, 7, 'black')
        for i in range(8):
            self.board[6][i] = Pawn(6, i, 'black')

    def print_board(self):
        piece_symbols = {'R': 'Rook', 'H': 'Knight', 'B': 'Bishop', 'Q': 'Queen', 'K': 'King', 'P': 'Pawn'}
        for row in self.board:
            for piece in row:
                if piece is None:
                    print("..", end=" ")
                else:
                    side_char = 'W' if piece.side == 'white' else 'B'
                    piece_char = piece_symbols[type(piece).__name__[0]]  # Get first letter of class name
                    print(side_char + piece_char, end=" ")
            print()