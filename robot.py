import random
from piece import Piece
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn

class Robot:
    def __init__(self, side):
        self.side = side

    def get_move(self, board):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece.side == self.side:
                    for x in range(8):
                        for y in range(8):
                            if piece.can_move(x, y, board):
                                valid_moves.append((i, j, x, y))  # Store (start_x, start_y, end_x, end_y)

        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None  # No valid moves (e.g., checkmate)


    def eval(self, board):
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    value = self.get_piece_value(piece)
                    if piece.side == self.side:
                        score += value
                    else:
                        score -= value
        return score

    def get_piece_value(self, piece):
        if isinstance(piece, Pawn):
            return 1
        elif isinstance(piece, Knight) or isinstance(piece, Bishop):
            return 3
        elif isinstance(piece, Rook):
            return 5
        elif isinstance(piece, Queen):
            return 9
        elif isinstance(piece, King):
            return 1000  # High value to prioritize king safety