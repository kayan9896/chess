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
        if not self.is_valid_square(start) or not self.is_valid_square(end):
            return False
        
        start_index = self.square_to_index(start)
        end_index = self.square_to_index(end)

        # Get the piece type at the start square
        piece_type = self.get_piece_type(start_index)
        if piece_type:
            # Call the specific function based on the piece type
            if piece_type == 'rook':
                return self.rook_can_move(start_index, end_index)
            elif piece_type == 'knight':
                return self.knight_can_move(start_index, end_index)
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
        if piece_type_at_end and piece_type_at_end[0] == self.player[0]:
            return False
        
        return True

    
    def knight_can_move(self, start_index, end_index):
        # Implement knight movement logic here
        pass
    
    # Add more functions for other piece types as needed

# Sample usage
chess = Chess()
chess.initialize_board()
chess.print_board()
