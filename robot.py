import random

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