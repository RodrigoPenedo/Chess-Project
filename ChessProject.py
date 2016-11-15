import time

class Board(object):
    # The chess board is represented as a 8x8 2D array
    def __init__(self):
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

        self.piecetaken = ""

    def InitialPieceSetup(self):
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

        self.piecetaken = ""

    def move(self, from_coords, to_coords):
        piece = self.__board[from_coords[0]][from_coords[1]]
        if piece is not None:  # Check if piece exists
            if piece.check_legal_move(from_coords, self.__board, to_coords):  #Check if the move is legal
                if self.__board[to_coords[0]][to_coords[1]] is not None:
                    self.piecetaken = str(self.__board[to_coords[0]][to_coords[1]])
                # Move the piece and then remove it from its original position
                self.__board[to_coords[0]][to_coords[1]] = self.__board[from_coords[0]][from_coords[1]]
                self.__board[from_coords[0]][from_coords[1]] = None


    def UndoMove(self, to_coords, from_coords):
        self.__board[to_coords[0]][to_coords[1]] = self.__board[from_coords[0]][from_coords[1]]
        self.__board[from_coords[0]][from_coords[1]] = None
        

    def Save(self,board):
        save = ""
        for i in range(8):
            for j in range(8):
                save += str(self.__board[i][j])
            save += "\n"

        save = save.replace("  ","-- ")
        save = save.replace("None","---- ")

        name = "Save-File-" + str(time.strftime("%d-%b-%Y-%H-%M-%S"))
        save_file = open(name + ".txt", mode="w+", encoding="utf-8")
        save_file.write(save)

    def Load(self,board,filelocation):
        board_loaded = []
        Load_file = open(filelocation,"r", encoding="utf-8")
        Load = Load_file.read()
        Load = Load.replace("\n","")
        Load = Load.replace("----","None")
        Load = Load.replace("  ","--")
        Load = Load.replace(" ","")
        Load = Load.replace("--", "  ")
        Load = [Load[i:i + 32] for i in range(0, len(Load), 32)]

        for i in range(0,8):
            board_loaded.append([])
            board_loaded[i] = [Load[i][j:j + 4] for j in range(0, len(Load[i]), 4)]

        self.__board = board_loaded
        return board_loaded
        
    def Turns(self):
        for x in range(0,8):
            for y in range(0,8):
                piece = (str(self.__board[x][y])).replace(" ","")
                if piece == "wK" or piece == "bK":
                    if (str(self.__board[x][y])).replace(" ","") == "wK":
                        whiteKing = self.__board[x][y]
                        WK_location = x,y
                        
                    if (str(self.__board[x][y])).replace(" ","") == "bK":
                        blackKing = self.__board[x][y]
                        BK_location = x,y

        self.turn = "W"
        self.turn_count = 1

        WK_Check = False
        for row in range(0,8):
            for column in range(0,8):
                from_coords = [row,column]
                piece = self.__board[row][column]
                if piece is not None: 
                    if type(piece) is not King and piece.colour is not "w":
                        piece.get_legal_moves(from_coords, self.__board)
                        for move in piece.legal_moves:
                            if move == WK_location:
                                WK_Check = True

        BK_Check = False
        for row in range(0,8):
            for column in range(0,8):
                from_coords = [row,column]
                piece = self.__board[row][column]
                if piece is not None: 
                    if type(piece) is not King and piece.colour is not "b":
                        piece.get_legal_moves(from_coords, self.__board)
                        for move in piece.legal_moves:
                            if move == BK_location:
                                BK_Check = True


        whiteKing = self.__board[WK_location[0]][WK_location[1]]
        blackKing = self.__board[BK_location[0]][BK_location[1]]
        
        white_conditions = ((whiteKing.legal_moves != None) and (WK_Check != True))
        black_conditions = ((blackKing.legal_moves != None) and (BK_Check != True))

        while (white_conditions or black_conditions) == True:
            self.turn_over == False
            
            while self.turn_over != True:
                if self.turn_over == True:
                    if self.turn == "W": #White Pieces
                        print("white to black")
                        self.turn = "B"

                    if self.turn == "B": #Black Pieces
                        print("black to white")
                        self.turn = "W"

                print(self.turn_count)
                self.turn_count += 1

                for x in range(8):    #Update the King's location
                    for y in range(8):
                        if self.__board[x][y] is King:
                            if self.__board[x][y].colour == "w":
                                self.whiteKing = self.__board[x][y]
                            if self.__board[x][y].colour == "b":
                                self.blackKing = self.__board[x][y]

        if white_conditions == False:
            print("Black Wins")
        if black_conditions == False:
            print("White Wins")
                                
    
    def legalmoves(self,from_coords,board):
        #print(from_coords)
        piece = self.__board[from_coords[0]][from_coords[1]]
        return piece.get_legal_moves(from_coords,self.__board)

    
    
    def turn_over():
        self.turn_over = True
    
    def boardshow(self):
        for row in self.__board:
            print(row)

    def taken(self):
        return self.piecetaken
    
    def turn(self):
        return self.turn
    
    def turn_count(self):
        return self.turn_count
    
    def turn_reset(self):
        self.turn_count = 0
        self.turn = ""

    @property
    def board(self):
        return self.__board



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

        return self._legal_moves

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
                
        return self._legal_moves

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
                
        return self._legal_moves
        
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
                
        return self._legal_moves

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
                if i != j:
                        
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
                else:
                    pass
                
        return self._legal_moves
    
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
                        self._legal_moves.append([from_coords[0]-1, from_coords[1]-1])

            # Check such that all but the right-most pawn can legally make this move
            if from_coords[1] != 7:
                # Check if the diagonal-right square is occupied
                if board[from_coords[0]-1][from_coords[1]+1] is not None:
                    # Check if the colour of the piece is black
                    if board[from_coords[0]-1][from_coords[1]+1].colour == "b":
                        # If so, add the capture into legal moves
                        self._legal_moves.append([from_coords[0]-1, from_coords[1]+1])


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

        return self._legal_moves
    
    def __repr__(self):
        return str(self._colour + "p  ")
