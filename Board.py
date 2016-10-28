from tkinter import *
from tkinter import ttk
from ChessProject import Board, Piece, Pawn, Rook, Knight, King, Queen, Bishop

global selected, square_selected

selected = False
square_selected = ""

board = Board()

root = Tk()
frame=Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)

grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1,minsize=60)
Grid.columnconfigure(frame, 0, weight=1,minsize=60)

Buttons = []
Colours = []

#Import images for pieces
# where
# colour + PIECE + .gif = file name

#black pieces
bB = PhotoImage(file="Pieces/bB.gif")
bK = PhotoImage(file="Pieces/bK.gif")
bN = PhotoImage(file="Pieces/bN.gif")
bp = PhotoImage(file="Pieces/bP.gif")
bQ = PhotoImage(file="Pieces/bQ.gif")
bR = PhotoImage(file="Pieces/bR.gif")

#white pieces
wB = PhotoImage(file="Pieces/wB.gif")
wK = PhotoImage(file="Pieces/wK.gif")
wN = PhotoImage(file="Pieces/wN.gif")
wp = PhotoImage(file="Pieces/wP.gif")
wQ = PhotoImage(file="Pieces/wQ.gif")
wR = PhotoImage(file="Pieces/wR.gif")

Empty = PhotoImage(file="Pieces/Empty.gif")

for x in range(0,8):
    a = True
    if x % 2:
        a = False
    Buttons.append([])
    Colours.append([])
    for y in range(0,8):
        if a:
            btn = Button(frame,bg = "black",image = Empty)
            Colours[x].append("black")
            a = False
            
        else:
            btn = Button(frame,bg = "white",image = Empty)
            Colours[x].append("white")
            a = True
        
        if board.board[y][x] is not None:
            
            if str(board.board[y][x]).replace("  ","") == "bB":
                btn.configure(image = bB)
            if str(board.board[y][x]).replace("  ","") == "bK":
                btn.configure(image = bK)
            if str(board.board[y][x]).replace("  ","") == "bN":
                btn.configure(image = bN)
            if str(board.board[y][x]).replace("  ","") == "bp":
                btn.configure(image = bp)
            if str(board.board[y][x]).replace("  ","") == "bQ":
                btn.configure(image = bQ)
            if str(board.board[y][x]).replace("  ","") == "bR":
                btn.configure(image = bR)
                
            if str(board.board[y][x]).replace("  ","") == "wB":
                btn.configure(image = wB)
            if str(board.board[y][x]).replace("  ","") == "wK":
                btn.configure(image = wK)
            if str(board.board[y][x]).replace("  ","") == "wN":
                btn.configure(image = wN)
            if str(board.board[y][x]).replace("  ","") == "wp":
                btn.configure(image = wp)
            if str(board.board[y][x]).replace("  ","") == "wQ":
                btn.configure(image = wQ)
            if str(board.board[y][x]).replace("  ","") == "wR":
                btn.configure(image = wR)

            
        btn.grid(column=x, row=y, sticky=N+S+E+W)
        Buttons[x].append(btn)
    

for x in range(0,8):
  Grid.columnconfigure(frame, x, weight=1, minsize=60)

for y in range(0,8):
  Grid.rowconfigure(frame, y, weight=1, minsize=60)


def click (event):
    global selected, square_selected, piece_selected
    
    grid_info = event.widget.grid_info()
    z = grid_info["column"]
    w = grid_info["row"]
    coords = z,w

    if selected == True and (square_selected == coords):
        btn = Buttons[z][w]
        colour = Colours[z][w]
        if colour == "white":
            btn.configure(bg = "white")
            
        if colour == "black":
            btn.configure(bg = "black")
        selected = False
        square_selected = ""
        piece_selected = ""
    
    elif selected == False:
        if board.board[w][z] is not None:
            btn = Buttons[z][w]
            btn.configure(bg = "orange")
            selected = True
            square_selected = z,w
            piece_selected = board.board[w][z]


    elif selected == True:
        board.move([square_selected[1],square_selected[0]],[coords[1],coords[0]])
        btn = Buttons[coords[0]][coords[1]]

        if piece_selected == board.board[coords[1]][coords[0]]:
            
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "bB":
                btn.configure(image = bB)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "bK":
                btn.configure(image = bK)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "bN":
                btn.configure(image = bN)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "bp":
                btn.configure(image = bp)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "bQ":
                btn.configure(image = bQ)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "bR":
                btn.configure(image = bR)
                
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "wB":
                btn.configure(image = wB)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "wK":
                btn.configure(image = wK)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "wN":
                btn.configure(image = wN)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "wp":
                btn.configure(image = wp)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "wQ":
                btn.configure(image = wQ)
            if str(board.board[coords[1]][coords[0]]).replace("  ","") == "wR":
                btn.configure(image = wR)

            btn = Buttons[square_selected[0]][square_selected[1]]
            colour = Colours[square_selected[0]][square_selected[1]]

            if colour == "white":
                btn.configure(bg = "white")
                
            elif colour == "black":
                btn.configure(bg = "black")
                
            btn.configure(image = Empty)
            selected = False
            square_selected = ""


    if selected == True:
        from_coords = [square_selected[1],square_selected[0]]
        possiblemoves = board.legalmoves(from_coords,board)
        print(possiblemoves)
        
        for i in range(0,len(possiblemoves)):
            moves = possiblemoves[i]
            btn = Buttons[moves[1]][moves[0]]
            btn.configure(bg = "orange")
            

    elif selected == False:
        for i in range(0,8):
            for j in range(0,8):
                btn = Buttons[i][j]
                colour = Colours[i][j]

                if colour == "white":
                    btn.configure(bg = "white")
                    
                if colour == "black":
                    btn.configure(bg = "black")
                    
                    
    
    print(w,z)


    

root.bind("<Button-1>", click)
root.bind("<Button-3>")

root.mainloop()
