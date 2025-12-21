# gui.py
import tkinter as tk
from tkinter import messagebox

from board import create_board
from constants import BOARD_SIZE


CELL_SIZE = 60


class BattleshipGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battleship")

        self.player_board = create_board()
        self.computer_board = create_board()

        self.buttons = []
        self.create_grid()

        self.root.mainloop()

    def create_grid(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        for r in range(BOARD_SIZE):
            row_buttons = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(
                    frame,
                    width=4,
                    height=2,
                    font=("Arial", 14),
                    command=lambda r=r, c=c: self.on_cell_click(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def on_cell_click(self, row, col):
        messagebox.showinfo(
            "Cell Clicked",
            f"You clicked row {row}, column {col}"
        )


if __name__ == "__main__":
    BattleshipGUI()
