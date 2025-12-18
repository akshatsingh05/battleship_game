import random
from constants import BOARD_SIZE

def is_valid_attack(board, row, col):
    return board[row][col] in ["~", "S"]


def attack(board, row, col):
    if board[row][col] == "S":
        board[row][col] = "X"
        return True
    elif board[row][col] == "~":
        board[row][col] = "O"
        return False


def player_turn(computer_board):
    while True:
        row_input = input("Enter row (0-4) or 'q' to quit: ").lower()
        if row_input in ["q", "quit", "exit"]:
            return False

        col_input = input("Enter column (0-4): ")

        try:
            row = int(row_input)
            col = int(col_input)

            if row not in range(BOARD_SIZE) or col not in range(BOARD_SIZE):
                print("❌ Out of bounds.")
                continue

            if not is_valid_attack(computer_board, row, col):
                print("❌ Already attacked.")
                continue

            hit = attack(computer_board, row, col)
            print("🔥 HIT!" if hit else "💦 MISS!")
            return True

        except ValueError:
            print("❌ Invalid input.")


def computer_turn(player_board):
    while True:
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)

        if is_valid_attack(player_board, row, col):
            hit = attack(player_board, row, col)
            print(f"\n🤖 Computer attacks ({row}, {col})")
            print("💥 HIT!" if hit else "🌊 MISS!")
            break
