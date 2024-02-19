from piece import Piece

class Knight(Piece):
    def can_move(self, end_x, end_y, board):
        # Check all possible L-shaped moves
        possible_moves = {
            (self.x + 2, self.y + 1), (self.x + 2, self.y - 1),
            (self.x - 2, self.y + 1), (self.x - 2, self.y - 1),
            (self.x + 1, self.y + 2), (self.x + 1, self.y - 2),
            (self.x - 1, self.y + 2), (self.x - 1, self.y - 2)
        }

        # Check if the target square is within the board and valid
        if 0 <= end_x < 8 and 0 <= end_y < 8 and (end_x, end_y) in possible_moves:
            # Check if the target square is empty or has an opponent's piece
            if board[end_x][end_y] is None or board[end_x][end_y].side != self.side:
                return True
        return False

    def can_kill(self, other_piece, board):
        return self.can_move(other_piece.x, other_piece.y, board)