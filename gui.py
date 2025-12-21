# gui.py
import tkinter as tk
from tkinter import messagebox

from board import create_board
from ships import place_all_ships
from attacks import attack, is_valid_attack
from constants import BOARD_SIZE


class BattleshipGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battleship")

        # Boards
        self.player_board = create_board()
        self.computer_board = create_board()
        place_all_ships(self.computer_board)

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
                    bg="blue",          # 🔵 default color
                    activebackground="blue",
                    command=lambda r=r, c=c: self.on_cell_click(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def on_cell_click(self, row, col):
        # Prevent invalid attacks
        if not is_valid_attack(self.computer_board, row, col):
            return

        hit = attack(self.computer_board, row, col)
        btn = self.buttons[row][col]

        if hit:
            btn.config(bg="red", activebackground="red")     # 🔴 Hit
        else:
            btn.config(bg="green", activebackground="green") # 🟢 Miss

        btn.config(state="disabled")


if __name__ == "__main__":
    BattleshipGUI()
