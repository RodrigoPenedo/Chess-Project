import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox, colorchooser

from ChessProject import Board, Piece, Pawn, Rook, Knight, King, Queen, Bishop


class Stack:
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

    def clear(self):
        self.items = []


def write(msg):
        log['state'] = 'normal'
        if log.index('end-1c')!='1.0':
            log.insert('end', '\n')
            log.see(END)
        log.insert('end', msg)
        log['state'] = 'disabled'


def clear_log():
    log['state'] = 'normal'
    log.delete('1.0', END)
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

        menubar = tk.Menu(container)
        Game_menu = tk.Menu(menubar, tearoff=0)
        Game_menu.add_command(label = "Save", command = lambda: SaveGame(game_played))
        Game_menu.add_command(label = "Undo Move", command = lambda: UndoMove(self))
        Game_menu.add_separator()
        Game_menu.add_command(label = "Restart", command = lambda: Reset_Board_State())
        Game_menu.add_separator()
        Game_menu.add_command(label = "Menu", command = lambda:  Reset_Board(self))
        Game_menu.add_command(label = "Exit", command = lambda: Quit(game_played))
        menubar.add_cascade(label="Game", menu=Game_menu)

        Settings_menu = tk.Menu(menubar, tearoff=0)
        Settings_Colour_menu = tk.Menu(menubar, tearoff=0)
        Settings_Colour_menu.add_command(label="Change Selected Piece Colour", command = ColourPicker_Piece)
        Settings_Colour_menu.add_command(label="Change Possible Moves Colour", command = ColourPicker_Moves)
        Settings_Colour_menu.add_command(label="Change Both Colours", command = Colour_Picker_Both)
        Settings_menu.add_cascade(label="Colour Settings", menu=Settings_Colour_menu)
        menubar.add_cascade(label="Settings", menu=Settings_menu)

        Help_menu = tk.Menu(menubar, tearoff=0)
        Help_menu.add_command(label="Information", command= Info)
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

def Reset_Board(controller):
    SaveFirst()
    global selected, piece_selected, game_over
    selected = False
    game_over = False
    board.turn_reset()
    piece_selected = ""
    board.InitialPieceSetup()
    PiecesImagesUpdate()
    stack.clear()
    clear_log()
    controller.show_frame(StartMenu)
    return board

def Reset_Board_State():
    SaveFirst()
    global selected, piece_selected, game_over
    selected = False
    game_over = False
    board.turn_reset()
    piece_selected = ""
    board.InitialPieceSetup()
    PiecesImagesUpdate()
    stack.clear()
    clear_log()
    return board,game_over


def ColourPicker_Piece():
    global colour_selected
    colour_selected = colorchooser.askcolor(initialcolor="#ff0000")

    if colour_selected == "#ffffff" or colour_selected == "#ffffff":
        while colour_selected == "#ffffff" or colour_selected == "#ffffff":
            colour_selected = colorchooser.askcolor(initialcolor="#ff0000")

    colour_selected = colour_selected[1]
    PiecesImagesUpdate()

def ColourPicker_Moves():
    global colour_possible_moves
    colour_possible_moves = colorchooser.askcolor(initialcolor="#ff0000")

    if colour_possible_moves == "#ffffff" or colour_selected == "#ffffff":
        while colour_possible_moves == "#ffffff" or colour_selected == "#ffffff":
            colour_possible_moves = colorchooser.askcolor(initialcolor="#ff0000")

    colour_possible_moves = colour_possible_moves[1]
    PiecesImagesUpdate()

def Colour_Picker_Both():
    global both, colour_possible_moves, colour_selected
    both = colorchooser.askcolor(initialcolor="#ff0000")

    if both == "#ffffff" or both == "#ffffff":
        while both == "#ffffff" or both == "#ffffff":
            both = colorchooser.askcolor(initialcolor="#ff0000")

    colour_selected = both[1]
    colour_possible_moves = both[1]
    PiecesImagesUpdate()

def Info():
    info = tk.Tk()
    info.wm_title("Information")
    label = ttk.Label(info, text = "Information",font=22)
    label.pack(side="top",pady=10,padx=10)

    label = ttk.Label(info, text="This program is still under development", font=12)
    label.pack(pady=10, padx=10)

    label2 = ttk.Label(info, text = "Version 0.3.4",font=12)
    label2.pack()


def UndoMove(event):
    if selected == False:
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
            board.turn_undo()
            PiecesImagesUpdate()


        except IndexError:
            messagebox.showinfo(title="Failed", message="No more moves to Undo.")

    else:
        messagebox.showinfo(title="Undo", message="Please deselect the piece to undo a move.")

class StartMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Chess", font =("Verdana", 40))
        label.pack(padx = 10, pady = 10)

        chessimage = PhotoImage(file="chess-square.gif")
        img = Label(self, image=chessimage)
        img.image = chessimage
        img.pack()

        button1 = ttk.Button(self, text = "New Game", command = lambda: NewGame_Costumize(controller))
        button1.pack(ipady=10,ipadx=10)

        button2 = ttk.Button(self, text="Load", command = lambda: controller.show_frame(Load))
        button2.pack(ipady=10,ipadx=10)

        button3 = ttk.Button(self, text="Tutorial", command = lambda: controller.show_frame(Tutorial))
        button3.pack(ipady=10,ipadx=10)

        button4 = ttk.Button(self, text="Quit", command = lambda: Quit(game_played))
        button4.pack(ipady=10,ipadx=10)

        game_played = False

        loadimages()

def NewGame_Costumize(controller):
    window = tk.Tk()
    window.wm_title("New Game")

    label = ttk.Label(window, text="Game Options",font=12)
    label.grid(column=2, row=0,ipady=10,ipadx=10)

    # FEATURES NEED TO BE ADDED FIRST#
    testing = """
    label2 = ttk.Label(window, text="Timer",font=12)
    label2.grid(column=4, row=1,ipady=10,ipadx=10)

    time = StringVar()
    ttk.Radiobutton(window, text='0', variable=time, value='False').grid(column=4, row=2)
    ttk.Radiobutton(window, text='5', variable=time, value='5').grid(column=4, row=3)
    ttk.Radiobutton(window, text='10', variable=time, value='10').grid(column=4, row=4)
    ttk.Radiobutton(window, text='15', variable=time, value='15').grid(column=4, row=5)
    ttk.Radiobutton(window, text='20', variable=time, value='20').grid(column=4, row=6)

    #FEATURES NEED TO BE ADDED FIRST#

    LogOptions = ttk.Label(window, text="Moves Log",font=12)
    LogOptions.grid(column=1,row=1,ipadx=10)
    
    Complexlog = str()
    
    Complex = ttk.Checkbutton(window, text='Complex log',variable=Complexlog,
                              onvalue=True, offvalue=False)
    Complex.grid(column=2,row=1)

    Log_used = "Simple"
    
    if Complexlog == True:
        Log_used = "Complex"
        
    if Complexlog == False:
        Log_used = "Simple"

    selected = "The Log Used will be " + str(Log_used)

    Log = Label(window,text=selected)
    Log.grid(column=1, row=4,sticky=NW)

    """

    Newgame = ttk.Button(window, text = "Start", command = lambda: NewGame_Initialize_Start(controller,window))
    Newgame.grid(column=1, row=8,ipady=10,ipadx=10,sticky=SW)
    
    Newgame = ttk.Button(window, text = "Quick Start", command = lambda: NewGame_Initialize_Start(controller,window))
    Newgame.grid(column=3, row=8,ipady=10,ipadx=10,sticky=SE)


def NewGame_Initialize_Start(controller,window):
    window.destroy()
    board.InitialPieceSetup()
    board.Turns()

    global selected, square_selected, piece_selected, game_over
    game_over = False
    selected = False
    square_selected = ""
    piece_selected = ""

    PiecesImagesUpdate()
    controller.show_frame(NewGame)


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
                    btn = tk.Button(self, bg="white", image=Empty)
                    Colours[x].append("white")
                    Even = False

                else:
                    btn = tk.Button(self, bg="black", image=Empty)
                    Colours[x].append("black")
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

        global Turn_var
        
        Turn_var = StringVar()
        PlayerTurnLabel = tk.Label(self, textvariable=Turn_var ,font=30)
        PlayerTurnLabel.grid(column=10, row=0, sticky=(N,S))
        
        gap = ttk.Label(self, text=" "*25)
        gap.grid(column=9, row=0,rowspan=8, sticky=(N,S))

        gap2 = ttk.Label(self, text=" "*20)
        gap2.grid(column=16, row=1, rowspan=8, sticky=(N,S))

        log = Text(self, state='disabled',height=25, width=60, wrap="none",font=26)
        log.grid(column=10, row=1, rowspan=6,sticky=(N,S,E,W))

        s = ttk.Scrollbar(self, orient=VERTICAL, command=log.yview)
        s.grid(column=15, row=1, sticky=(N, S),rowspan=6)
        log['yscrollcommand'] = s.set

        button = ttk.Button(self, text = "Undo", command = lambda: UndoMove(self))
        button.grid(column=10, row=7,ipady=10,ipadx=10)

        button = ttk.Button(self, text = "Print Board", command = lambda: board.boardshow())
        button.grid(column=9, row=7,ipady=10,ipadx=10)
        

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

