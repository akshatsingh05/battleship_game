import tkinter as tk
from constants import BOARD_SIZE


def create_computer_board(parent, click_handler, size):
    board_frame = tk.Frame(parent)
    board_frame.pack()   # parent uses pack → OK

    buttons = []
    for r in range(size):
        row = []
        for c in range(size):
            btn = tk.Button(
                board_frame,
                width=3,
                height=1,
                bg="blue",
                command=lambda r=r, c=c: click_handler(r, c)
            )
            btn.grid(row=r, column=c)  # grid ONLY inside board_frame
            row.append(btn)
        buttons.append(row)
    return buttons




def create_player_board(parent, size):
    board_frame = tk.Frame(parent)
    board_frame.pack()

    buttons = []
    for r in range(size):
        row = []
        for c in range(size):
            btn = tk.Button(board_frame, width=3, height=1, bg="blue")
            btn.grid(row=r, column=c)
            row.append(btn)
        buttons.append(row)
    return buttons



def update_player_board(player_board, player_buttons):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cell = player_board[r][c]
            btn = player_buttons[r][c]

            if cell == "X":
                btn.config(bg="red")          # Hit ship
            elif cell == "O":
                btn.config(bg="green")        # Miss
            elif cell == "S":
                btn.config(bg="gray")         # Player ship (VISIBLE)
            else:
                btn.config(bg="blue")         # Water

