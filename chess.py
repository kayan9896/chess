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
        self.player = 'white'

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
                    print("__", end=" ")
                else:
                    side_char = 'W' if piece.side == 'white' else 'B'
                    piece_char = piece_symbols[type(piece).__name__[0]]  # Get first letter of class name
                    print(side_char + piece_char[0], end=" ")
            print()

    
    def move(self, start_x, start_y, end_x, end_y):
        piece = self.board[start_x][start_y]
        if not piece: return False
        if piece.side==self.player and piece.can_move(end_x, end_y, self.board):
            if self.board[end_x][end_y] and piece.can_kill(self.board[end_x][end_y], self.board):
                self.board[end_x][end_y] = None  # Remove the killed piece
            self.board[end_x][end_y] = piece
            self.board[start_x][start_y] = None
            piece.x = end_x
            piece.y = end_y
            if isinstance(piece, Pawn):
                piece.has_moved = True  # Update pawn's movement status
            return True
        else:
            return False

    def game_over(self):
        white_king_found = False
        black_king_found = False
        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    if piece.side == 'white':
                        white_king_found = True
                    else:
                        black_king_found = True
        return not (white_king_found and black_king_found)

    def checkmate(self, side):
        king_x, king_y = None, None
        r1=False
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if isinstance(piece, King) and piece.side == side:
                    king_x, king_y = i, j
                    break
            if king_x is not None:
                break

        # Check if the king is in check
        for i in range(8):
            if r1:
                break
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None and piece.side != side and piece.can_kill(King(king_x, king_y, side), self.board):
                    r1=True
                    break

        # Check if the king can move to any safe square
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= king_x + i < 8 and 0 <= king_y + j < 8 and \
                   self.move(king_x, king_y, king_x + i, king_y + j):
                    self.move(king_x + i, king_y + j, king_x, king_y)  # Undo the move
                    return False

        return r1

    def play(self):
        self.player = 'white'
        while True:
            self.print_board()
            print(f"{self.player.capitalize()}'s turn:")

            try:
                start_x, start_y = map(int, input("Enter start coordinates (x,y): ").split(','))
                end_x, end_y = map(int, input("Enter end coordinates (x,y): ").split(','))
            except ValueError:
                print("Invalid input format. Please enter coordinates as x,y (e.g., 0,1)")
                continue

            if self.move(start_x, start_y, end_x, end_y):
                if self.game_over():
                    self.print_board()
                    print(f"{self.player.capitalize()} wins!")
                    break
                elif self.checkmate(self.player):
                    self.print_board()
                    print(f"{self.player.capitalize()} is in checkmate!")
                    break
                else:
                    self.player = 'black' if self.player == 'white' else 'white'
            else:
                print("Illegal move. Try again.")

if __name__ == "__main__":
    game = Chess()
    game.initialize_board()
    game.play()
    