def SaveFirst():
    choice = messagebox.askyesno(message="Would you like to save first?\nSaving the Board state is advised.",
                        title="Quit")
    if choice == True:
        board.Save(board)

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
    global selected, square_selected, piece_selected, Playing, game_over

    try:
        PiecesImagesUpdate()
        grid_info = event.widget.grid_info()

        z = grid_info["column"]
        w = grid_info["row"]

        if 0 <= z <= 8 and 0 <= w <= 8:
            coords = z,w
            Playing = True

    except KeyError or AttributeError:
        Playing = False


    if Playing == True and 0 <= z <= 8 and 0 <= w <= 8 and game_over == False:
        if 0 <= z <= 8 and 0 <= w <= 8:
            if selected == True and (square_selected == coords):
                try:
                    selected = False
                    square_selected = ""
                    piece_selected = ""

                except IndexError:
                    selected = True


            elif selected == False:
                try:
                    if board.board[w][z] is not None:
                        btn = Buttons[z][w]
                        square_selected = z, w
                        piece_selected = board.board[w][z]
                        if board.Wturn() == "W":
                            if board.board[square_selected[1]][square_selected[0]].colour == "w":
                                btn.configure(bg=colour_selected)
                                selected = True

                        if board.Wturn() == "B":
                            if board.board[square_selected[1]][square_selected[0]].colour == "b":
                                btn.configure(bg=colour_selected)
                                selected = True

                        if selected != True:
                            square_selected = ""
                            piece_selected = ""


                except IndexError:
                    selected = False



            elif selected == True:
                if piece_selected != "":
                    try:
                        selected = Movement(square_selected,coords,piece_selected)
                        if selected == False:
                            board.Next_Turn()
                            square_selected = ""
                            piece_selected = ""
                        PiecesImagesUpdate()
                        
                    except AttributeError:
                        selected = True

            if selected == True and piece_selected is not None:
                from_coords = [square_selected[1], square_selected[0]]
                possiblemoves = board.legalmoves(from_coords, board)
                #print(possiblemoves)

                from_coords = [square_selected[1], square_selected[0]]
                possiblemoves = board.legalmoves(from_coords, board)

                for i in range(0, len(possiblemoves)):
                    moves = possiblemoves[i]
                    btn = Buttons[moves[1]][moves[0]]
                    btn.configure(bg=colour_possible_moves)


            elif selected == False:
                for i in range(0, 8):
                    for j in range(0, 8):
                        btn = Buttons[i][j]
                        colour = Colours[i][j]

                        if colour == "white":
                            btn.configure(bg="white")

                        if colour == "black":
                            btn.configure(bg="black")


        win = board.check_mate()
        if win != None:
            if win[0] == "B":
                write("Black Wins")
                coords = win[1]
                button = Buttons[coords[1]][coords[0]]
                button.configure(bg="red")
                game_over = True

            if win[0] == "W":
                write("White Wins")
                coords = win[1]
                button = Buttons[coords[1]][coords[0]]
                button.configure(bg="red")
                game_over = True

                #print(w, z)


def Movement(square_selected,coords,piece_selected):
    PiecesImagesUpdate()
    board.move([square_selected[1], square_selected[0]], [coords[1], coords[0]])
    selected = UpdateBoardPieces(piece_selected, coords, square_selected, False)
    PiecesImagesUpdate()

    
    if board.promote() == True:
        promote_window = tk.Toplevel()
        promote_window.wm_title("Promotion")

        title = tk.Label(promote_window,text="What piece would you like to promote to?",font=40)
        title.grid(row=0,column=0,columnspan=12)
        
        button = tk.Button(promote_window, bg="white",text="Queen",image=wQ,
                           height=65,width=65,command= lambda: promote_to_queen(promote_window))
        button.grid(row=1, column=1, pady=20, padx=40)
        Queen = tk.Label(promote_window,text="Queen",font=40)
        Queen.grid(row=2,column=1)
        
        button1 = tk.Button(promote_window, bg="white",text="Knight",image=wN,
                            height=65,width=65,command= lambda: promote_to_knight(promote_window))
        button1.grid(row=1, column=3, pady=20, padx=40)
        Knight = tk.Label(promote_window,text="Knight",font=40)
        Knight.grid(row=2,column=3)
        
        button2 = tk.Button(promote_window, bg="white",text="Rook",image=wR,
                            height=65,width=65,command= lambda: promote_to_rook(promote_window))
        button2.grid(row=1, column=5, pady=20, padx=40)
        Rook = tk.Label(promote_window,text="Rook",font=40)
        Rook.grid(row=2,column=5)
        
        button3 = tk.Button(promote_window, bg="white",text="Bishop",image=wB,
                            height=65,width=65,command= lambda: promote_to_bishop(promote_window))
        button3.grid(row=1, column=7, pady=20, padx=40)
        Bishop = tk.Label(promote_window,text="Bishop",font=40)
        Bishop.grid(row=2,column=7)

        if board.Wturn() == "W":
            button.configure(image=bQ)
            button1.configure(image=bN)
            button2.configure(image=bR)
            button3.configure(image=bB)

        
    return selected

