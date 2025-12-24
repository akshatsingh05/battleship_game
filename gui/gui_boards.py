import tkinter as tk
from constants import BOARD_SIZE


def create_computer_board(parent, click_handler):
    buttons = []
    grid = tk.Frame(parent)
    grid.pack()

    for r in range(BOARD_SIZE):
        row = []
        for c in range(BOARD_SIZE):
            btn = tk.Button(
                grid,
                width=4,
                height=2,
                font=("Arial", 14),
                bg="blue",
                activebackground="blue",
                command=lambda r=r, c=c: click_handler(r, c)
            )
            btn.grid(row=r, column=c, padx=2, pady=2)
            row.append(btn)
        buttons.append(row)

    return buttons


def create_player_board(parent):
    buttons = []
    grid = tk.Frame(parent)
    grid.pack()

    for r in range(BOARD_SIZE):
        row = []
        for c in range(BOARD_SIZE):
            btn = tk.Button(
                grid,
                width=4,
                height=2,
                font=("Arial", 14),
                bg="blue",
                state="disabled"
            )
            btn.grid(row=r, column=c, padx=2, pady=2)
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

