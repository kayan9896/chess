from piece import Piece
from rook import Rook  # Import Rook logic
from bishop import Bishop  # Import Bishop logic

class Queen(Piece):
    def can_move(self, end_x, end_y, board):
        # Combine Rook and Bishop movement logic
        return Rook(self.x, self.y, self.side).can_move(end_x, end_y, board) or \
               Bishop(self.x, self.y, self.side).can_move(end_x, end_y, board)

    def can_kill(self, other_piece, board):
        return self.can_move(other_piece.x, other_piece.y, board)