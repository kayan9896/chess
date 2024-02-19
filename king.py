from piece import Piece

class King(Piece):
    def can_move(self, end_x, end_y, board):
        # Check if within one square in any direction
        if abs(self.x - end_x) <= 1 and abs(self.y - end_y) <= 1:
            # Check if the target square is empty or has an opponent's piece
            if board[end_x][end_y] is None or board[end_x][end_y].side != self.side:
                return True
        return False

    def can_kill(self, other_piece,board):
        # Kings can "kill" by moving to the opponent's square
        return self.can_move(other_piece.x, other_piece.y, board)