class Piece:
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side

    def can_move(self, end_x, end_y):
        # Not implemented, should be specific to each piece type
        pass

    def can_kill(self, other_piece):
        # Not implemented, should be specific to each piece type
        pass