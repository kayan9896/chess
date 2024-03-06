import chess

class AI:
    def __init__(self):
        pass

    def evaluate_board(self, board):
        # Evaluate the board position
        # Here, you can implement your own evaluation function to assign a score to the board state
        score = 0
        for piece in board.piece_map().values():
            if piece.color == chess.BLACK:
                score += self.get_piece_value(piece)
            else:
                score -= self.get_piece_value(piece)
        return score

    def get_piece_value(self, piece):
        # Assign values to different pieces
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000
        }
        return 0 if not piece else piece_values[piece.piece_type]

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return None, self.evaluate_board(board)

        legal_moves = list(board.legal_moves)
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            legal_moves.sort(key=lambda move: -self.get_piece_value(board.piece_at(move.to_square)))
            for move in legal_moves:
                board.push(move)
                _, eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            legal_moves.sort(key=lambda move: self.get_piece_value(board.piece_at(move.to_square)))
            for move in legal_moves:
                board.push(move)
                _, eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

