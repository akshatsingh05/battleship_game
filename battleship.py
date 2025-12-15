BOARD_SIZE = 5

def create_board():
    """
    Creates and returns a BOARD_SIZE x BOARD_SIZE board filled with water (~)
    """
    board = []
    for _ in range(BOARD_SIZE):
        row = ["~"] * BOARD_SIZE
        board.append(row)
    return board


def print_board(board, hide_ships=True):
    """
    Prints the board.
    If hide_ships is True, ships ('S') are hidden from view.
    """
    print("\n  0 1 2 3 4")
    for i, row in enumerate(board):
        print(i, end=" ")
        for cell in row:
            if cell == "S" and hide_ships:
                print("~", end=" ")
            else:
                print(cell, end=" ")
        print()

import random

def can_place_ship(board, row, col, ship_size, orientation):
    """
    Checks if a ship can be placed at the given location.
    """
    if orientation == "H":
        if col + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            if board[row][col + i] != "~":
                return False

    else:  # Vertical
        if row + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            if board[row + i][col] != "~":
                return False

    return True


def place_ship(board, ship_size):
    """
    Randomly places a ship of given size on the board.
    """
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
    """
    Places all ships on the board.
    """
    ships = [3, 2]  # Ship sizes
    for ship_size in ships:
        place_ship(board, ship_size)



def is_valid_attack(board, row, col):
    """
    Checks if the attack is valid (not already tried).
    """
    return board[row][col] in ["~", "S"]


def attack(board, row, col):
    """
    Applies attack on the board.
    Returns True if hit, False if miss.
    """
    if board[row][col] == "S":
        board[row][col] = "X"
        return True
    elif board[row][col] == "~":
        board[row][col] = "O"
        return False


def player_turn(computer_board):
    """
    Handles player's attack turn.
    Returns False if player exits, True otherwise.
    """
    while True:
        row_input = input("Enter row (0-4) or 'q' to quit: ").strip().lower()

        if row_input in ["q", "quit", "exit"]:
            return False

        col_input = input("Enter column (0-4): ").strip()

        try:
            row = int(row_input)
            col = int(col_input)

            if row not in range(BOARD_SIZE) or col not in range(BOARD_SIZE):
                print("❌ Coordinates out of bounds. Try again.")
                continue

            if not is_valid_attack(computer_board, row, col):
                print("❌ You already attacked this position. Try again.")
                continue

            hit = attack(computer_board, row, col)
            print("🔥 HIT!" if hit else "💦 MISS!")
            return True

        except ValueError:
            print("❌ Invalid input. Enter numbers only.")



def computer_turn(player_board):
    """
    Handles computer's random attack.
    """
    while True:
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)

        if is_valid_attack(player_board, row, col):
            hit = attack(player_board, row, col)
            print(f"\n🤖 Computer attacks ({row}, {col})")
            if hit:
                print("💥 Computer HIT your ship!")
            else:
                print("🌊 Computer MISSED!")
            break

def all_ships_sunk(board):
    """
    Returns True if no ships ('S') remain on the board.
    """
    for row in board:
        if "S" in row:
            return False
    return True

def play_game():
    print("\n🚢 Welcome to Battleship!\n")

    player_board = create_board()
    computer_board = create_board()

    place_all_ships(player_board)
    place_all_ships(computer_board)

    while True:
        print("\n🧍 Your Board:")
        print_board(player_board, hide_ships=False)

        print("\n💻 Computer Board:")
        print_board(computer_board, hide_ships=True)

        # Player turn
        print("\n🎯 Your turn!")
        player_continue = player_turn(computer_board)

        if not player_continue:
            print("\n🚪 You exited the game. Thanks for playing!")
            break

        # Player win check
        if all_ships_sunk(computer_board):
            print("\n🎉 YOU WIN! All enemy ships sunk!")

            print("\n🧍 Final Player Board:")
            print_board(player_board, hide_ships=False)

            print("\n💻 Final Computer Board:")
            print_board(computer_board, hide_ships=False)
            break

        # Computer turn
        print("\n🤖 Computer's turn...")
        computer_turn(player_board)

        # Computer win check
        if all_ships_sunk(player_board):
            print("\n💀 YOU LOST! All your ships have sunk!")

            print("\n🧍 Final Player Board:")
            print_board(player_board, hide_ships=False)

            print("\n💻 Final Computer Board:")
            print_board(computer_board, hide_ships=False)
            break



if __name__ == "__main__":
    play_game()
