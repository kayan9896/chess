from copy import deepcopy
class AI:
    def __init__(self, side):
        self.side = side
    
    def evaluate_score(self, chess):
        score = 0
        for piece, bitboard in chess.white_pieces.items():
            if piece == 'king':
                score += 1000 * bin(bitboard).count('1')
            elif piece == 'queen':
                score += 9 * bin(bitboard).count('1')
            elif piece == 'rook':
                score += 5 * bin(bitboard).count('1')
            elif piece == 'bishop' or piece == 'knight':
                score += 3 * bin(bitboard).count('1')
            elif piece == 'pawn':
                score += 1 * bin(bitboard).count('1') 
        for piece, bitboard in chess.black_pieces.items():
            if piece == 'king':
                score -= 1000 * bin(bitboard).count('1')
            elif piece == 'queen':
                score -= 9 * bin(bitboard).count('1')
            elif piece == 'rook':
                score -= 5 * bin(bitboard).count('1')
            elif piece == 'bishop' or piece == 'knight':
                score -= 3 * bin(bitboard).count('1')
            elif piece == 'pawn':
                score -= 1 * bin(bitboard).count('1')           

        return score if self.side=='white' else -score

    def get_move(self, chess):
        best_move, best_score = self.minimax(chess, 3, -float('inf'), float('inf'),True)
        return best_move

    def minimax(self, chess, depth, alpha, beta, maximizing_player):
        if depth == 0 or chess.game_over():
            return None, self.evaluate_score(chess)
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            legal_moves = self.generate_legal_moves(chess)
            for move in legal_moves:
                chessc=self.make_move(chess,move)
                '''
                chess.move(move[0],move[1])
                chess.player = 'black' if chess.player == 'white' else 'white'
                '''
                _, eval = self.minimax(chessc, depth - 1, alpha, beta, False)
                #chess.undo()
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
            legal_moves = self.generate_legal_moves(chess)
            for move in legal_moves:
                chessc=self.make_move(chess,move)
                '''
                chess.move(move[0],move[1])
                chess.player = 'black' if chess.player == 'white' else 'white'
                '''
                _, eval = self.minimax(chessc, depth - 1, alpha, beta, True)
                #chess.undo()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def make_move(self, chess, move):
        chess_copy = deepcopy(chess)
        chess_copy.move(move[0], move[1])
        return chess_copy

    def generate_legal_moves(self, chess):
        legal_moves = []
        for file in 'abcdefgh':
            for rank in '12345678':
                start = file + rank
                for file_end in 'abcdefgh':
                    for rank_end in '12345678':
                        end = file_end + rank_end
                        if chess.can_move(start, end):
                            legal_moves.append((start, end))
        return legal_moves