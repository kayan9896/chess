import chess
from ai import AI  # Assuming the AI class is implemented in a separate file named "ai.py"

class ConsoleChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.ai = AI()

    def play(self):
        print("Welcome to Console Chess!")
        print("Enter moves in algebraic notation (e.g., e2e4)")
        print("Type 'quit' to exit.\n")
        
        while not self.board.is_game_over():
            self.print_board()
            if self.board.turn == chess.WHITE:
                move = input("Your move: ")
                if move.lower() == 'quit':
                    break
                try:
                    self.board.push_san(move)
                except ValueError:
                    print("Invalid move. Try again.")
            else:
                print("AI is thinking...")
                best_move, s = self.ai.minimax(self.board, 6, float('-inf'), float('inf'), False)
                print(s)
                self.board.push(best_move)

        print("Game over.")
        print("Result: " + self.board.result())

    def print_board(self):
        print("\n" + self.board.__str__())
        print("  a b c d e f g h\n")

if __name__ == "__main__":
    game = ConsoleChessGame()
    game.play()
