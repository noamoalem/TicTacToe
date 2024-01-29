import tkinter as tk
from game import Game
from tkinter import font

class Board(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic Tac Toe")
        self.photo_o = tk.PhotoImage(file=r"O.PNG")
        self.photo_x = tk.PhotoImage(file=r"X.PNG")
        self.photo_b = tk.PhotoImage(file=r"blank.PNG")
        self.cells = {}
        self.game = game
        self.create_board()

    def create_board(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill='x')
        self.txt_display = tk.Label(master=display_frame, text="Start Play", font=font.Font(name="Modern", size=28, weight="bold"))
        self.txt_display.pack()
        self.grid_frame = tk.Frame(master=self)
        self.grid_frame.pack()
        i = 0
        for r in range(3):
            for c in range(3):
                button = tk.Button(master=self.grid_frame, image=self.photo_b)
                self.cells[button] = i
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                i+=1

    def update_button_display(self, clicked_btn):
        if self.game.players[self.game.curr_player].symbol == 'X':
            clicked_btn.config(image=self.photo_x)
        else:
            clicked_btn.config(image=self.photo_o)

    def reset_buttons_display(self):
        for button in self.cells.keys():
            button.config(image=self.photo_b)

    def update_txt_display(self, msg, color="black"):
        self.txt_display["text"] = msg
        self.txt_display["fg"] = color

    def play(self, event):
        clicked_btn = event.widget
        i = self.cells[clicked_btn]
        if self.game.is_valid_move(i):
            self.game.play(i)
            self.update_button_display(clicked_btn)
            if self.game.check_winner():
                msg = f'Congratulations! player "{self.game.players[self.game.curr_player].symbol}" WON!'
                color = self.game.players[self.game.curr_player].color
                self.update_txt_display(msg, color)
                self.finished_game()
            elif self.game.check_tie():
                msg = "It's a Tie!"
                color = "pink"
                self.update_txt_display(msg, color)
                self.finished_game()
            else: # game still on
                self.game.update_curr_player()
                msg = f"{self.game.players[self.game.curr_player].symbol}'s turn"
                color = self.game.players[self.game.curr_player].color
                self.update_txt_display(msg, color)

    def finished_game(self):
        win_x = self.winfo_rootx() + 300
        win_y = self.winfo_rooty() + 100
        self.keep_playing_win = tk.Toplevel()

        self.keep_playing_win.geometry(f'+{win_x}+{win_y}')
        tk.Label(self.keep_playing_win, text="Do you want to keep playing?").pack()
        button1 = tk.Button(self.keep_playing_win, text='Yes', command=self.keep_playing_win.destroy)
        button1.pack()
        button1.bind("<ButtonPress-1>", self.reset_board)
        button2 = tk.Button(self.keep_playing_win, text='No', command=self.keep_playing_win.destroy)
        button2.pack()
        button2.bind("<ButtonPress-1>", self.kill)


    def reset_board(self, event):
        self.game.reset_game_board()
        self.reset_buttons_display()
        self.update_txt_display("Start Play")

    def kill(self, event):
        self.grid_frame.destroy()
        self.keep_playing_win.destroy()
        self.destroy()

def main():
    gui_or_terminal = input("Do you want want to play with gui or temrinal? G/T ")
    game = Game(gui_or_terminal)
    if gui_or_terminal =='G':
        # gui_or_terminal = input("Do you want want to play with gui or temrinal? G/T ")
        board = Board(game)
        board.mainloop()
    else:
        game.game_loop()

if __name__ == '__main__':
    main()