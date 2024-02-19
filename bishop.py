from piece import Piece

class Bishop(Piece):
    def can_move(self, end_x, end_y, board):
        # Check if moving diagonally
        if abs(self.x - end_x) == abs(self.y - end_y):
            # Check for obstructions in the path
            step_x = 1 if end_x > self.x else -1
            step_y = 1 if end_y > self.y else -1
            for i in range(1, abs(end_x - self.x)):
                if board[self.x + i * step_x][self.y + i * step_y] is not None:
                    return False

            # Check if the target square is empty or has an opponent's piece
            if board[end_x][end_y] is None or board[end_x][end_y].side != self.side:
                return True
        return False

    def can_kill(self, other_piece, board):
        return self.can_move(other_piece.x, other_piece.y, board)