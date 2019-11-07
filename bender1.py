import importlib
from random import *
from keras.models import Sequential

# Init your variables here
SIZE = 7
MIDDLE = 3
WIN = 5
# Put your bot name here
name = "Langue"


# Bender strategy : return the first element in the available cells.
# That always generates horizontal line in the top of the board 

def play(board, available_cells, player):
    res = available_cells[randint(0, len(available_cells)-1)]
    next_pos = False
    board_copy  = board
    if player == 1:
        player_adverse = 2
    else:
        player_adverse = 1
    for i in available_cells:
        if check_win(board_copy, i, player_adverse):
            res = i
            next_pos = True
            print("baise")
            break
    if not next_pos:
        for i in available_cells:
            if check_win(board_copy, i, player):
                res = i
                next_pos = True
                print("gagner")
                break

    return res


def check_win(board, position, player):
    target = player
    board[MIDDLE][MIDDLE] = target  # Middle cell takes the color of the current player
    if board[position[0]][position[1]] != target:
        print("false1")
        return False
    directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
    for direction in directions:
        counter = 0
        for i in range(2):
            p = position[:]
            while 0 <= p[0] < SIZE and 0 <= p[1] < SIZE:
                if board[p[0]][p[1]] == target:
                    counter += 1
                else:
                    break
                p[0] += direction[i][0]
                p[1] += direction[i][1]
        if counter >= WIN + 1:
            board[MIDDLE][MIDDLE] = 0  # The middle cell becomes neutral before return
            print("true")
            return True
    board[MIDDLE][MIDDLE] = 0  # The middle cell becomes neutral before return
    print("false2")
    return False
