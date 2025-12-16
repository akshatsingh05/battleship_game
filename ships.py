import random
from constants import BOARD_SIZE
from board import print_board

def can_place_ship(board, row, col, ship_size, orientation):
    if orientation == "H":
        if col + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            if board[row][col + i] != "~":
                return False
    else:
        if row + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            if board[row + i][col] != "~":
                return False
    return True


def place_ship(board, ship_size):
    while True:
        orientation = random.choice(["H", "V"])
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)

        if can_place_ship(board, row, col, ship_size, orientation):
            if orientation == "H":
                for i in range(ship_size):
                    board[row][col + i] = "S"
            else:
                for i in range(ship_size):
                    board[row + i][col] = "S"
            break


def place_all_ships(board):
    for ship_size in [3, 2]:
        place_ship(board, ship_size)


def player_place_ships(board):
    ships = [3, 2]
    print("\n🚢 Time to place your ships!")

    for ship_size in ships:
        while True:
            print_board(board, hide_ships=False)
            print(f"\nPlacing ship of size {ship_size}")

            try:
                row = int(input("Enter starting row (0-4): "))
                col = int(input("Enter starting column (0-4): "))
                orientation = input("Orientation (H/V): ").upper()

                if orientation not in ["H", "V"]:
                    print("❌ Invalid orientation.")
                    continue

                if row not in range(BOARD_SIZE) or col not in range(BOARD_SIZE):
                    print("❌ Out of bounds.")
                    continue

                if not can_place_ship(board, row, col, ship_size, orientation):
                    print("❌ Cannot place ship here.")
                    continue

                if orientation == "H":
                    for i in range(ship_size):
                        board[row][col + i] = "S"
                else:
                    for i in range(ship_size):
                        board[row + i][col] = "S"
                break

            except ValueError:
                print("❌ Invalid input.")
