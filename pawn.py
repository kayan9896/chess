from piece import Piece

class Pawn(Piece):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        self.has_moved = False  # Track if the pawn has made its initial move

    def can_move(self, end_x, end_y, board):
        direction = 1 if self.side == 'white' else -1  # White moves up, black moves down

        # Check for one-square forward move
        if end_x == self.x + direction and end_y == self.y and board[end_x][end_y] is None:
            return True

        # Check for two-square initial move
        if not self.has_moved and end_x == self.x + 2 * direction and end_y == self.y and \
           board[self.x + direction][self.y] is None and board[end_x][end_y] is None:
            return True

        return False  # No other valid moves

    def can_kill(self, other_piece, board):
        if not other_piece: return False
        direction = 1 if self.side == 'white' else -1
        # Check for diagonal capture
        return abs(other_piece.x - self.x) == 1 and other_piece.y - self.y == direction and \
               other_piece.side != self.side

    def enpassant(self, other_pawn, board):
        # Placeholder - to be implemented later
        pass

    def promote(self):
        # Placeholder - to be implemented later
        pass