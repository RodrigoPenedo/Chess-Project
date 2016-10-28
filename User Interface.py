import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from ChessProject import Board, Piece, Pawn, Rook, Knight, King, Queen, Bishop

global game_played
game_played = False

LARGE_FONT = ("Verdana", 16)

class ChessApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default = "chessgame.ico")
        tk.Tk.wm_title(self, "Chess")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)


        # create a pulldown menu, and add it to the menu bar
        menubar = tk.Menu(container)
        Game_menu = tk.Menu(menubar, tearoff=0)
        Game_menu.add_command(label = "Save", command = SaveGame)
        Game_menu.add_command(label = "Load")
        Game_menu.add_command(label = "Undo Move")
        Game_menu.add_separator()
        Game_menu.add_command(label = "Menu", command = lambda: SaveFirst(self))
        Game_menu.add_command(label = "Exit", command = lambda: Quit(game_played))
        menubar.add_cascade(label="Game", menu=Game_menu)

        tk.Tk.config(self, menu = menubar)

        self.frames = {}

        for F in (StartMenu, NewGame, Load):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "NSEW")

        self.show_frame(StartMenu)


    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Chess", font ="LARGE_FONT")
        label.pack(padx = 10, pady = 10)

        button1 = ttk.Button(self, text = "New Game", command = lambda: controller.show_frame(NewGame))
        button1.pack()

        button2 = ttk.Button(self, text="Load", command = lambda: controller.show_frame(Load))
        button2.pack()

        button3 = ttk.Button(self, text="Tutorial", command = lambda: controller.show_frame(Tutorial))
        button3.pack()

        button4 = ttk.Button(self, text="Quit", command = lambda: Quit(game_played))
        button4.pack()

        game_played = False

        loadimages()

class NewGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        grid = Frame(self)
        grid.grid(sticky=N + S + E + W, column=0, row=7, columnspan=2)
        Grid.rowconfigure(self, 7, weight=1, minsize=60)
        Grid.columnconfigure(self, 0, weight=1, minsize=60)

        #label = ttk.Label(self, text = "New Game", font ="LARGE_FONT")
        #label.pack(padx = 10, pady = 10)

        #button1 = ttk.Button(self, text = "Menu", command = lambda: controller.show_frame(StartMenu))
        #button1.pack()

        global board
        board = Board()

        global game_played
        game_played = True

        global selected, square_selected
        selected = False
        square_selected = ""

        global Buttons, Colours
        Buttons = []
        Colours = []


        # Import images for pieces
        # where
        # colour + PIECE + .gif = file name


        for x in range(0, 8):
            Even = True
            if x % 2:
                Even = False
            Buttons.append([])
            Colours.append([])
            for y in range(0, 8):
                if Even:
                    btn = tk.Button(self, bg="black", image=Empty)
                    Colours[x].append("black")
                    Even = False

                else:
                    btn = tk.Button(self, bg="white", image=Empty)
                    Colours[x].append("white")
                    Even = True

                if board.board[y][x] is not None:
                    if str(board.board[y][x]).replace("  ", "") == "bB":
                        btn.configure(image=bB)
                    if str(board.board[y][x]).replace("  ", "") == "bK":
                        btn.configure(image=bK)
                    if str(board.board[y][x]).replace("  ", "") == "bN":
                        btn.configure(image=bN)
                    if str(board.board[y][x]).replace("  ", "") == "bp":
                        btn.configure(image=bp)
                    if str(board.board[y][x]).replace("  ", "") == "bQ":
                        btn.configure(image=bQ)
                    if str(board.board[y][x]).replace("  ", "") == "bR":
                        btn.configure(image=bR)

                    if str(board.board[y][x]).replace("  ", "") == "wB":
                        btn.configure(image=wB)
                    if str(board.board[y][x]).replace("  ", "") == "wK":
                        btn.configure(image=wK)
                    if str(board.board[y][x]).replace("  ", "") == "wN":
                        btn.configure(image=wN)
                    if str(board.board[y][x]).replace("  ", "") == "wp":
                        btn.configure(image=wp)
                    if str(board.board[y][x]).replace("  ", "") == "wQ":
                        btn.configure(image=wQ)
                    if str(board.board[y][x]).replace("  ", "") == "wR":
                        btn.configure(image=wR)

                btn.grid(column=x, row=y, sticky=N + S + E + W)
                Buttons[x].append(btn)

        for x in range(0, 8):
            Grid.columnconfigure(self, x, weight=1, minsize=60)

        for y in range(0, 8):
            Grid.rowconfigure(self, y, weight=1, minsize=60)




class Load(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text = "Load", font ="LARGE_FONT")
        label.pack(padx = 10, pady = 10)

        game_played = True

        button1 = ttk.Button(self, text = "Menu", command = lambda: controller.show_frame(StartMenu))
        button1.pack()

