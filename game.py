from player import *

class Game:
    def __init__(self, gui_or_terminal):
        if gui_or_terminal == 'T':
            self.use_terminal = True
        else:
            self.use_terminal = False
        self.players = []
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.define_players()
        self.print_board()
        self.score = {'X':0, 'O':0}
        self.game_on = True

    def define_players(self):
        if self.use_terminal:
            player_1 = input("Choose Player 1 (X/O): ")
            while player_1 != "O" and player_1 != "X":
                print("Invalid input. Type X or O")
                player_1 = input("Choose Player 1 (X/O): ")
            if player_1 == "X":
                self.curr_player = 0
            elif player_1 == "O":
                self.curr_player = 1
        else:
            self.curr_player = 0
        self.players.append(Player('X', 'blue'))
        self.players.append(Player('O', 'red'))

    def print_board(self):
        if self.use_terminal:
            print(self.board[0] + " | " + self.board[1] + " | " + self.board[2] + "      " + "1|2|3")
            print('--' + "--" + '--' + "-" + '--' + "     " + " -----")
            print(self.board[3] + " | " + self.board[4] + " | " + self.board[5] + "      " + "4|5|6")
            print('--' + "--" + '--' + "-" + '--' + "     " + " -----")
            print(self.board[6] + " | " + self.board[7] + " | " + self.board[8] + "      " + "7|8|9")

    def print_winner(self, p_winner):
        print("Congratulations! player " + p_winner + " WON!")

    def print_score(self):
        if self.use_terminal:
            for k, v in self.score.items():
                print(f"Player: {k}, score: {v}")

    def is_valid_move(self, position):
        return self.board[position] == ' '

    def play_terminal(self):
        print("Current player turn: " + self.players[self.curr_player].symbol)
        position = input("Choose position on board (from 1 - 9): ")
        valid_input = False
        while not valid_input:
            while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                position = input("Choose position on board (from 1 - 9): ")
            position = int(position) - 1
            if self.is_valid_move(position):
                valid_input = True
            else:
                print("Position is taken, you must choose another position!")
        self.board[position] = self.players[self.curr_player].symbol
        self.update_curr_player()
        self.print_board()

    def play(self, i):
        self.board[i] = self.players[self.curr_player].symbol

    def update_curr_player(self):
        self.curr_player = int(not self.curr_player)

    def check_tie(self):
        if ' ' not in self.board:
            self.game_on = False
            if self.use_terminal:
                print("It's a Tie")
            return True
        return False

    def check_row_combination(self):
        p_winner = ''
        if self.board[0] == self.board[1] == self.board[2] != ' ':
            self.game_on = False
            p_winner = self.board[0]
        elif self.board[3] == self.board[4] == self.board[5] !=  ' ':
            self.game_on = False
            p_winner = self.board[3]
        elif self.board[6] == self.board[7] == self.board[8] !=  ' ':
            self.game_on = False
            p_winner = self.board[6]
        if p_winner != '':
            self.score[p_winner] += 1
            if self.use_terminal:
                self.print_winner(p_winner)

    def check_col_combination(self):
        p_winner = ''
        if self.board[0] == self.board[3] == self.board[6] != ' ':
            self.game_on = False
            p_winner = self.board[0]
        elif self.board[1] == self.board[4] == self.board[7] != ' ':
            self.game_on = False
            p_winner = self.board[1]
        elif self.board[2] == self.board[5] == self.board[8] != ' ':
            self.game_on = False
            p_winner = self.board[2]
        if p_winner != '':
            self.score[p_winner] += 1
            if self.use_terminal:
                self.print_winner(p_winner)

    def check_diag_combination(self):
        p_winner = ''
        if self.board[0] == self.board[4] == self.board[8] !=  ' ':
            self.game_on = False
            p_winner = self.board[0]
        elif self.board[2] == self.board[4] == self.board[6] !=  ' ':
            self.game_on = False
            p_winner = self.board[2]
        if p_winner != '':
            self.score[p_winner] += 1
            if self.use_terminal:
                self.print_winner(p_winner)

    def check_winner(self):
        self.check_row_combination()
        self.check_col_combination()
        self.check_diag_combination()
        return not self.game_on

    def reset_game(self):
        keep_playing = input("Do you want to keep playing? Y/N ")
        if keep_playing == "Y":
            self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
            self.define_players()
            self.print_board()
            self.game_on = True
        else:
            exit()

    def reset_game_board(self):
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.define_players()
        self.print_board()
        self.game_on = True


    def game_loop(self):
        while self.game_on:
            self.play_terminal()
            self.check_tie()
            self.check_winner()
            if self.game_on == False:
                self.print_score()
                self.reset_game()

if __name__ == '__main__':
    game  = Game('T')
    game.game_loop()