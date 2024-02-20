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

    def get_move(self, board):
        best_move, best_score = self.minimax(board, 4, True, -float('inf'), float('inf'))
        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if depth == 0 or self.is_game_over(board):
            return None, self.eval(board)

        if is_maximizing:
            best_score = -float('inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    piece = board[i][j]
                    if piece and piece.side == self.side:
                        for x in range(8):
                            for y in range(8):
                                if piece.can_move(x, y, board):
                                    new_board = self.simulate_move(board, i, j, x, y)
                                    _, score = self.minimax(new_board, depth - 1, False, alpha, beta)
                                    if score > best_score:
                                        best_score = score
                                        best_move = (i, j, x, y)
                                    alpha = max(alpha, score)
                                    if beta <= alpha:
                                        break  # Beta cutoff
            return best_move, best_score
        else:
            best_score = float('inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    piece = board[i][j]
                    if piece and piece.side != self.side:
                        for x in range(8):
                            for y in range(8):
                                if piece.can_move(x, y, board):
                                    new_board = self.simulate_move(board, i, j, x, y)
                                    _, score = self.minimax(new_board, depth - 1, True, alpha, beta)
                                    if score < best_score:
                                        best_score = score
                                        best_move = (i, j, x, y)
                                    beta = min(beta, score)
                                    if beta <= alpha:
                                        break  # Alpha cutoff
            return best_move, best_score


    def is_game_over(self, board):
        white_king_found = False
        black_king_found = False
        for row in board:
            for piece in row:
                if isinstance(piece, King):
                    if piece.side == 'white':
                        white_king_found = True
                    else:
                        black_king_found = True
        return not (white_king_found and black_king_found)

    def simulate_move(self, board, start_x, start_y, end_x, end_y):
        # Create a copy of the board and make the move on the copy
        new_board = [row[:] for row in board]
        new_board[end_x][end_y] = new_board[start_x][start_y]
        new_board[start_x][start_y] = None
        return new_board