import time

class Board(object):
    # The chess board is represented as a 8x8 2D array
    def __init__(self):
        # Create the board and put the pieces in their initial positions
        self.__board = [[None] * 8 for i in range(8)]
        for i in range(0, 8):
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
            if piece.check_legal_move(from_coords, self.__board, to_coords):  #Check if the move is legal
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
        #Check if the move is legal using the piece's move set
        self.get_legal_moves(from_coords, board)

        #If the to coordinates are present in the list
        #allow the peice to move
        #otherwise wont work
        if to_coords in self._legal_moves:
            return True
        else:
            return False
            print("Invalid Move")

    @property
    def colour(self):
        return self._colour

    @property
    def legal_moves(self):
        return self._legal_moves

    def __repr__ (self):
        return str(self._colour + "General Piece")


class King(Piece):
    # King piece class
    def __init__(self, colour):
        super().__init__("K", colour)
        
    def get_legal_moves(self, from_coords, board):
        self._legal_moves = [] # Empties the list of previous moves

        #A loop capable of checking 3 squares Horizontally
        for i in range(-1,2):
            if  0 <= from_coords[0] + i  <= 7: #Within the board
                
                #A loop capable of checking 3 squares Vertically
                for j in range(-1,2):
                    if  0 <= from_coords[1] + j  <= 7: #Within the board

                        #Check if there is a piece
                        if board[from_coords[0]+i][from_coords[1]+j] is not None:
                            
                            #Check the colour of the piece
                            if board[from_coords[0]+i][from_coords[1]+j].colour is not self._colour:
                                #If not the same colour then piece can be taken
                                self._legal_moves.append([from_coords[0]+i, from_coords[1]+j])

                        #If empty square, King can move
                        if board[from_coords[0]+i][from_coords[1]+j] is None:
                            self._legal_moves.append([from_coords[0]+i, from_coords[1]+j])

            
        #loop to check everyother piece's move set
        for row in range(0,8):
            for column in range(0,8):

                #Make the coordinates equal que ones being checked
                from_coords = [row,column]
                #Check if that coordinate is empty
                if board[row][column] is not None: 

                    #Check if there isnt a king and if there is a piece check it's the opposite colour
                    if type(board[row][column]) is not King and board[row][column].colour is not self._colour:

                        #List all the possible moves, by accessing the get_legal_moves of the piece
                        #at the given coordinates
                        board[row][column].get_legal_moves(from_coords, board)

                        #Loop for the amount of moves in the list
                        for move in board[row][column].legal_moves:
                                    
                            #Check if the move affects the king
                            if move in self.legal_moves:
                                #If so remove that move from the king's possible moves
                                #So that the king doesn't move into a Check Position
                                self.legal_moves.remove(move)



    def __repr__(self):
        return str(self._colour + "K  ")

class Queen(Piece):
    # Queen piece class
    def __init__(self, colour):
        super().__init__("Q", colour)
        
    def get_legal_moves(self, from_coords, board):
        self._legal_moves = [] # Empties the list of previous moves

        # A Loop to check if the squares are empty, and up to where can it move on the board.
        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]+i <= 7:
                #To go Down
                if board[from_coords[0]+i][from_coords[1]] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0]+i, from_coords[1]])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]+i][from_coords[1]].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]])
                    #Stop after finding any piece
                    break

        for i in range(1,8):
            #Make sure it stays within range of the board
            if 0 <= from_coords[1]+i <= 7:
                #To go Up
                if board[from_coords[0]][from_coords[1]+i] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0], from_coords[1]+i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]][from_coords[1]+i].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0], from_coords[1]+i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):
            #Make sure it stays within range of the board
            if 0 <= from_coords[0]-i <= 7:
                #To go Right
                if board[from_coords[0]-i][from_coords[1]] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0]-i, from_coords[1]])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]-i][from_coords[1]].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]])
                    #Stop after finding any piece
                    break

        for i in range(1,8):
            #Make sure it stays within range of the board
            if 0 <= from_coords[1]-i <= 7:
                #To go Left
                if board[from_coords[0]][from_coords[1]-i] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0], from_coords[1]-i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]][from_coords[1]-i].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0], from_coords[1]-i])
                    #Stop after finding any piece
                    break

        # A Loop to check if the squares are empty, and up to where can it move on the board.
        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]+i <= 7 and 0 <= from_coords[1]+i <= 7:
                #To go Right-Down
                if board[from_coords[0]+i][from_coords[1]+i] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0]+i, from_coords[1]+i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]+i][from_coords[1]+i].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]+i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]-i <= 7 and 0 <= from_coords[1]+i <= 7:
                #To go Right-Up
                if board[from_coords[0]-i][from_coords[1]+i] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0]-i, from_coords[1]+i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]-i][from_coords[1]+i].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]+i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]-i <= 7 and 0 <= from_coords[1]-i <= 7:
                #To go Left-Up
                if board[from_coords[0]-i][from_coords[1]-i] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0]-i, from_coords[1]-i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]-i][from_coords[1]-i].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]-i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]+i <= 7 and 0 <= from_coords[1]-i <= 7:
                #To go Left-Down
                if board[from_coords[0]+i][from_coords[1]-i] is None:
                    # If so, add the move to the Queen's legal moves
                    self._legal_moves.append([from_coords[0]+i, from_coords[1]-i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]+i][from_coords[1]-i].colour is not self._colour:
                        # If so, add the move to the Queen's legal moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]-i])
                    #Stop after finding any piece
                    break


    def __repr__(self):
        return str(self._colour + "Q  ")

