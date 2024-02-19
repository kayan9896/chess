from piece import Piece

class Knight(Piece):
    def can_move(self, end_x, end_y, board):
        # Check if the move is L-shaped (2 steps in one direction, 1 step perpendicular)
        if (abs(self.x - end_x) == 2 and abs(self.y - end_y) == 1) or \
           (abs(self.x - end_x) == 1 and abs(self.y - end_y) == 2):
            # Check if the target square is empty or has an opponent's piece
            if board[end_x][end_y] is None or board[end_x][end_y].side != self.side:
                return True
        return False
    '''
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
        return False'''

    def can_kill(self, other_piece, board):
        if not other_piece: return False
        return self.can_move(other_piece.x, other_piece.y, board)

        

