import random

def can_place_ship(board, row, col, ship_size, orientation):
    size = len(board)

    if orientation == "H":
        if col + ship_size > size:
            return False
        for i in range(ship_size):
            if board[row][col + i] != "~":
                return False
    else: 
        if row + ship_size > size:
            return False
        for i in range(ship_size):
            if board[row + i][col] != "~":
                return False

    return True


def place_ship(board, ship_size, ships_list):
    size = len(board)

    while True:
        orientation = random.choice(["H", "V"])
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)

        if can_place_ship(board, row, col, ship_size, orientation):
            if orientation == "H":
                for i in range(ship_size):
                    board[row][col + i] = "S"
            else:
                for i in range(ship_size):
                    board[row + i][col] = "S"
            return


def place_all_ships(board, ship_sizes, ships_list):
    for ship_size in ship_sizes:
        place_ship(board, ship_size, ships_list)