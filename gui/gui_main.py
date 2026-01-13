import tkinter as tk
from tkinter import messagebox

from board import create_board, all_ships_sunk
from ships import place_all_ships, can_place_ship
from attacks import attack, is_valid_attack
from ai import generate_hunt_cells, ai_turn

from gui.gui_boards import (
    create_computer_board,
    create_player_board,
    update_player_board
)
from gui.gui_status import update_counters
from gui.animations import hit_animation, miss_animation


class BattleshipGUI:

    # ================= INITIALIZATION =================

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battleship")
        self.root.state("zoomed")

        self.ship_configs = {
            5: [3, 2],
            7: [4, 3, 2],
            10: [5, 4, 3, 3, 2]
        }

        self.board_size_var = tk.IntVar(value=5)
        self.difficulty_var = tk.StringVar(value="Hard")

        self.preview_cells = []
        self.animating = False
        self.board_size = 5

        self.show_start_screen()
        self.root.mainloop()

    # ================= GAME SETUP =================

    def setup_game(self):
        self.animating = False
        self.preview_cells.clear()

        for w in self.root.winfo_children():
            w.destroy()

        self.board_size = self.board_size_var.get()

        self.player_board = create_board(self.board_size)
        self.computer_board = create_board(self.board_size)

        place_all_ships(
            self.computer_board,
            self.ship_configs[self.board_size]
        )

        self.ships_to_place = self.ship_configs[self.board_size]
        self.current_ship_index = 0
        self.current_orientation = "H"
        self.placement_phase = True

        self.ai_state = {
            "mode": "hunt",
            "hunt_cells": generate_hunt_cells(self.board_size),
            "targets": []
        }

        self.build_ui()
        self.refresh_ui()

        self.status.config(
            text=f"Place ship of size {self.ships_to_place[0]}"
        )

    def restart_game(self):
        self.animating = False
        self.setup_game()

    # ================= UI =================

    def build_ui(self):
        tk.Button(
            self.root,
            text="← Back to Start",
            font=("Arial", 12),
            command=self.back_to_start
        ).place(relx=0.98, rely=0.03, anchor="ne")

        tk.Label(self.root, text="Board Size", font=("Arial", 12)).pack(pady=4)
        tk.OptionMenu(self.root, self.board_size_var, 5, 7, 10).pack()

        tk.Label(self.root, text="Difficulty", font=("Arial", 12)).pack(pady=4)
        tk.OptionMenu(
            self.root,
            self.difficulty_var,
            "Easy", "Medium", "Hard"
        ).pack()

        self.orientation_btn = tk.Button(
            self.root,
            text="Orientation: H",
            font=("Arial", 12),
            command=self.toggle_orientation
        )
        self.orientation_btn.pack(pady=8)

        container = tk.Frame(self.root)
        container.pack(pady=15)

        # --- COMPUTER BOARD ---
        comp = tk.Frame(container)
        comp.grid(row=0, column=0, padx=30)

        tk.Label(comp, text="Computer Board", font=("Arial", 16)).pack()
        self.comp_counter = tk.Label(comp, text="", font=("Arial", 11))
        self.comp_counter.pack()
        self.comp_result = tk.Label(comp, text="Result: -", font=("Arial", 11))
        self.comp_result.pack(pady=5)

        self.computer_buttons = create_computer_board(
            comp, self.on_computer_click, self.board_size
        )
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")

        # --- PLAYER BOARD ---
        player = tk.Frame(container)
        player.grid(row=0, column=1, padx=30)

        tk.Label(player, text="Your Board", font=("Arial", 16)).pack()
        self.player_counter = tk.Label(player, text="", font=("Arial", 11))
        self.player_counter.pack()
        self.player_result = tk.Label(player, text="Enemy Attack: -", font=("Arial", 11))
        self.player_result.pack(pady=5)

        self.player_buttons = create_player_board(player, self.board_size)

        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = self.player_buttons[r][c]
                btn.config(command=lambda r=r, c=c: self.on_player_place_click(r, c))
                btn.bind("<Enter>", lambda e, r=r, c=c: self.show_preview(r, c))
                btn.bind("<Leave>", lambda e: self.clear_preview())

        self.status = tk.Label(self.root, text="", font=("Arial", 14))
        self.status.pack(pady=10)

        tk.Button(
            self.root,
            text="Restart Game",
            font=("Arial", 12),
            width=18,
            command=self.restart_game
        ).pack(pady=(5, 2))

        self.finish_btn = tk.Button(
            self.root,
            text="Finish Placement",
            font=("Arial", 12),
            width=18,
            state="disabled",
            command=self.finish_placement
        )
        self.finish_btn.pack(pady=(2, 10))

    # ================= PLACEMENT PREVIEW =================

    def show_preview(self, row, col):
        if not self.placement_phase:
            return

        self.clear_preview()
        ship_size = self.ships_to_place[self.current_ship_index]

        valid = can_place_ship(
            self.player_board, row, col, ship_size, self.current_orientation
        )
        color = "lightgreen" if valid else "pink"

        cells = (
            [(row, col + i) for i in range(ship_size)]
            if self.current_orientation == "H"
            else [(row + i, col) for i in range(ship_size)]
        )

        for r, c in cells:
            if 0 <= r < self.board_size and 0 <= c < self.board_size:
                self.player_buttons[r][c].config(bg=color)
                self.preview_cells.append((r, c))

    def clear_preview(self):
        for r, c in self.preview_cells:
            cell = self.player_board[r][c]
            self.player_buttons[r][c].config(
                bg="gray" if cell == "S" else "blue"
            )
        self.preview_cells.clear()

    # ================= PLACEMENT =================

    def on_player_place_click(self, row, col):
        if not self.placement_phase:
            return

        self.clear_preview()
        ship_size = self.ships_to_place[self.current_ship_index]

        if not can_place_ship(
            self.player_board, row, col, ship_size, self.current_orientation
        ):
            self.status.config(text="Invalid placement!")
            return

        if self.current_orientation == "H":
            for i in range(ship_size):
                self.player_board[row][col + i] = "S"
        else:
            for i in range(ship_size):
                self.player_board[row + i][col] = "S"

        self.current_ship_index += 1
        self.refresh_ui()

        if self.current_ship_index == len(self.ships_to_place):
            self.status.config(text="All ships placed. Click Finish Placement.")
            self.finish_btn.config(state="normal")
        else:
            self.status.config(
                text=f"Place ship of size {self.ships_to_place[self.current_ship_index]}"
            )

    def finish_placement(self):
        self.placement_phase = False
        self.orientation_btn.config(state="disabled")
        self.finish_btn.config(state="disabled")
        self.clear_preview()

        for row in self.player_buttons:
            for btn in row:
                btn.config(state="disabled")
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="normal")

        self.status.config(text="Your turn!")

    # ================= GAME FLOW =================

    def on_computer_click(self, row, col):
        if self.animating or self.placement_phase:
            return
        if not is_valid_attack(self.computer_board, row, col):
            return

        self.animating = True
        hit = attack(self.computer_board, row, col)
        btn = self.computer_buttons[row][col]

        def after_player():
            self.refresh_ui()
            if all_ships_sunk(self.computer_board):
                self.end_game("🎉 You win!")
            else:
                self.ai_move()

        (hit_animation if hit else miss_animation)(btn, on_finish=after_player)
        self.comp_result.config(text="Hit!" if hit else "Miss!")
        btn.config(state="disabled")

    def ai_move(self):
        self.ai_state, move, hit = ai_turn(
            self.player_board, self.ai_state, self.difficulty_var.get()
        )

        if move is None:
            self.animating = False
            return

        r, c = move
        btn = self.player_buttons[r][c]

        def after_ai():
            self.refresh_ui()
            if all_ships_sunk(self.player_board):
                self.end_game("💀 You lost!")
            else:
                self.status.config(text="Your turn!")
                self.animating = False

        (hit_animation if hit else miss_animation)(btn, on_finish=after_ai)

    # ================= HELPERS =================

    def refresh_ui(self):
        update_player_board(self.player_board, self.player_buttons)
        update_counters(
            self.player_board,
            self.computer_board,
            self.player_counter,
            self.comp_counter
        )

    def end_game(self, message):
        self.animating = False
        self.status.config(text=message)
        for row in self.computer_buttons + self.player_buttons:
            for btn in row:
                btn.config(state="disabled")

    def toggle_orientation(self):
        self.current_orientation = "V" if self.current_orientation == "H" else "H"
        self.orientation_btn.config(text=f"Orientation: {self.current_orientation}")

    # ================= START SCREENS =================

    def show_start_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center, text="🚢 Battleship",
            font=("Arial", 34, "bold")
        ).pack(pady=20)

        tk.Button(
            center,
            text="Start Game",
            font=("Arial", 18),
            width=18,
            height=2,
            command=self.show_board_size_screen
        ).pack(pady=30)

    def show_board_size_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center, text="Select Board Size",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        for size in (5, 7, 10):
            tk.Radiobutton(
                center,
                text=f"{size} × {size}",
                variable=self.board_size_var,
                value=size,
                indicatoron=0,
                font=("Arial", 16),
                width=16,
                pady=8
            ).pack(pady=6)

        tk.Button(
            center,
            text="Next",
            font=("Arial", 16),
            width=16,
            command=self.show_difficulty_screen
        ).pack(pady=25)

    def show_difficulty_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center, text="Select Difficulty",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        for level in ("Easy", "Medium", "Hard"):
            tk.Radiobutton(
                center,
                text=level,
                variable=self.difficulty_var,
                value=level,
                indicatoron=0,
                font=("Arial", 16),
                width=16,
                pady=8
            ).pack(pady=6)

        tk.Button(
            center,
            text="Start Game",
            font=("Arial", 16),
            width=18,
            command=self.setup_game
        ).pack(pady=30)

    def back_to_start(self):
        if not messagebox.askyesno(
            "Exit Game",
            "Return to start screen? Current game will be lost."
        ):
            return
        self.animating = False
        self.show_start_screen()