def promote_to_queen(promote_window):
    board.promote_to("Queen")
    write("Promoted to Queen")
    promote_window.destroy()
    PiecesImagesUpdate()
    
def promote_to_knight(promote_window):
    board.promote_to("Knight")
    write("Promoted to Knight")
    promote_window.destroy()
    PiecesImagesUpdate()
    
def promote_to_rook(promote_window):
    board.promote_to("Rook")
    write("Promoted to Rook")
    promote_window.destroy()
    PiecesImagesUpdate()
    
def promote_to_bishop(promote_window):
    board.promote_to("Bishop")
    write("Promoted to Bishop")
    promote_window.destroy()
    PiecesImagesUpdate()

def UpdateBoardPieces(piece_selected, coords, square_selected, Undo):

    if piece_selected == board.board[coords[1]][coords[0]]:
            selected = False

    if Undo == False and piece_selected == board.board[coords[1]][coords[0]]:
        item = [square_selected[1], square_selected[0]] + [coords[1], coords[0]] + [piece_selected]
        try:
            piece_taken = str(board.taken())
            if piece_taken is not None:
                piece = str(board.board[coords[1]][coords[0]])
                if piece_taken[0] != piece[0]:
                    item += [piece_taken]
            else:
                item += None

        except IndexError:
            None

        print(item)
        stack.push(item)

        piece = str(piece_selected)
        if "w" in piece:
            data = "White "
        if "b" in piece:
            data = "Black "
        if "B" in piece:
            data += "Bishop "
        if "K" in piece:
            data += "King "
        if "N" in piece:
            data += "Knight "
        if "p" in piece:
            data += "Pawn "
        if "Q" in piece:
            data += "Queen "
        if "R" in piece:
            data += "Rook "

        Column = ["8","7","6","5","4","3","2","1"]
        Row = ["A","B","C","D","E","F","G","H"]

        data += "Moved from " + str(Row[square_selected[0]]) + str(Column[square_selected[1]]) + " to "
        data += str(Row[coords[0]]) + str(Column[coords[1]])

        write(data)

        board.turn_over()

    try:
        return selected
    except UnboundLocalError:
        selected = True
        return selected


def PiecesImagesUpdate():
    for i in range(0, 8):
        for j in range(0, 8):
            btn = Buttons[i][j]
            if board.board[j][i] is not None:
                if str(board.board[j][i]).replace("  ", "") == "bB":
                    btn.configure(image=bB)
                if str(board.board[j][i]).replace("  ", "") == "bK":
                    btn.configure(image=bK)
                if str(board.board[j][i]).replace("  ", "") == "bN":
                    btn.configure(image=bN)
                if str(board.board[j][i]).replace("  ", "") == "bp":
                    btn.configure(image=bp)
                if str(board.board[j][i]).replace("  ", "") == "bQ":
                    btn.configure(image=bQ)
                if str(board.board[j][i]).replace("  ", "") == "bR":
                    btn.configure(image=bR)

                if str(board.board[j][i]).replace("  ", "") == "wB":
                    btn.configure(image=wB)
                if str(board.board[j][i]).replace("  ", "") == "wK":
                    btn.configure(image=wK)
                if str(board.board[j][i]).replace("  ", "") == "wN":
                    btn.configure(image=wN)
                if str(board.board[j][i]).replace("  ", "") == "wp":
                    btn.configure(image=wp)
                if str(board.board[j][i]).replace("  ", "") == "wQ":
                    btn.configure(image=wQ)
                if str(board.board[j][i]).replace("  ", "") == "wR":
                    btn.configure(image=wR)

            if selected != True:
                btn = Buttons[i][j]
                colour = Colours[j][i]
                if colour == "white":
                    btn.configure(bg="white")

                if colour == "black":
                    btn.configure(bg="black")

            if board.board[j][i] is None:
                btn = Buttons[i][j]
                btn.configure(image=Empty)
    
    turn = board.Wturn()
    if turn == "W":
        Turn_var.set("White's turn")
    if turn == "B":
        Turn_var.set("Black's turn")


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
