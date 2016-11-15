import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox, colorchooser

from ChessProject import Board, Piece, Pawn, Rook, Knight, King, Queen, Bishop

class Stack():
    def __init__(self):
        self.items = []

    def Empty(self):
        if self.items == []:
            return True
        else:
            return False

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

def write(msg):
    numlines = log.index('end - 1 line').split('.')[0]
    log['state'] = 'normal'
    if numlines==24:
        log.delete(1.0, 2.0)
    if log.index('end-1c')!='1.0':
        log.insert('end', '\n')
        log.see(END)
    log.insert('end', msg)
    log['state'] = 'disabled'


global colour_selected, colour_possible_moves
colour_selected = "orange"
colour_possible_moves = "orange"

LARGE_FONT = ("Verdana", 40)

class ChessApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default = "chessgame.ico")
        tk.Tk.wm_title(self, "Chess")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        global selected, piece_selected, square_selected
        selected = False
        square_selected = ""
        piece_selected = ""


        global game_played
        game_played = False

        # create a pulldown menu, and add it to the menu bar
        menubar = tk.Menu(container)
        Game_menu = tk.Menu(menubar, tearoff=0)
        Game_menu.add_command(label = "Save", command = lambda: SaveGame(game_played))
        Game_menu.add_command(label = "Undo Move", command = lambda: UndoMove(self))
        Game_menu.add_separator()
        Game_menu.add_command(label = "Menu", command = lambda: SaveFirst(self))
        Game_menu.add_command(label = "Exit", command = lambda: Quit(game_played))
        menubar.add_cascade(label="Game", menu=Game_menu)

        Settings_menu = tk.Menu(menubar, tearoff=0)
        Settings_menu.add_command(label="Change Selected Piece Colour", command = ColourPicker_Piece)
        Settings_menu.add_command(label="Change Possible Moves Colour", command = ColourPicker_Moves)
        Settings_menu.add_command(label="Change Both Colours", command = Colour_Picker_Both)
        menubar.add_cascade(label="Settings", menu=Settings_menu)

        Help_menu = tk.Menu(menubar, tearoff=0)
        Help_menu.add_command(label="Information", command= lambda: Info(self))
        menubar.add_cascade(label="Help", menu=Help_menu)


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


def ColourPicker_Piece():
    global colour_selected
    colour_selected = colorchooser.askcolor(initialcolor="#ff0000")

    if colour_selected == "#ffffff" or colour_selected == "#ffffff":
        while colour_selected == "#ffffff" or colour_selected == "#ffffff":
            colour_selected = colorchooser.askcolor(initialcolor="#ff0000")

    colour_selected = colour_selected[1]

def ColourPicker_Moves():
    global colour_possible_moves
    colour_possible_moves = colorchooser.askcolor(initialcolor="#ff0000")

    if colour_possible_moves == "#ffffff" or colour_selected == "#ffffff":
        while colour_possible_moves == "#ffffff" or colour_selected == "#ffffff":
            colour_possible_moves = colorchooser.askcolor(initialcolor="#ff0000")

    colour_possible_moves = colour_possible_moves[1]

def Colour_Picker_Both():
    global both, colour_possible_moves, colour_selected
    both = colorchooser.askcolor(initialcolor="#ff0000")

    if both == "#ffffff" or both == "#ffffff":
        while both == "#ffffff" or both == "#ffffff":
            both = colorchooser.askcolor(initialcolor="#ff0000")

    colour_selected = both[1]
    colour_possible_moves = both[1]

def Info(parent):
    print("Soon")

def UndoMove(event):
    try:
        coordinates = stack.pop()
        to_coords = coordinates[0], coordinates[1]
        from_coords = coordinates[2], coordinates[3]
        piece_selected = coordinates[4]
        coords = to_coords[1], to_coords[0]
        square_selected = from_coords[1], from_coords[0]
        # print(to_coords, from_coords)

        board.UndoMove(to_coords, from_coords)
        UpdateBoardPieces(piece_selected, coords, square_selected, True)

    except IndexError:
        messagebox.showinfo(title="Failed", message="No more moves to Undo.")


class StartMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Chess", font =("Verdana", 40))
        label.pack(padx = 10, pady = 10)

        chessimage = PhotoImage(file="chess-square.gif")
        img = Label(self, image=chessimage)
        img.image = chessimage
        img.pack()

        button1 = ttk.Button(self, text = "New Game", command = lambda: controller.show_frame(NewGame))
        button1.pack(ipady=10,ipadx=10)

        button2 = ttk.Button(self, text="Load", command = lambda: controller.show_frame(Load))
        button2.pack(ipady=10,ipadx=10)

        button3 = ttk.Button(self, text="Tutorial", command = lambda: controller.show_frame(Tutorial))
        button3.pack(ipady=10,ipadx=10)

        button4 = ttk.Button(self, text="Quit", command = lambda: Quit(game_played))
        button4.pack(ipady=10,ipadx=10)

        game_played = False

        loadimages()


class NewGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        grid = Frame(self)
        grid.grid(sticky=N + S + E + W, column=0, row=7, columnspan=2)
        Grid.rowconfigure(self, 7, weight=1, minsize=70)
        Grid.columnconfigure(self, 0, weight=1, minsize=70)

        global board, stack, log
        board = Board()
        stack = Stack()

        global game_played
        game_played = True

        global selected, square_selected, piece_selected
        selected = False
        square_selected = ""
        piece_selected = ""

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
            Grid.columnconfigure(self, x, weight=1, minsize=70)

        for y in range(0, 8):
            Grid.rowconfigure(self, y, weight=1, minsize=70)

        text = ttk.Label(self, text="Who's Turn", font=20)
        text.grid(column=9, row=0,columnspan=2)

        text = ttk.Label(self, text="")
        text.grid(column=8, row=0,columnspan=8, sticky=(N,S))

        log = Text(self, state='disabled',height=28, width=60, wrap="none")
        log.grid(column=9, row=1, rowspan=6,sticky=(N,S,E,W))

        s = ttk.Scrollbar(self, orient=VERTICAL, command=log.yview)
        s.grid(column=15, row=1, sticky=(N, S),rowspan=6)
        log['yscrollcommand'] = s.set


class Load(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text = "Load", font ="LARGE_FONT")
        label.pack(padx = 10, pady = 10)

        global game_played
        game_played = True

        button1 = ttk.Button(self, text = "Menu", command = lambda: controller.show_frame(StartMenu))
        button1.pack()


class Tutorial(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)


###Work needs to be done here###
def SaveGame(game_played):
    if game_played == True:
        board.Save(board)
        messagebox.showinfo(title="Saved", message="Board State Successfully Saved.")

    else:
        messagebox.showinfo(title="Save Failed", message="Board is in the Initial Position.")
###Work needs to be done here###

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
    global selected, square_selected, piece_selected, Playing

    try:
        grid_info = event.widget.grid_info()

        z = grid_info["column"]
        w = grid_info["row"]
        coords = z,w

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
            btn.configure(bg=colour_selected)
            selected = True
            square_selected = z, w
            piece_selected = board.board[w][z]


    elif selected == True and Playing == True:
        if piece_selected != "":
            try:
                selected = Movement(square_selected,coords,piece_selected)
                if selected == False:
                    square_selected = ""
                    piece_selected = ""

            except AttributeError:
                selected = True

    if selected == True and Playing == True:
        from_coords = [square_selected[1], square_selected[0]]
        possiblemoves = board.legalmoves(from_coords, board)
        #print(possiblemoves)

        for i in range(0, len(possiblemoves)):
            moves = possiblemoves[i]
            btn = Buttons[moves[1]][moves[0]]
            btn.configure(bg=colour_possible_moves)


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


def Movement(square_selected,coords,piece_selected):
    board.move([square_selected[1], square_selected[0]], [coords[1], coords[0]])
    selected = UpdateBoardPieces(piece_selected, coords, square_selected, False)

    return selected


def UpdateBoardPieces(piece_selected, coords, square_selected, Undo):

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


    if Undo == False and piece_selected == board.board[coords[1]][coords[0]]:
        item = [square_selected[1], square_selected[0]] + [coords[1], coords[0]] + [piece_selected]
        print(item)
        stack.push(item)

        data = str(['Moved'] + [piece_selected] + [' from ('] +
                   [square_selected[1]] + [square_selected[0]] + [') to ('] +
                   [coords[1]] + [coords[0]] + [')'])
        write(data)

    try:
        return selected
    except UnboundLocalError:
        selected = True
        return selected


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
