# gui.py
import tkinter as tk

from board import create_board, all_ships_sunk
from ships import place_all_ships
from attacks import attack, is_valid_attack
from ai import generate_hunt_cells, ai_turn
from constants import BOARD_SIZE


class BattleshipGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battleship")

        # Boards
        self.player_board = create_board()
        self.computer_board = create_board()

        place_all_ships(self.player_board)
        place_all_ships(self.computer_board)

        # AI state (Hard difficulty for now)
        self.ai_state = {
            "mode": "hunt",
            "hunt_cells": generate_hunt_cells(),
            "targets": []
        }

        self.player_buttons = []
        self.computer_buttons = []

        self.create_ui()
        self.update_player_board()
        self.update_counters()

        self.root.mainloop()

    # ---------- UI SETUP ----------

    def create_ui(self):
        container = tk.Frame(self.root)
        container.pack(padx=10, pady=10)

        # ---- COMPUTER BOARD (LEFT) ----
        self.computer_frame = tk.Frame(container)
        self.computer_frame.grid(row=0, column=0, padx=20)

        tk.Label(self.computer_frame, text="Computer Board", font=("Arial", 14)).pack()
        self.comp_counter = tk.Label(self.computer_frame, text="")
        self.comp_counter.pack(pady=2)

        self.comp_result = tk.Label(self.computer_frame, text="Result: -")
        self.comp_result.pack(pady=2)

        comp_grid = tk.Frame(self.computer_frame)
        comp_grid.pack()

        for r in range(BOARD_SIZE):
            row_buttons = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(
                    comp_grid,
                    width=4,
                    height=2,
                    font=("Arial", 14),
                    bg="blue",
                    activebackground="blue",
                    command=lambda r=r, c=c: self.on_computer_click(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_buttons.append(btn)
            self.computer_buttons.append(row_buttons)

        # ---- PLAYER BOARD (RIGHT) ----
        self.player_frame = tk.Frame(container)
        self.player_frame.grid(row=0, column=1, padx=20)

        tk.Label(self.player_frame, text="Your Board", font=("Arial", 14)).pack()
        self.player_counter = tk.Label(self.player_frame, text="")
        self.player_counter.pack(pady=2)

        self.player_result = tk.Label(self.player_frame, text="Enemy Attack: -")
        self.player_result.pack(pady=2)

        player_grid = tk.Frame(self.player_frame)
        player_grid.pack()

        for r in range(BOARD_SIZE):
            row_buttons = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(
                    player_grid,
                    width=4,
                    height=2,
                    font=("Arial", 14),
                    bg="blue",
                    state="disabled"
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_buttons.append(btn)
            self.player_buttons.append(row_buttons)

        # ---- STATUS ----
        self.status = tk.Label(self.root, text="Your turn", font=("Arial", 12), pady=10)
        self.status.pack()

    # ---------- GAME LOGIC ----------

    def on_computer_click(self, row, col):
        if not is_valid_attack(self.computer_board, row, col):
            return

        hit = attack(self.computer_board, row, col)
        btn = self.computer_buttons[row][col]

        if hit:
            btn.config(bg="red", activebackground="red")
            self.comp_result.config(text="Result: Hit!")
        else:
            btn.config(bg="green", activebackground="green")
            self.comp_result.config(text="Result: Miss!")

        btn.config(state="disabled")
        self.update_counters()

        if all_ships_sunk(self.computer_board):
            self.end_game("🎉 You win!")
            return

        # ---- AUTOMATIC AI TURN ----
        self.status.config(text="Computer's turn...")
        self.root.after(300, self.ai_move)

    def ai_move(self):
        self.ai_state = ai_turn(self.player_board, self.ai_state)
        self.update_player_board()
        self.update_counters()

        # Determine AI result text
        if any("X" in row for row in self.player_board):
            self.player_result.config(text="Enemy Attack: Hit!")
        else:
            self.player_result.config(text="Enemy Attack: Miss!")

        if all_ships_sunk(self.player_board):
            self.end_game("💀 You lost!")
        else:
            self.status.config(text="Your turn")

    # ---------- UPDATES ----------

    def update_player_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = self.player_board[r][c]
                btn = self.player_buttons[r][c]

                if cell == "X":
                    btn.config(bg="red")
                elif cell == "O":
                    btn.config(bg="green")
                else:
                    btn.config(bg="blue")

    def update_counters(self):
        comp_hits = sum(row.count("X") for row in self.computer_board)
        comp_safe = sum(row.count("S") for row in self.computer_board)
        self.comp_counter.config(text=f"Hits: {comp_hits} | Remaining: {comp_safe}")

        player_hits = sum(row.count("X") for row in self.player_board)
        player_safe = sum(row.count("S") for row in self.player_board)
        self.player_counter.config(text=f"Hits: {player_hits} | Remaining: {player_safe}")

    def end_game(self, message):
        self.status.config(text=message)

        # Disable all computer buttons
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")


if __name__ == "__main__":
    BattleshipGUI()