class Rook(Piece):
    # Rook piece class
    def __init__(self, colour):
        super().__init__("R", colour)

    def get_legal_moves(self, from_coords, board):

        self._legal_moves = [] # Empties the list of previous moves

        # A Loop to check if the squares are empty, and up to where can it move on the board.
        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]+i <= 7:
                #To go Down
                if board[from_coords[0]+i][from_coords[1]] is None:
                    # If so, add the move to the Rook's legal moves
                    self._legal_moves.append([from_coords[0]+i, from_coords[1]])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]+i][from_coords[1]].colour is not self._colour:
                        # If so, add the move to the Rook's legal moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]])
                    #Stop after finding any piece
                    break

        for i in range(1,8):
            #Make sure it stays within range of the board
            if 0 <= from_coords[1]+i <= 7:
                #To go Up
                if board[from_coords[0]][from_coords[1]+i] is None:
                    # If so, add the move to the Rook's legal moves
                    self._legal_moves.append([from_coords[0], from_coords[1]+i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]][from_coords[1]+i].colour is not self._colour:
                        # If so, add the move to the Rook's legal moves
                        self._legal_moves.append([from_coords[0], from_coords[1]+i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):
            #Make sure it stays within range of the board
            if 0 <= from_coords[0]-i <= 7:
                #To go Right
                if board[from_coords[0]-i][from_coords[1]] is None:
                    # If so, add the move to the Rook's legal moves
                    self._legal_moves.append([from_coords[0]-i, from_coords[1]])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]-i][from_coords[1]].colour is not self._colour:
                        # If so, add the move to the Rook's legal moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]])
                    #Stop after finding any piece
                    break

        for i in range(1,8):
            #Make sure it stays within range of the board
            if 0 <= from_coords[1]-i <= 7:
                #To go Left
                if board[from_coords[0]][from_coords[1]-i] is None:
                    # If so, add the move to the Rook's legal moves
                    self._legal_moves.append([from_coords[0], from_coords[1]-i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]][from_coords[1]-i].colour is not self._colour:
                        # If so, add the move to the Rook's legal moves
                        self._legal_moves.append([from_coords[0], from_coords[1]-i])
                    #Stop after finding any piece
                    break

        
    def __repr__(self):
        return str(self._colour + "R  ")

class Bishop(Piece):
    # Bishop piece class
    def __init__(self, colour):
        super().__init__("B", colour)

    def get_legal_moves(self, from_coords, board):

        self._legal_moves = [] # Empties the list of previous moves

        # A Loop to check if the squares are empty, and up to where can it move on the board.
        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]+i <= 7 and 0 <= from_coords[1]+i <= 7:
                #To go Right-Down
                if board[from_coords[0]+i][from_coords[1]+i] is None:
                    # If so, add the move to the Bishop's legal moves
                    self._legal_moves.append([from_coords[0]+i, from_coords[1]+i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]+i][from_coords[1]+i].colour is not self._colour:
                        # If so, add the move to the Bishop's legal moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]+i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]-i <= 7 and 0 <= from_coords[1]+i <= 7:
                #To go Right-Up
                if board[from_coords[0]-i][from_coords[1]+i] is None:
                    # If so, add the move to the Bishop's legal moves
                    self._legal_moves.append([from_coords[0]-i, from_coords[1]+i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]-i][from_coords[1]+i].colour is not self._colour:
                        # If so, add the move to the Bishop's legal moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]+i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]-i <= 7 and 0 <= from_coords[1]-i <= 7:
                #To go Left-Up
                if board[from_coords[0]-i][from_coords[1]-i] is None:
                    # If so, add the move to the Bishop's legal moves
                    self._legal_moves.append([from_coords[0]-i, from_coords[1]-i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]-i][from_coords[1]-i].colour is not self._colour:
                        # If so, add the move to the Bishop's legal moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]-i])
                    #Stop after finding any piece
                    break

        for i in range(1,8):

            #Make sure it stays within range of the board
            if 0 <= from_coords[0]+i <= 7 and 0 <= from_coords[1]-i <= 7:
                #To go Left-Down
                if board[from_coords[0]+i][from_coords[1]-i] is None:
                    # If so, add the move to the Bishop's legal moves
                    self._legal_moves.append([from_coords[0]+i, from_coords[1]-i])

                #To when there is a piece
                else:
                    #Check if the color of the piece is not the same, so it can be taken
                    if board[from_coords[0]+i][from_coords[1]-i].colour is not self._colour:
                        # If so, add the move to the Bishop's legal moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]-i])
                    #Stop after finding any piece
                    break
                

    def __repr__(self):
        return str(self._colour + "B  ")

