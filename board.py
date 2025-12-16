from constants import BOARD_SIZE

def create_board():
    board = []
    for _ in range(BOARD_SIZE):
        board.append(["~"] * BOARD_SIZE)
    return board


def print_board(board, hide_ships=True):
    print("\n  0 1 2 3 4")
    for i, row in enumerate(board):
        print(i, end=" ")
        for cell in row:
            if cell == "S" and hide_ships:
                print("~", end=" ")
            else:
                print(cell, end=" ")
        print()


def all_ships_sunk(board):
    for row in board:
        if "S" in row:
            return False
    return True
