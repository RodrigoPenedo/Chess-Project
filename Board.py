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
meme = PhotoImage(file="Pieces/meme.gif")

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


def mouse(event):
    grid_info = event.widget.grid_info()
    x = grid_info["row"]
    y = grid_info["column"]
    print(y,x)

    btn = Buttons[y][x]
    btn.configure(image = Empty)
    
    print("hello")


def secondmouse (event):
    global selected, square_selected
    
    grid_info = event.widget.grid_info()
    z = grid_info["column"]
    w = grid_info["row"]
    coords = z,w
    
    if selected == False:
        btn = Buttons[z][w]
        btn.configure(bg = "orange")
        selected = True
        square_selected = z,w

        
    elif selected == True and (square_selected == coords):
        btn = Buttons[z][w]
        colour = Colours[z][w]
        if colour == "white":
            btn.configure(bg = "white")
            
        if colour == "black":
            btn.configure(bg = "black")
        selected = False
        square_selected = ""


    print(w,z)

def movement(event,y,x,w,z):
    board.move([y,x],[w,z])
    grid_info = event.widget.grid_info()
    btn = Buttons[y][x]
    btn.configure(image = Empty)
    btn = Buttons[y][x]
    btn.configure(image = str(board.board[y][x]).replace("  ",""))

root.bind("<Button-1>", mouse)
root.bind("<Button-3>", secondmouse)

root.mainloop()