class Knight(Piece):
    # Knight piece class
    def __init__(self, colour):
        super().__init__("N", colour)

    def get_legal_moves(self, from_coords, board):
        
        self._legal_moves = [] # Empties the list of previous moves

        #Loop to calculate every square the Knight can move to (jumping over pieces)
        for i in range(1,3):
            for j in range(1,3):

                #Limit the knight to only doing L shaped moves
                if i == 1 and j == 1 or i == 2 and j == 2:
                    break


                #Check two squares downwards vertically to the right, while within range
                if 0 <= from_coords[0]+i <= 7 and 0 <= from_coords[1]+j <= 7:
                    #Check if empty
                    if board[from_coords[0]+i][from_coords[1]+j] is None:
                        #If so add new move to it's possible moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]+j])
                    else:
                        #When not empty check for the colour of the piece
                        if board[from_coords[0]+i][from_coords[1]+j].colour is not self._colour:
                            #If so add new move to it's possible moves
                            self._legal_moves.append([from_coords[0]+i, from_coords[1]+j])

                #Check two squares downwards vertically to the left, while within range
                if 0 <= from_coords[0]-i <= 7 and 0 <= from_coords[1]+j <= 7:
                    #Check if empty
                    if board[from_coords[0]-i][from_coords[1]+j] is None:
                        #If so add new move to it's possible moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]+j])
                    else:
                        #When not empty check for the colour of the piece
                        if board[from_coords[0]-i][from_coords[1]+j].colour is not self._colour:
                            #If so add new move to it's possible moves
                            self._legal_moves.append([from_coords[0]-i, from_coords[1]+j])

                #Check two squares upwards vertically to the left, while within range
                if 0 <= from_coords[0]+i <= 7 and 0 <= from_coords[1]-j <= 7:
                    #Check if empty
                    if board[from_coords[0]+i][from_coords[1]-j] is None:
                        #If so add new move to it's possible moves
                        self._legal_moves.append([from_coords[0]+i, from_coords[1]-j])
                        
                    else:
                        #When not empty check for the colour of the piece
                        if board[from_coords[0]+i][from_coords[1]-j].colour is not self._colour:
                            #If so add new move to it's possible moves
                            self._legal_moves.append([from_coords[0]+i, from_coords[1]-j])

                #Check two squares upwards vertically to the right, while within range
                if 0 <= from_coords[0]-i <= 7 and 0 <= from_coords[1]-j <= 7:
                    #Check if empty
                    if board[from_coords[0]-i][from_coords[1]-j] is None:
                        #If so add new move to it's possible moves
                        self._legal_moves.append([from_coords[0]-i, from_coords[1]-j])
                    else:
                        #When not empty check for the colour of the piece
                        if board[from_coords[0]-i][from_coords[1]-j].colour is not self._colour:
                            #If so add new move to it's possible moves
                            self._legal_moves.append([from_coords[0]-i, from_coords[1]-j])


    def __repr__(self):
        return str(self._colour + "N  ")

class Pawn(Piece):
    # Pawn piece class

    def __init__(self, colour):
            super().__init__("p", colour)

    def get_legal_moves(self, from_coords, board):

        self._legal_moves = [] # Empties the list of previous moves

        # When the Pawn is White
        if self._colour == "w":

            # Check if the square directly below is empty
            if board[from_coords[0]-1][from_coords[1]] is None:
                # If so, add the move to the pawn's legal moves
                self._legal_moves.append([from_coords[0]-1, from_coords[1]])

                # Then check if the pawn is on its starting rank
                # and the square two spaces below is empty
                if from_coords[0] == 6 and board[4][from_coords[1]] is None:
                    # If so, add the option of moving two squares to legal moves
                    self._legal_moves.append([4, from_coords[1]])

            # Check such that all but the left-most pawn can legally make his move
            if from_coords[1] != 0:
                # Check if the diagonal-right square is occupied
                if board[from_coords[0]-1][from_coords[1]-1] is not None:
                    # Check if the colour of the piece is black
                    if board[from_coords[0]-1][from_coords[1]-1].colour == "b":
                        # If so, add the capture into legal moves
                        self._legal_moves.append([[from_coords[0]-1], from_coords[1]-1])

            # Check such that all but the right-most pawn can legally make this move
            if from_coords[1] != 7:
                # Check if the diagonal-right square is occupied
                if board[from_coords[0]-1][from_coords[1]-1] is not None:
                    # Check if the colour of the piece is black
                    if board[from_coords[0]-1][from_coords[1]-1].colour == "b":
                        # If so, add the capture into legal moves
                        self._legal_moves.append([from_coords[0]-1, from_coords[1]-1])


        # When the Pawn is Black
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


print("version 2.1 - King update")

#delete me, just for debugging
def a():
    global start
    start = time.time()
    global board
    board = Board()
def b():
    board.board()

def m():
    z = int(input())
    x = int(input())
    c = int(input())
    v = int(input())
    board.move([z,x],[c,v])
    
def timetaken():
    end = time.time()
    print(end - start)
#delete me
