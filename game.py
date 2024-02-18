from player import *
from typing import List

class Game:

    def __init__(self, gui_or_terminal: str):
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

    def define_players(self) -> None:
        """
        This function defines the first player of the game.
        """
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

    def print_board(self) -> None:
        """
        This function prints the current board state.
        """
        if self.use_terminal:
            print(self.board[0] + " | " + self.board[1] + " | " + self.board[2] + "      " + "1|2|3")
            print('--' + "--" + '--' + "-" + '--' + "     " + " -----")
            print(self.board[3] + " | " + self.board[4] + " | " + self.board[5] + "      " + "4|5|6")
            print('--' + "--" + '--' + "-" + '--' + "     " + " -----")
            print(self.board[6] + " | " + self.board[7] + " | " + self.board[8] + "      " + "7|8|9")

    def print_winner(self, p_winner: str) -> None:
        """
        This function prints the winner player of the current game.
        :param p_winner: X or O.
        """
        print("Congratulations! player " + p_winner + " WON!")

    def print_score(self) -> None:
        """
        This function prints the score state.
        """
        if self.use_terminal:
            for k, v in self.score.items():
                print(f"Player: {k}, score: {v}")

    def is_valid_move(self, position: int) -> None:
        """
        This function check if the player choose a valid position
        :return: True if its a valid position, false otherwise.
        """
        return self.board[position] == ' '

    def play_terminal(self) -> None:
        """
        This function play a one turn in the terminal.
        The player need to choose position, represented by a index between 1-9.
        """
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

    def play(self, i: int) -> None:
        """
        This function update the board with a given position.
        :param i: index between 1-9 which represent a position on the board.
        """
        self.board[i] = self.players[self.curr_player].symbol

    def update_curr_player(self) -> None:
        """
        This function change the current player.
        """
        self.curr_player = int(not self.curr_player)

    def check_tie(self) -> bool:
        """
        This function check if the game ends with a tie.
        :return: True if the game ends with true, False otherwise.
        """
        if ' ' not in self.board:
            self.game_on = False
            if self.use_terminal:
                print("It's a Tie")
            return True
        return False

    def check_row_combination(self) -> None:
        """
        This function check if one of the players have a winning row combination.
        """
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

    def check_col_combination(self) -> None:
        """
        This function check if one of the players have a winning column combination.
        """
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

    def check_diag_combination(self) -> None:
        """
        This function check if one of the players have a winning diagonal combination.
        """
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

    def check_winner(self) -> bool:
        """
        This function check if one of the player won the game.
        :return: True if one of the player won the game, False otherwise.
        """
        self.check_row_combination()
        self.check_col_combination()
        self.check_diag_combination()
        return not self.game_on

    def get_board(self) -> List[str]:
        """
        This function return the game board.
        :return: The game board.
        """
        return self.board

    def reset_game(self) -> None:
        """
        This function ask the player if he wants to keep playing and if so its reset the game.
        """
        keep_playing = input("Do you want to keep playing? Y/N ")
        if keep_playing == "Y":
            self.reset_game_board()
        else:
            exit()

    def reset_game_board(self):
        """
        This function reset the game board and state.
        """
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.define_players()
        self.print_board()
        self.game_on = True

    def game_loop(self) -> None:
        """
        This function runs the game.
        """
        while self.game_on:
            self.play_terminal()
            self.check_tie()
            self.check_winner()
            if self.game_on == False:
                self.print_score()
                self.reset_game()

# if __name__ == '__main__':
#     game  = Game('T')
#     game.game_loop()