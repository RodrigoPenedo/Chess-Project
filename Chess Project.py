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
        move_piece()
        

def move_piece():
    accepted1 = ["a","b","c","d","e","f","g","h"]
    accepted2 = ["1","2","3","4","5","6","7","8"]

    move_from = " "
    move_to = " "
    
    while (move_from[0] not in accepted1) or (move_from[1] not in accepted2):
        move_from = str(input("Please enter the piece you wish to move: "))
        
        if len(move_from) == 2: #length must be 2, otherwise code breaks
            if move_from[0] in accepted1 or move_from[1] in accepted2: #check for format
                print("") #Accepted
            else:
                print("Invalid")
        else:
            print("Invalid")


    while move_to[0] not in accepted1 or move_to[1] not in accepted2:
        move_to = str(input("please enter the desired destination of the piece: "))

        if len(move_to) == 2: #length must be 2, otherwise code breaks
            if move_to[0] in accepted1 or move_to[1] in accepted2: #check for format
                print("") #Accepted
            else:
                print("Invalid")
        else:
            print("Invalid")
            
    print("Moving from",move_from,"to",move_to)

    movefrom = str(accepted1.index(move_from[0])) + str(int(move_from[1])-1)
    moveto = str(accepted1.index(move_to[0])) + str(int(move_to[1])-1)
    print("Moving from",movefrom,"to",moveto)

    row = board[movefrom[0]]
    print(row[movefrom[1]])

    
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

