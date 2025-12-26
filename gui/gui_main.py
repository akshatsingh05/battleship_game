import tkinter as tk

from board import create_board, all_ships_sunk
from ships import place_all_ships
from attacks import attack, is_valid_attack
from ai import generate_hunt_cells, ai_turn
from ships import can_place_ship

from gui.gui_boards import (
    create_computer_board,
    create_player_board,
    update_player_board
)
from gui.gui_status import update_counters


class BattleshipGUI:
    def __init__(self):
        self.ships_to_place = [3, 2]   # ship sizes
        self.current_ship_index = 0
        self.current_orientation = "H"
        self.placement_phase = True


        self.root = tk.Tk()
        self.root.title("Battleship")

        # Boards
        self.player_board = create_board()
        self.computer_board = create_board()

        place_all_ships(self.computer_board)

        # AI state (Hard mode)
        self.ai_state = {
            "mode": "hunt",
            "hunt_cells": generate_hunt_cells(),
            "targets": []
        }

        self.player_buttons = []
        self.computer_buttons = []

        self.build_ui()
        self.refresh_ui()

        self.root.mainloop()

    # ---------------- UI ----------------

    def build_ui(self):
        self.orientation_btn = tk.Button(
        self.root,
        text="Orientation: H",
        command=self.toggle_orientation
        )
        self.orientation_btn.pack(pady=5)

        container = tk.Frame(self.root)
        container.pack(padx=10, pady=10)

        # ---- COMPUTER BOARD (LEFT) ----
        comp_frame = tk.Frame(container)
        comp_frame.grid(row=0, column=0, padx=20)

        tk.Label(comp_frame, text="Computer Board", font=("Arial", 14)).pack()
        self.comp_counter = tk.Label(comp_frame, text="")
        self.comp_counter.pack()

        self.comp_result = tk.Label(comp_frame, text="Result: -")
        self.comp_result.pack(pady=5)

        self.computer_buttons = create_computer_board(
            comp_frame, self.on_computer_click
        )

        # ---- PLAYER BOARD (RIGHT) ----
        player_frame = tk.Frame(container)
        player_frame.grid(row=0, column=1, padx=20)

        tk.Label(player_frame, text="Your Board", font=("Arial", 14)).pack()
        self.player_counter = tk.Label(player_frame, text="")
        self.player_counter.pack()

        self.player_result = tk.Label(player_frame, text="Enemy Attack: -")
        self.player_result.pack(pady=5)

        self.player_buttons = create_player_board(player_frame)
        for r in range(len(self.player_buttons)):
            for c in range(len(self.player_buttons[r])):
                self.player_buttons[r][c].config(
                    command=lambda r=r, c=c: self.on_player_place_click(r, c)
                )


        self.status = tk.Label(self.root, text="Your turn", font=("Arial", 12))
        self.status.pack(pady=10)

        self.restart_btn = tk.Button(
        self.root,
        text="Restart Game",
        font=("Arial", 11),
        command=self.restart_game
        )
        self.restart_btn.pack(pady=5)

        self.finish_btn = tk.Button(
            self.root,
            text="Finish Placement",
            state="disabled",   # disabled until all ships placed
            command=self.finish_placement
        )
        self.finish_btn.pack(pady=5)



    # ---------------- GAME FLOW ----------------

    def on_computer_click(self, row, col):
        if not is_valid_attack(self.computer_board, row, col):
            return

        hit = attack(self.computer_board, row, col)
        btn = self.computer_buttons[row][col]

        if hit:
            btn.config(bg="red")
            self.comp_result.config(text="Result: Hit!")
        else:
            btn.config(bg="green")
            self.comp_result.config(text="Result: Miss!")

        btn.config(state="disabled")
        self.refresh_ui()

        if all_ships_sunk(self.computer_board):
            self.end_game("🎉 You win!")
            return

        self.status.config(text="Computer's turn...")
        self.root.after(300, self.ai_move)

    def ai_move(self):
        self.ai_state = ai_turn(self.player_board, self.ai_state)
        update_player_board(self.player_board, self.player_buttons)
        self.refresh_ui()

        if all_ships_sunk(self.player_board):
            self.end_game("💀 You lost!")
        else:
            self.status.config(text="Your turn")

    # ---------------- HELPERS ----------------

    def refresh_ui(self):
        update_player_board(self.player_board, self.player_buttons)
        update_counters(
            self.player_board,
            self.computer_board,
            self.player_counter,
            self.comp_counter
        )

    def end_game(self, message):
        self.status.config(text=message)
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")
                    
    def restart_game(self):
        # Reset boards
        self.player_board = create_board()
        self.computer_board = create_board()

        place_all_ships(self.player_board)
        place_all_ships(self.computer_board)

        # Reset AI
        self.ai_state = {
            "mode": "hunt",
            "hunt_cells": generate_hunt_cells(),
            "targets": []
        }

        # Reset computer board buttons
        for row in self.computer_buttons:
            for btn in row:
                btn.config(bg="blue", state="normal")

        # Reset player board buttons
        for row in self.player_buttons:
            for btn in row:
                btn.config(bg="blue")

        # Reset labels
        self.comp_result.config(text="Result: -")
        self.player_result.config(text="Enemy Attack: -")
        self.status.config(text="Your turn")

        self.refresh_ui()

    def toggle_orientation(self):
        self.current_orientation = "V" if self.current_orientation == "H" else "H"
        self.orientation_btn.config(text=f"Orientation: {self.current_orientation}")

    def on_player_place_click(self, row, col):
        if not self.placement_phase:
            return

        ship_size = self.ships_to_place[self.current_ship_index]

        if not can_place_ship(
            self.player_board,
            row,
            col,
            ship_size,
            self.current_orientation
        ):
            self.status.config(text="Invalid placement!")
            return

        # Place ship
        if self.current_orientation == "H":
            for i in range(ship_size):
                self.player_board[row][col + i] = "S"
        else:
            for i in range(ship_size):
                self.player_board[row + i][col] = "S"

        self.current_ship_index += 1
        self.refresh_ui()

        if self.current_ship_index == len(self.ships_to_place):
            # Ensure placement is still active
            self.placement_phase = True
            self.status.config(text="All ships placed. Click 'Finish Placement'.")
            self.finish_btn.config(state="normal")
        else:
            self.status.config(
                text=f"Place ship of size {self.ships_to_place[self.current_ship_index]}"
            )


    def finish_placement(self):
        # End placement phase
        self.placement_phase = False

        # Update UI state
        self.status.config(text="Placement complete. Your turn!")
        self.orientation_btn.config(state="disabled")
        self.finish_btn.config(state="disabled")

        # Disable player board clicks
        for row in self.player_buttons:
            for btn in row:
                btn.config(state="disabled")


