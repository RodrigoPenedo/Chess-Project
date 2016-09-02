

class Board(object):
    # The chess board is represented as a 8x8 2D array
    def __init__(self):
        # Create the board and move pieces to their initial positions
        self.__board = [[""] * 8 for i in range(8)]
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
            print(self.__board)

class Piece(object):
    # A generalised piece object, chess pieces will inherit from this class
    # and override its procedures
    def __init__(self, piece, colour):
        self._piece = piece  # Pieces are named for AN/FEN
        self._colour = colour  # Pieces are given colours for each player
        
class King(Piece):   # King piece class
    def __init__(self, colour):
        super().__init__("K", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "K")
        
class Queen(Piece):    # Queen piece class
    def __init__(self, colour):
        super().__init__("Q", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "Q")
        
class Rook(Piece):  # Rook piece class
    def __init__(self, colour):
        super().__init__("R", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "R")
    
class Bishop(Piece):    # Bishop piece class
    def __init__(self, colour):
        super().__init__("B", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "B")
        
class Knight(Piece):    # Knight piece class
    def __init__(self, colour):
        super().__init__("N", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "N")
        
class Pawn(Piece):
    # Pawn piece class 
    def __init__(self, colour):
            super().__init__("p", colour)
    def move(self):
        pass
    def __repr__(self):
        return str(self._colour + "p")
    
board = Board()
