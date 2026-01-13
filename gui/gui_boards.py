import tkinter as tk

def get_cell_size(size):
    if size <= 5:
        return 4, 2
    elif size <= 7:
        return 3, 2
    else:
        return 2, 1


def create_computer_board(parent, click_handler, size):
    board_frame = tk.Frame(parent)
    board_frame.pack()

    w, h = get_cell_size(size)

    buttons = []
    for r in range(size):
        row = []
        for c in range(size):
            btn = tk.Button(
                board_frame,
                width=w,
                height=h,
                bg="blue",
                command=lambda r=r, c=c: click_handler(r, c)
            )
            btn.grid(row=r, column=c, padx=1, pady=1)
            row.append(btn)
        buttons.append(row)
    return buttons


def create_player_board(parent, size):
    board_frame = tk.Frame(parent)
    board_frame.pack()

    w, h = get_cell_size(size)

    buttons = []
    for r in range(size):
        row = []
        for c in range(size):
            btn = tk.Button(
                board_frame,
                width=w,
                height=h,
                bg="blue"
            )
            btn.grid(row=r, column=c, padx=1, pady=1)
            row.append(btn)
        buttons.append(row)
    return buttons



def update_player_board(player_board, player_buttons):
    size = len(player_board)

    for r in range(size):
        for c in range(size):
            cell = player_board[r][c]
            btn = player_buttons[r][c]

            if cell == "X":
                btn.config(bg="red")      # Hit
            elif cell == "O":
                btn.config(bg="green")    # Miss
            elif cell == "S":
                btn.config(bg="gray")     # Player ship visible
            else:
                btn.config(bg="blue")     # Water
