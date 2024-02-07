import random
import tkinter as tk
from game import Game
from tkinter import font

class Board(tk.Tk):

    def __init__(self, game, one_or_two_players=2):
        super().__init__()
        self.title("Tic Tac Toe")
        self.photo_o = tk.PhotoImage(file=r"O.PNG")
        self.photo_x = tk.PhotoImage(file=r"X.PNG")
        self.photo_b = tk.PhotoImage(file=r"blank.PNG")
        self.one_or_two_players = one_or_two_players
        self.cells = {}
        self.game = game
        self.create_board()

    def create_board(self) -> None:
        """
        This function create the board display, the board contains a text display and a grid
        with the buttons.
        """
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill='x')
        self.txt_display = tk.Label(master=display_frame, text="Start Play", font=font.Font(name="Modern", size=28, weight="bold"))
        self.txt_display.pack()
        self.grid_frame = tk.Frame(master=self)
        self.grid_frame.pack()
        i = 0
        for r in range(3):
            for c in range(3):
                button = tk.Button(master=self.grid_frame, image=self.photo_b, bg='white')
                self.cells[button] = i
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                i+=1

    def update_button_display(self, clicked_btn) -> None:
        """
        This function update the given pressed button display.
        :param clicked_btn: a given pressed button.
        """
        if self.game.players[self.game.curr_player].symbol == 'X':
            clicked_btn.config(image=self.photo_x)
        else:
            clicked_btn.config(image=self.photo_o)

    def reset_buttons_display(self) -> None:
        """
        This function reset the board buttons display.
        """
        for button in self.cells.keys():
            button.config(image=self.photo_b)

    def update_txt_display(self, txt: str, color: str= "black") -> None:
        """
        This function update the text display on screen.
        :param txt: a given text to display.
        :param color: a given color to displat the text with.
        """
        self.txt_display["text"] = txt
        self.txt_display["fg"] = color

    def play(self, event) -> None:
        """
        This function playes one turn if two players play against each other, or two turns if
        the player play against the computer.
        :param event: ButtonPress event.
        """
        clicked_btn = event.widget
        i = self.cells[clicked_btn]
        if self.game.is_valid_move(i):
            self.game.play(i)
            self.update_button_display(clicked_btn)
            if self.game.check_winner():
                txt = f'Congratulations! player "{self.game.players[self.game.curr_player].symbol}" WON!'
                color = self.game.players[self.game.curr_player].color
                self.update_txt_display(txt, color)
                self.finished_game()
            elif self.game.check_tie():
                txt = "It's a Tie!"
                color = "pink"
                self.update_txt_display(txt, color)
                self.finished_game()
            else: # game still on
                self.game.update_curr_player()
                txt = f"{self.game.players[self.game.curr_player].symbol}'s turn"
                color = self.game.players[self.game.curr_player].color
                self.update_txt_display(txt, color)
                # if we play against the computer
                if self.one_or_two_players == 1 and self.game.players[self.game.curr_player].symbol == 'O':
                    # i = random.randint(0, 8)
                    i = self.computer_player()
                    clicked_btn_comp = [b for b in self.cells.keys() if self.cells[b] == i][0]
                    while not self.game.is_valid_move(i):
                        # i = random.randint(0, 8)
                        i = self.computer_player()
                        clicked_btn_comp = [b for b in self.cells.keys() if self.cells[b]==i][0]
                    clicked_btn_comp.event_generate("<ButtonPress-1>") # simulate buttom pressed

    def computer_player(self) -> int:
        """
        This function play a turn of the computer player.
        It search for a a position that prevent the other player to win.
        """
        board = self.game.get_board()
        # check rows
        if board[0] == board[1] == 'X' and board[2] == ' ':
            return 2
        elif board[1] == board[2] == 'X' and board[0] == ' ':
            return 0
        elif board[3] == board[4] == 'X' and board[5] == ' ':
            return 5
        elif board[4] == board[5] == 'X' and board[3] == ' ':
            return 3
        elif board[6] == board[7] == 'X' and board[8] == ' ':
            return 8
        elif board[7] == board[8] == 'X' and board[6] == ' ':
            return 6
        # check cols
        if board[0] == board[3] == 'X' and board[6] == ' ':
            return 6
        elif board[3] == board[6] == 'X' and board[0] == ' ':
            return 0
        elif board[1] == board[4] == 'X' and board[7] == ' ':
            return 7
        elif board[4] == board[7] == 'X' and board[1] == ' ':
            return 1
        elif board[2] == board[5] == 'X' and board[8] == ' ':
            return 8
        elif board[5] == board[8] == 'X' and board[2] == ' ':
            return 2
        # check diagonal
        if board[0] == board[4] == 'X' and board[8] == ' ':
            return 8
        elif board[4] == board[8] == 'X' and board[0] == ' ':
            return 0
        elif board[2] == board[4] == 'X' and board[6] == ' ':
            return 6
        elif board[4] == board[6] == 'X' and board[2] == ' ':
            return 2
        else:
            return random.randint(0, 8)

    def finished_game(self) -> None:
        """
        This function ask the player if he wants to keep playing or not, if not it kills the GUI.
        """
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

    def reset_board(self, event) -> None:
        """
        This function reset the game and the game board.
        :param event: ButtonPress event.
        """
        self.game.reset_game_board()
        self.reset_buttons_display()
        self.update_txt_display("Start Play")

    def kill(self, event) -> None:
        """
        This function kill the game GUI if the user pressed the relevant button.
        :param event: ButtonPress event.
        """
        self.grid_frame.destroy()
        self.keep_playing_win.destroy()
        self.destroy()

def game_loop() -> None:
    """
    This function runs the game.
    Ask the user if he wants to play with gui or terminal, and if he wants to play
    against the computer or another player.
    """
    gui_or_terminal = input("Do you want want to play with gui or temrinal? G/T ")
    game = Game(gui_or_terminal)
    if gui_or_terminal == 'G':
        one_or_two_players = input("Do you want want to play against the computer? Y/N ")
        if one_or_two_players == 'Y':
            board = Board(game, 1)
        else:
            board = Board(game, 2)
        board.mainloop()
    else:
        game.game_loop()

if __name__ == '__main__':
    game_loop()