class Tutorial(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)



def SaveGame():
    board.Save(board)
    messagebox.showinfo(title="Saved", message="Board State Successfully Saved")

def SaveFirst(controller):
    choice = messagebox.askyesno(message="Would you like to save first?\nSaving the Board state is advised.",
                        title="Quit")
    if choice == True:
        board.Save(board)
        controller.show_frame(StartMenu)

    else:
        controller.show_frame(StartMenu)


def LoadGame():
    filelocation = filedialog.askopenfilename()
    board.Load(board,filelocation)

def Quit(game_played):
    if game_played == True:
        choice = messagebox.askyesno(message="Are you sure you want to Quit?\nSaving the Board state is advised.",
                            title="Quit")
        if choice == True:
            app.destroy()

    elif game_played == False:
        app.destroy()

    else:
        choice = messagebox.askyesno(message="Are you sure you want to Quit?\nSaving the Board state is advised.",
                            title="Quit")
        if choice == True:
            app.destroy()

def click(event):
    global selected, square_selected, piece_selected

    Playing = False

    try:
        grid_info = event.widget.grid_info()
        z = grid_info["column"]
        w = grid_info["row"]
        coords = z,w

        coords = z, w

        Playing = True

    except KeyError:
        Playing = False

    if selected == True and (square_selected == coords) and Playing == True:
        btn = Buttons[z][w]
        colour = Colours[z][w]
        if colour == "white":
            btn.configure(bg="white")

        if colour == "black":
            btn.configure(bg="black")
        selected = False
        square_selected = ""
        piece_selected = ""

    elif selected == False and Playing == True:
        if board.board[w][z] is not None:
            btn = Buttons[z][w]
            btn.configure(bg="orange")
            selected = True
            square_selected = z, w
            piece_selected = board.board[w][z]


    elif selected == True and Playing == True:
        board.move([square_selected[1], square_selected[0]], [coords[1], coords[0]])
        btn = Buttons[coords[0]][coords[1]]

        if piece_selected == board.board[coords[1]][coords[0]]:

            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "bB":
                btn.configure(image=bB)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "bK":
                btn.configure(image=bK)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "bN":
                btn.configure(image=bN)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "bp":
                btn.configure(image=bp)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "bQ":
                btn.configure(image=bQ)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "bR":
                btn.configure(image=bR)

            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "wB":
                btn.configure(image=wB)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "wK":
                btn.configure(image=wK)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "wN":
                btn.configure(image=wN)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "wp":
                btn.configure(image=wp)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "wQ":
                btn.configure(image=wQ)
            if str(board.board[coords[1]][coords[0]]).replace("  ", "") == "wR":
                btn.configure(image=wR)

            btn = Buttons[square_selected[0]][square_selected[1]]
            colour = Colours[square_selected[0]][square_selected[1]]

            if colour == "white":
                btn.configure(bg="white")

            elif colour == "black":
                btn.configure(bg="black")

            btn.configure(image=Empty)
            selected = False
            square_selected = ""

    if selected == True and Playing == True:
        from_coords = [square_selected[1], square_selected[0]]
        possiblemoves = board.legalmoves(from_coords, board)
        #print(possiblemoves)

        for i in range(0, len(possiblemoves)):
            moves = possiblemoves[i]
            btn = Buttons[moves[1]][moves[0]]
            btn.configure(bg="orange")


    elif selected == False and Playing == True:
        for i in range(0, 8):
            for j in range(0, 8):
                btn = Buttons[i][j]
                colour = Colours[i][j]

                if colour == "white":
                    btn.configure(bg="white")

                if colour == "black":
                    btn.configure(bg="black")

    #print(w, z)

def loadimages():
    global bB, bK, bN, bp, bQ, bR
    global wB, wK, wN, wp, wQ, wR, Empty

    # black pieces
    bB = PhotoImage(file="Pieces/bB.gif")
    bK = PhotoImage(file="Pieces/bK.gif")
    bN = PhotoImage(file="Pieces/bN.gif")
    bp = PhotoImage(file="Pieces/bP.gif")
    bQ = PhotoImage(file="Pieces/bQ.gif")
    bR = PhotoImage(file="Pieces/bR.gif")

    # white pieces
    wB = PhotoImage(file="Pieces/wB.gif")
    wK = PhotoImage(file="Pieces/wK.gif")
    wN = PhotoImage(file="Pieces/wN.gif")
    wp = PhotoImage(file="Pieces/wP.gif")
    wQ = PhotoImage(file="Pieces/wQ.gif")
    wR = PhotoImage(file="Pieces/wR.gif")

    Empty = PhotoImage(file="Pieces/Empty.gif")


app = ChessApp()
app.bind("<Button-1>", click)
app.mainloop()
