from ai import AI
class Chess:
    def __init__(self):
        self.white_pieces = {
            'pawn': 0,
            'rook': 0,
            'knight': 0,
            'bishop': 0,
            'queen': 0,
            'king': 0
        }
        self.black_pieces = {
            'pawn': 0,
            'rook': 0,
            'knight': 0,
            'bishop': 0,
            'queen': 0,
            'king': 0
        }
        self.player = 'white'
        self.moves_history = []

    def initialize_board(self):
        # Place white pieces
        self.white_pieces['queen'] = 0b00001000
        self.white_pieces['king'] = 0b00010000
        self.white_pieces['bishop'] = 0b00100100
        self.white_pieces['knight'] = 0b01000010
        self.white_pieces['rook'] = 0b10000001
        self.white_pieces['pawn'] = 0b11111111 << 8

        # Place black pieces (mirrored)
        self.black_pieces['queen'] = 0b00001000 << 56
        self.black_pieces['king'] = 0b00010000 << 56
        self.black_pieces['bishop'] = 0b00100100 << 56
        self.black_pieces['knight'] = 0b01000010 << 56
        self.black_pieces['rook'] = 0b10000001 << 56
        self.black_pieces['pawn'] = 0b11111111 << 48

    def print_board(self):
        print("   a b c d e f g h")
        print("  -----------------")
        for i in range(7,-1,-1):
            print(i+1, end='| ')
            for j in range(8):
                found_piece = False
                for piece_type, bitboard in self.white_pieces.items():
                    if bitboard & (1 << (i * 8 + j)):
                        print(piece_type[0].upper(), end=' ')
                        found_piece = True
                        break
                if not found_piece:
                    for piece_type, bitboard in self.black_pieces.items():
                        if bitboard & (1 << (i * 8 + j)):
                            print(piece_type[0], end=' ')
                            found_piece = True
                            break
                if not found_piece:
                    print('-', end=' ')
            print('|')
        print("  -----------------")

    def can_move(self, start, end):
        # Check if the start and end squares are valid
        if start==end: return False
        if not self.is_valid_square(start) or not self.is_valid_square(end):
            return False
        
        start_index = self.square_to_index(start)
        end_index = self.square_to_index(end)

        # Get the piece type at the start square
        piece_type = self.get_piece_type(start_index)
        if piece_type and piece_type[0]==self.player:
            # Call the specific function based on the piece type
            if piece_type[1] == 'rook':
                return self.rook_can_move(start_index, end_index)
            elif piece_type[1] == 'knight':
                return self.knight_can_move(start_index, end_index)
            elif piece_type[1] == 'bishop':
                return self.bishop_can_move(start_index, end_index)
            elif piece_type[1] == 'queen':
                return self.queen_can_move(start_index, end_index)
            elif piece_type[1] == 'king':
                return self.king_can_move(start_index, end_index)
            elif piece_type[1] == 'pawn':
                return self.pawn_can_move(start_index, end_index)
            # Add more piece types as needed
            
        return False
    
    def is_valid_square(self, square):
        file, rank = square
        return file in 'abcdefgh' and rank in '12345678'
    
    def square_to_index(self, square):
        file, rank = square
        file_index = ord(file) - ord('a')
        rank_index = int(rank) - 1
        return rank_index * 8 + file_index
    
    def get_piece_type(self, index):
        for piece_type, bitboard in self.white_pieces.items():
            if bitboard & (1 << index):
                return ('white',piece_type)
        for piece_type, bitboard in self.black_pieces.items():
            if bitboard & (1 << index):
                return ('black',piece_type)
        return None
    
    def rook_can_move(self, start_index, end_index):
        # Check if start and end squares are in the same row or column
        start_row = start_index // 8
        start_col = start_index % 8
        end_row = end_index // 8
        end_col = end_index % 8
        if start_row != end_row and start_col != end_col: return False
        if start_row == end_row:
            # Check if there are no pieces between start and end squares on the same row
            if start_col < end_col:
                for col in range(start_col + 1, end_col):
                    if self.get_piece_type(start_row * 8 + col):
                        return False
            else:
                for col in range(start_col - 1, end_col, -1):
                    if self.get_piece_type(start_row * 8 + col):
                        return False
        elif start_col == end_col:
            # Check if there are no pieces between start and end squares on the same column
            if start_row < end_row:
                for row in range(start_row + 1, end_row):
                    if self.get_piece_type(row * 8 + start_col):
                        return False
            else:
                for row in range(start_row - 1, end_row, -1):
                    if self.get_piece_type(row * 8 + start_col):
                        return False
        
        # Check if the end square is occupied by a piece of the same side
        piece_type_at_end = self.get_piece_type(end_index)
        if piece_type_at_end and piece_type_at_end[0] == self.player:
            return False
        return True

    def bishop_can_move(self, start_index, end_index):
        # Check if start and end squares are on the same diagonal
        start_row, start_col = divmod(start_index, 8)
        end_row, end_col = divmod(end_index, 8)
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        
        # Determine direction of movement
        row_dir = 1 if end_row > start_row else -1
        col_dir = 1 if end_col > start_col else -1
        
        # Check for obstacles on the diagonal path
        row, col = start_row + row_dir, start_col + col_dir
        while row != end_row:
            if self.get_piece_type(row * 8 + col):
                return False
            row += row_dir
            col += col_dir
        
        # Check if the end square is either empty or occupied by an opponent's piece
        piece_type_at_end = self.get_piece_type(end_index)
        if piece_type_at_end and piece_type_at_end[0] == self.player:
            return False
        return True

    def queen_can_move(self, start_index, end_index):
        # Check if the queen can move like a rook or a bishop
        return self.rook_can_move(start_index, end_index) or self.bishop_can_move(start_index, end_index)

    def knight_can_move(self, start_index, end_index):
        # Check if the move is a valid knight move
        valid_moves = {10, 17, 15, 6, -10, -17, -15, -6}
        diff = end_index - start_index
        if diff in valid_moves:
            # Check if the end square is empty or occupied by an opponent's piece
            piece_type_at_end = self.get_piece_type(end_index)
            if piece_type_at_end and piece_type_at_end[0] == self.player:
                return False
            return True
        return False

    def king_can_move(self, start_index, end_index):
        # Check if the move is a valid king move
        valid_moves = {-9, -8, -7, -1, 1, 7, 8, 9}
        diff = end_index - start_index
        if diff in valid_moves:
            # Check if the end square is empty or occupied by an opponent's piece
            piece_type_at_end = self.get_piece_type(end_index)
            if piece_type_at_end and piece_type_at_end[0] == self.player:
                return False
            return True
        return False

    def pawn_can_move(self, start_index, end_index):
        # Check if the move is a valid pawn move
        diff = end_index - start_index
        if self.player == 'white':
            if diff == 8:
                # Check if the end square is empty
                if not self.get_piece_type(end_index):
                    return True
            elif diff == 16 and start_index // 8 == 1:
                # Check if the pawn is in its initial position and the two cells in front are empty
                if not self.get_piece_type(end_index) and not self.get_piece_type(end_index - 8):
                    return True
            elif diff == 7 or diff == 9:
                # Check if the pawn captures an opponent's piece diagonally
                piece_type_at_end = self.get_piece_type(end_index)
                if piece_type_at_end and piece_type_at_end[0] != self.player:
                    return True
        else:  # player is black
            if diff == -8:
                # Check if the end square is empty
                if not self.get_piece_type(end_index):
                    return True
            elif diff == -16 and start_index // 8 == 6:
                # Check if the pawn is in its initial position and the two cells in front are empty
                if not self.get_piece_type(end_index) and not self.get_piece_type(end_index + 8):
                    return True
            elif diff == -7 or diff == -9:
                # Check if the pawn captures an opponent's piece diagonally
                piece_type_at_end = self.get_piece_type(end_index)
                if piece_type_at_end and piece_type_at_end[0] != self.player:
                    return True
        return False

    # Add more functions for other piece types as needed

    def move(self, start, end):
        # Check if the move is valid
        if self.can_move(start, end):
            start_index = self.square_to_index(start)
            end_index = self.square_to_index(end)
            self.moves_history.append((start, end))
            # Move the piece
            piece_type = self.get_piece_type(start_index)
            if piece_type:
                if self.player == 'white':
                    piece_type_at_end = self.get_piece_type(end_index)
                    if piece_type_at_end:
                        self.black_pieces[piece_type_at_end[1]] &= ~(1 << end_index)
                        self.moves_history[-1]=(start, end, piece_type_at_end[1])
                    self.white_pieces[piece_type[1]] &= ~(1 << start_index)
                    self.white_pieces[piece_type[1]] |= (1 << end_index)
                else:
                    piece_type_at_end = self.get_piece_type(end_index)
                    if piece_type_at_end:
                        self.white_pieces[piece_type_at_end[1]] &= ~(1 << end_index)
                        self.moves_history[-1]=(start, end, piece_type_at_end[1])
                    self.black_pieces[piece_type[1]] &= ~(1 << start_index)
                    self.black_pieces[piece_type[1]] |= (1 << end_index)
                return True
        return False

    def undo(self):
        if self.moves_history:
            last_move = self.moves_history.pop()
            start, end = last_move[:2]
            start_index = self.square_to_index(start)
            end_index = self.square_to_index(end)

            # Restore the moved piece
            piece_type = self.get_piece_type(end_index)
            if piece_type:
                if self.player == 'black':
                    self.white_pieces[piece_type[1]] &= ~(1 << end_index)
                    self.white_pieces[piece_type[1]] |= (1 << start_index)
                else:
                    self.black_pieces[piece_type[1]] &= ~(1 << end_index)
                    self.black_pieces[piece_type[1]] |= (1 << start_index)

            # Restore captured piece if any
            if len(last_move) == 3:
                captured_piece = last_move[2]
                if self.player == 'black':
                    self.black_pieces[captured_piece] |= (1 << end_index)
                else:
                    self.white_pieces[captured_piece] |= (1 << end_index)

            # Toggle player back
            self.player = 'black' if self.player == 'white' else 'white'

            return True
        return False

    def game_over(self):
        # Check if one side's king is captured
        if self.white_pieces['king'] == 0 or self.black_pieces['king'] == 0:
            return True
        return False

    def play(self):
        game_mode = input("Play against human or robot? (h/r): ")
        ai=AI('black')
        self.initialize_board()
        while not self.game_over():
            self.print_board()
            if self.player == 'white' or (self.player == 'black' and game_mode=='h'):
                start = input("Enter start position (e.g., 'a2'): ")
                end = input("Enter end position (e.g., 'a4'): ")
                # Check if the move is valid and execute it
                if self.move(start, end):
                    # Provide player feedback
                    print("Move successful!")
                    # Check if the game is over
                    if self.game_over():
                        # Print the final board
                        self.print_board()
                        # Print the winner
                        print(f"Game over! {self.player} wins!")
                        break
                    self.player = 'black' if self.player == 'white' else 'white'
                else:
                    # Provide player feedback
                    print("Invalid move! Please try again.")
            else:
                # AI makes a move
                bestmove = ai.get_move(self)
                if bestmove:
                    self.move(bestmove[0],bestmove[1])
                    self.player = 'white'
                    self.print_board()
                else:
                    print(f"Game over! white wins!")
                    break

        

# Sample usage
chess = Chess()
chess.play()


