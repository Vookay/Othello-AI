import tkinter as tk
from tkinter import *
import copy

class Othello:
    #spēles laukuma inicializācija
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        #sākuma stāvoklis
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        #pašreizējās krāsas gājiens, 'B' jo melnā krāsa sāk pirmā
        self.turn = 'B'
        #cilvēka kauliņu krāsa, tiek izvēlētā izvēles logā
        self.playerTurn = 'B'
        #datora kauliņu krāsa
        self.aiTurn = 'W'
        #spēles laukuma kopija, ko izmanto algoritmā
        self.savedBoard = copy.deepcopy(self.board)
    
    #pārbaude, vai pašreizējais spēlētājs var veikt gājienu dotajās koordinātēs
    def is_valid_move(self, i, j):
        if self.board[i][j] != '.':
            return False
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                r, c = i+di, j+dj
                if r < 0 or r >= 8 or c < 0 or c >= 8:
                    continue
                if self.board[r][c] == self.turn:
                    continue
                while self.board[r][c] != '.':
                    r += di
                    c += dj
                    if r < 0 or r >= 8 or c < 0 or c >= 8:
                        break
                    if self.board[r][c] == self.turn:
                        return True
        return False
    
    #gājiena veikšana ar pašreizējo krāsu
    def make_move(self, i, j):
        self.board[i][j] = self.turn
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                r, c = i+di, j+dj
                if r < 0 or r >= 8 or c < 0 or c >= 8:
                    continue
                if self.board[r][c] == self.turn:
                    continue
                #kauliņu apgriešana
                flips = []
                while self.board[r][c] != '.':
                    flips.append((r, c))
                    r += di
                    c += dj
                    if r < 0 or r >= 8 or c < 0 or c >= 8:
                        break
                    if self.board[r][c] == self.turn:
                        for fr, fc in flips:
                            self.board[fr][fc] = self.turn
                        break    

    #pārbaude, vai pašreizējai krāsai vispār ir iespējami gājieni   
    def move_check(self):
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    return True
        return False
                    
    #algoritms prieks heiristiskā novērtējuma iegūšanas gājienam, tiek izmantots alfa-beta algoritms
    def alphabeta(self, depth, maximizing_player, alpha=-float('inf'), beta=float('inf')):
        print(depth)
        if self.aiTurn == 'W':
            value = self.get_score()[1] - self.get_score()[0]
        else:
            value = self.get_score()[0] - self.get_score()[1]
        if depth == 0:
            return value

        #maksimizētājs
        if maximizing_player:
            val = alpha
            self.turn = self.aiTurn
            for i in range(8):
                for j in range(8):
                    if self.is_valid_move(i, j):
                        self.make_move(i, j)
                        val = max(val, self.alphabeta(depth-1, False, alpha, beta))
                        alpha = max(alpha, val)
                        #beta nogriešana
                        if val >= beta:
                            return val
            return val
        #minimizētājs
        else:
            val = beta
            self.turn = self.playerTurn
            for i in range(8):
                for j in range(8):
                    if self.is_valid_move(i, j):
                        self.make_move(i, j)
                        val = min(val, self.alphabeta(depth-1, True, alpha, beta))
                        beta = min(beta, val)
                        #alfa nogriešana
                        if val <= alpha:
                            return val
            return val

    #nosaka labako gajienu, izmantojot heiristisko novērtējumu 
    def find_best_move(self) : 
        bestVal = -float('inf')
        bestMove = (0, 0)
        for i in range(8) :     
            for j in range(8) :
                if self.is_valid_move(i, j): 
                    self.make_move(i, j)
                    #izsaukts alfa-beta algoritms, ar noteiktu dziļumu un maksimizāciju
                    val = self.alphabeta(10, True)
                    self.board = copy.deepcopy(self.savedBoard)
                    if (val > bestVal) :                
                        bestMove = (i, j)
                        bestVal = val
        return bestMove

    #datora gājiena veikšana, izmantojot labāko gājienu, kas tika atrasts
    def ai_move(self):
        self.savedBoard = copy.deepcopy(self.board)
        move = self.find_best_move()
        self.turn = self.aiTurn
        self.board = copy.deepcopy(self.savedBoard)
        self.make_move(move[0], move[1])        
        self.turn = self.playerTurn
    
    #punktu (krāsas kauliņu) saskaitīšana
    def get_score(self):
        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'B':
                    black += 1
                elif self.board[i][j] == 'W':
                    white += 1
        return (black, white)
    
    #spēles uzsākšana
    def start(self):
        #krāsas izvēles logs
        def choiceWindow():
            choice_window = tk.Toplevel(window)
            label = tk.Label(choice_window, text="Choose your color. Black moves first!")
            def on_white_choice(event):
                self.playerTurn = 'W'
                self.aiTurn = 'B'
                closeWindow()
            def on_black_choice(event):
                self.playerTurn = 'B'
                self.aiTurn = 'W'
                closeWindow()
            choiceBtn1 = tk.Button (choice_window, width=9, height=3, text="WHITE")
            choiceBtn2 = tk.Button (choice_window, width=9, height=3, text="BLACK")
            exitBtn = tk.Button(choice_window, width=9, height=3, text="EXIT", command =lambda: [closeWindow(), exit()])
            choiceBtn1.bind('<Button-1>', on_white_choice)
            choiceBtn2.bind('<Button-1>', on_black_choice)

            label.pack()
            choiceBtn1.pack()
            choiceBtn2.pack()
            exitBtn.pack()
            choice_window.geometry(f'{width}x{height}+{center_x}+{center_y}')

            def closeWindow():
                choice_window.destroy()
                window.deiconify()
            choice_window.wait_window()   
        
        #spēles beigu logs
        def gameOverWindow(winner):
            gameover_window = tk.Toplevel(window)
            if winner == 'White':
                label = tk.Label(gameover_window, text="White wins!")
            elif winner == 'Black':
                label = tk.Label(gameover_window, text="Black wins!")
            else:
                label = tk.Label(gameover_window, text="It's a tie!")
            def restart(event):
                gameover_window.destroy()
                window.withdraw()
                Othello.start(Othello())
                choiceWindow()
            restartBtn = tk.Button(gameover_window, width=9, height=3, text="RESTART")
            exitBtn = tk.Button(gameover_window, width=9, height=3, text="EXIT", command = exit)
            restartBtn.bind('<Button-1>', restart)
            label.pack()
            restartBtn.pack()
            exitBtn.pack()
            gameover_window.geometry(f'{width}x{height}+{center_x}+{center_y}')

        #galvenais spēles logs
        window = tk.Tk()
        window.title("Othello")
        width = 500
        height = 500
        window.configure(bg='light green')
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        window.geometry(f'{width}x{height}+{center_x}+{center_y}')
        window.withdraw()

        choiceWindow()

        #lauciņa uzspiešanas funkcija, ja viss izpildas pareizi, spēlētājs veic gājienu un pēc tam gājienu veic dators
        def on_tile_click(event):
            button = event.widget
            row = button.grid_info()['row']
            col = button.grid_info()['column']
            if self.is_valid_move(row, col):
                self.make_move(row, col)
                updateButtons()
                self.turn = self.aiTurn
                if check_moves():          
                    self.ai_move()
                    check_moves()
                    updateButtons()
        
        #spēles vizuālā laukuma izveide, kas sastāv no 8x8 lauciņiem, uz kuriem var uzklikšķināt
        button_grid = []
        for i in range(8):
            button_row = []
            window.grid_rowconfigure(i, weight=1)
            for j in range(8):
                button = tk.Button(window, width=6, height=3, background = 'green', font=('Helvetica', 10, 'bold'))
                button.bind('<Button-1>', on_tile_click)
                button.grid(row=i, column=j, sticky="sewn")
                button_row.append(button)
                window.grid_columnconfigure(j, weight=1)
            button_grid.append(button_row)

        #atjaunina lauciņu stāvokli un kauliņu stāvokli
        def updateButtons():
            for i in range(8):
                for j in range(8):
                    if self.is_valid_move(i, j):
                        button_grid[i][j].configure(background = 'green')
                    else:
                        button_grid[i][j].configure(background = 'dark green')
                    if self.board[i][j] == 'B':
                        button_grid[i][j].configure(text = '⬤', foreground = 'black')
                    elif self.board[i][j] == 'W':
                        button_grid[i][j].configure(text = '⬤', foreground = 'white')

        #spēles rezultāta iegūšana un spēles beigu loga atvēršana
        def gameOver():
            black_score, white_score = self.get_score()
            if black_score > white_score:
                gameOverWindow('Black')
            elif white_score > black_score:
                gameOverWindow('White')
            else:
                gameOverWindow('Tie')

        #pārbaude, vai ir iespējami gājieni, ja nav, tad spēle beidzas
        def check_moves():
            if self.turn == self.aiTurn:
                if not self.move_check():
                    self.turn = self.playerTurn
                    if not self.move_check():
                        gameOver()
                        return False
                    else:
                        updateButtons()
                        return False
            else:
                if not self.move_check():
                    self.turn = self.aiTurn
                    if not self.move_check():
                        gameOver()
                        return False
                    else:
                        self.ai_move()
                        updateButtons()
                        if not check_moves():
                            return False
                        updateButtons()
            return True

        #ja dators ir melnā krāsa, tad tas veic pirmo gājienu
        if self.aiTurn == 'B': self.ai_move()
        updateButtons()

        window.mainloop()

#tiek palaista spēle
Othello.start(Othello())