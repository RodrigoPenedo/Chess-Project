class Board(object):
    # The chess board is represented as a 8x8 2D array
    def __init__(self):
        # Create the board and move pieces to their initial positions
        self.__board = [[None] * 8 for i in range(8)]
        for i in range(0,8):
            self.__board[1][i] = Pawn("b")
            self.__board[6][i] = Pawn("w")
        self.__board[0][0] = Rook("b")
        self.__board[7][0] = Rook("w")
        self.__board[0][1] = Knight("b")
        self.__board[7][1] = Knight("w")
        self.__board[0][2] = Bishop("b")
        self.__board[7][2] = Bishop("w")
        self.__board[0][3] = Queen("b")
        self.__board[7][3] = Queen("w")
        self.__board[0][4] = King("b")
        self.__board[7][4] = King("w")
        self.__board[0][5] = Bishop("b")
        self.__board[7][5] = Bishop("w")
        self.__board[0][6] = Knight("b")
        self.__board[7][6] = Knight("w")
        self.__board[0][7] = Rook("b")
        self.__board[7][7] = Rook("w")

    def move(self, from_coords, to_coords):
        piece = self.__board[from_coords[0]][from_coords[1]]
        if piece is not None:  # Check if piece exists
            if piece.check_legal_move(from_coords, self.__board, to_coords):  # Check if the move is legal
                # Move the piece and then remove it from its original position
                self.__board[to_coords[0]][to_coords[1]] = self.__board[from_coords[0]][from_coords[1]]
                self.__board[from_coords[0]][from_coords[1]] = None

    def board(self):
        for row in self.__board:
            print(row)


class Piece(object):
    # A generalised piece object, chess pieces will inherit from this class
    # and override its procedures

    def __init__(self, piece, colour):
        self._piece = piece  # Pieces are named for AN/FEN
        self._colour = colour  # Pieces are given colours for each player
        self._legal_moves = []

    def get_legal_moves(self, from_coords, board):
        # A method to check for all of the possible moves for a given piece,
        # given its current co-ordinates and the current position of the board.
        pass

    def check_legal_move(self, from_coords, board, to_coords):
        self.get_legal_moves(from_coords, board)
        print(self._legal_moves)
        if to_coords in self._legal_moves:
            return True
        else:
            return False

    @property
    def colour(self):
        return self._colour

    @property
    def legal_moves(self):
        return self._legal_moves

    def __repr__ (self):
        return str(self._colour + "General Piece")

    
class King(Piece):   # King piece class
    def __init__(self, colour):
        super().__init__("K", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "K  ")
        
class Queen(Piece):    # Queen piece class
    def __init__(self, colour):
        super().__init__("Q", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "Q  ")
        
class Rook(Piece):  # Rook piece class
    def __init__(self, colour):
        super().__init__("R", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "R  ")
    
class Bishop(Piece):    # Bishop piece class
    def __init__(self, colour):
        super().__init__("B", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "B  ")
        
class Knight(Piece):    # Knight piece class
    def __init__(self, colour):
        super().__init__("N", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "N  ")
        
class Pawn(Piece):
    # Pawn piece class
    
    def __init__(self, colour):
            super().__init__("p", colour)
            
    def get_legal_moves(self, from_coords, board):

        self._legal_moves = [] # Empties the list from previous moves
        
        if self._colour == "w":
            
            if board[from_coords[0]-1][from_coords[1]] is None:
                self._legal_moves.append([from_coords[0]-1, from_coords[1]])
                if from_coords[0] == 6 and board[4][from_coords[1]] is None:
                    self._legal_moves.append([4, from_coords[1]])
                    
            # Check such that all but the left-most pawn can legally make his move
            if from_coords[1] != 0:
                # Check if the diagonal-right square is occupied
                if board[from_coords[0]-1][from_coords[1]-1] is not None:
                    # Check if the colour of the piece is white
                    if board[from_coords[0]-1][from_coords[1]-1].colour == "w":
                        # If so, add the capture into legal moves
                        self._legal_moves.append([[from_coords[0]-1], from_coords[1]-1])

            # Check such that all but the right-most pawn can legally make this move
            if from_coords[1] != 7:
                # Check if the diagonal-right square is occupied        
                if board[from_coords[0]-1][from_coords[1]-1] is not None:
                    # Check if the colour of the piece is white
                    if board[from_coords[0]-1][from_coords[1]-1].colour == "w":
                        # If so, add the capture into legal moves
                        self._legal_moves.append([from_coords[0]-1, from_coords[1]-1])

        
        if self._colour == "b":

            # Check if the square directly below is empty
            if board[from_coords[0]+1][from_coords[1]] is None:
                # If so, add the move to the pawn's legal moves
                self._legal_moves.append([from_coords[0]+1, from_coords[1]])

                # Then check if the pawn is on its starting rank 
                # and the square two spaces below is empty
                if from_coords[0] == 1 and board[3][from_coords[1]] is None:
                    # If so, add the option of moving two squares to legal moves
                    self._legal_moves.append([3, from_coords[1]])
                    
            # Check such that all but the left-most pawn can legally make his move
            if from_coords[1] != 0:
                # Check if the diagonal-right square is occupied
                if board[from_coords[0]+1][from_coords[1]-1] is not None:
                    # Check if the colour of the piece is white
                    if board[from_coords[0]+1][from_coords[1]-1].colour == "w":
                        # If so, add the capture into legal moves
                        self._legal_moves.append([from_coords[0]+1, from_coords[1]-1])

            # Check such that all but the right-most pawn can legally make this move
            if from_coords[1] != 7:
                # Check if the diagonal-right square is occupied        
                if board[from_coords[0]+1][from_coords[1]+1] is not None:
                    # Check if the colour of the piece is white
                    if board[from_coords[0]+1][from_coords[1]+1].colour == "w":
                        # If so, add the capture into legal moves
                        self._legal_moves.append([from_coords[0]+1, from_coords[1]+1])

    
    def __repr__(self):
        return str(self._colour + "p  ")

def a():
    global board
    board = Board()
def b():
    board.board()
