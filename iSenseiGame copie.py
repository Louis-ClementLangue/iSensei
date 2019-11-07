import numpy as np
import importlib
import time
import bot
from bot import net

# Import your agents dynamically here

ai_player_1 = importlib.import_module("c3po", package=None)
ai_player_2 = importlib.import_module("bender", package=None)

print("STARTING : " + ai_player_1.name + " VS " + ai_player_2.name + "\n")

SIZE = 7
MIDDLE = 3
WIN = 5


class iSensei(object):
    def __init__(self):
        self.board = [[0 for x in range(SIZE)] for y in range(SIZE)]
        self.lastPosition = [-1, -1]
        self.player = False  # False for player 1 and True for player 2
        self.firstPlayer = False  # Who plays first ? switch after each game
        self.playing = False

    # Call the AI to play 
    def play(self):
        [r, c] = [-1, -1]
        availables = self.get_available_cells()

        if len(availables) > 0:
            [r, c] = ai_player_1.play(self.board, availables, 1) if self.player else ai_player_2.play(self.board,
                                                                                                      availables, 2)
            if self.board[r][c] == 0:  # I do not trust your AI, so I check again
                self.lastPosition = [r, c]
                self.board[r][c] = 1 if self.player else 2
        else:  # No available cell, stop the game
            self.playing = False

    # Infinite loop of games
    def execute(self, nbEntrainement):
        try:
            self.start()
            i = 0
            self.tab = []
            while i < nbEntrainement:
                print(i)
                self.win_turn = np.copy(self.board)
                # Let the bot play
                self.play()
                # Check if there is a winner
                if self.check_win(self.lastPosition, self.player):
                    self.tab.append([self.last_turn, self.findLastMovement(self.last_turn, self.win_turn)])
                    i += 1
                    print(ai_player_1.name if self.player else ai_player_2.name,
                          "(O)" if self.player else "(X)",
                          "won :")
                    self.playing = False  # Stop playing

                # No winner but no more cells. Find the longest aligned sequence for each player
                elif len(self.get_available_cells()) == 0:
                    self.tab.append([self.last_turn, self.findLastMovement(self.last_turn, self.win_turn)])
                    i += 1
                    print("DRAW")
                    print("X: ", self.check_win_by_points(False))
                    print("O: ", self.check_win_by_points(True))
                    self.playing = False  # Stop playing

                # Switch player
                else:
                    self.player = not self.player

                # Print the board and restart new game
                if not self.playing:
                    self.print_board()
                    time.sleep(.5)  # Wait half second
                    self.start()  # Start a new Game

                self.last_turn = np.copy(self.board)
        except KeyboardInterrupt:
            print("Stopping iSensei...")

    # Start / clean the board
    def start(self):
        self.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.lastPosition = [-1, -1]
        self.firstPlayer = not self.firstPlayer
        self.player = self.firstPlayer
        self.playing = True

    # Find all empty cells
    def get_available_cells(self):
        availables = []
        for row in range(SIZE):
            for column in range(SIZE):
                if (row == MIDDLE and column == MIDDLE):  # Never play the cell in the middle
                    continue
                if self.board[row][column] == 0:
                    availables.append([row, column])
        return availables

    # Print the board
    def print_board(self):
        for r in range(SIZE):  # ROWS
            for c in range(SIZE):  # COLUMNS
                if r == MIDDLE and c == MIDDLE:
                    print('% ', end='')
                elif self.board[r][c] == 0:
                    print('. ', end='')
                elif self.board[r][c] == 1:
                    print('O ', end='')
                elif self.board[r][c] == 2:
                    print('X ', end='')
            print()
        print()

    # Check if a player win after a move
    def check_win(self, position, player):
        target = 1 if player else 2
        self.board[MIDDLE][MIDDLE] = target  # Middle cell takes the color of the current player
        if self.board[position[0]][position[1]] != target:
            return False
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        for direction in directions:
            counter = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] < SIZE and 0 <= p[1] < SIZE:
                    if self.board[p[0]][p[1]] == target:
                        counter += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]
            if counter >= WIN + 1:
                self.board[MIDDLE][MIDDLE] = 0  # The middle cell becomes neutral before return
                return True
        self.board[MIDDLE][MIDDLE] = 0  # The middle cell becomes neutral before return
        return False

    # Find the longest sequence made by a player 
    def check_win_by_points(self, player):
        target = 1 if player else 2
        self.board[MIDDLE][MIDDLE] = target  # The middle cell takes the color of the current player
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        best = 0
        for r in range(SIZE):  # ROWS
            for c in range(SIZE):  # COLUMNS
                for direction in directions:
                    counter = 0
                    for i in range(2):
                        p = [r, c]
                        while 0 <= p[0] < SIZE and 0 <= p[1] < SIZE:
                            if self.board[p[0]][p[1]] == target:
                                counter += 1
                            else:
                                break
                            p[0] += direction[i][0]
                            p[1] += direction[i][1]
                    best = max(best, counter - 1)
        self.board[MIDDLE][MIDDLE] = 0  # The middle cell becomes neutral before return
        return best

    def findLastMovement(self, last_turn, win_turn):
        res = win_turn - last_turn
        res = res / np.amax(win_turn)
        return res

    def __call__(self, nbEntrainement):
        self.execute(nbEntrainement)


if __name__ == "__main__":
    partie = iSensei()
    partie(100)
    train = partie.tab[:, 0]
    target = partie.tab[:, 1]
    train_data = np.array(train[0]).reshape(49)
    target_data = np.array(target[0]).reshape(49)
    newReseau = net(False)
    net.training(train_data, target_data)
    net.save()
