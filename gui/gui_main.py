import tkinter as tk

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

    # ================= GAME SETUP / RESTART =================

    def setup_game(self):
        self.animating = False

        for widget in self.root.winfo_children():
            widget.destroy()

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
            command=self.back_to_start
        ).place(relx=0.98, rely=0.03, anchor="ne")

        tk.Label(self.root, text="Board Size").pack()
        self.board_size_menu = tk.OptionMenu(
            self.root, self.board_size_var, 5, 7, 10
        )
        self.board_size_menu.pack()

        tk.Label(self.root, text="Difficulty").pack()
        tk.OptionMenu(
            self.root, self.difficulty_var,
            "Easy", "Medium", "Hard"
        ).pack()

        self.orientation_btn = tk.Button(
            self.root, text="Orientation: H",
            command=self.toggle_orientation
        )
        self.orientation_btn.pack(pady=5)

        container = tk.Frame(self.root)
        container.pack(pady=10)

        # --- COMPUTER BOARD ---
        comp = tk.Frame(container)
        comp.grid(row=0, column=0, padx=20)

        tk.Label(comp, text="Computer Board").pack()
        self.comp_counter = tk.Label(comp, text="")
        self.comp_counter.pack()
        self.comp_result = tk.Label(comp, text="Result: -")
        self.comp_result.pack()

        self.computer_buttons = create_computer_board(
            comp, self.on_computer_click, self.board_size
        )
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")

        # --- PLAYER BOARD ---
        player = tk.Frame(container)
        player.grid(row=0, column=1, padx=20)

        tk.Label(player, text="Your Board").pack()
        self.player_counter = tk.Label(player, text="")
        self.player_counter.pack()
        self.player_result = tk.Label(player, text="Enemy Attack: -")
        self.player_result.pack()

        self.player_buttons = create_player_board(player, self.board_size)

        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = self.player_buttons[r][c]
                btn.config(
                    command=lambda r=r, c=c: self.on_player_place_click(r, c)
                )
                btn.bind("<Enter>", lambda e, r=r, c=c: self.show_preview(r, c))
                btn.bind("<Leave>", lambda e: self.clear_preview())

        self.status = tk.Label(self.root, text="")
        self.status.pack(pady=8)

        tk.Button(
            self.root, text="Restart Game",
            command=self.restart_game
        ).pack()

        self.finish_btn = tk.Button(
            self.root, text="Finish Placement",
            state="disabled",
            command=self.finish_placement
        )
        self.finish_btn.pack()

    # ================= PLACEMENT =================

    def finish_placement(self):
        if self.animating:
            return

        self.animating = True
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

        self.status.config(text="Your turn")
        self.animating = False

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

        if hit:
            hit_animation(btn, on_finish=after_player)
            self.comp_result.config(text="Hit!")
        else:
            miss_animation(btn, on_finish=after_player)
            self.comp_result.config(text="Miss!")

        btn.config(state="disabled")

    def ai_move(self):
        difficulty = self.difficulty_var.get()

        self.ai_state, move, hit = ai_turn(
            self.player_board, self.ai_state, difficulty
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
                self.status.config(text="Your turn")
                self.animating = False

        if hit:
            hit_animation(btn, on_finish=after_ai)
        else:
            miss_animation(btn, on_finish=after_ai)

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

        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")
        for row in self.player_buttons:
            for btn in row:
                btn.config(state="disabled")

    def toggle_orientation(self):
        self.current_orientation = "V" if self.current_orientation == "H" else "H"
        self.orientation_btn.config(
            text=f"Orientation: {self.current_orientation}"
        )

    # ================= START SCREENS =================

    def show_start_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="🚢 Battleship", font=("Arial", 30)).pack(pady=20)
        tk.Button(
            center, text="Start Game",
            command=self.show_board_size_screen
        ).pack(pady=30)

    def show_board_size_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Select Board Size").pack()
        for size in (5, 7, 10):
            tk.Radiobutton(
                center, text=f"{size} × {size}",
                variable=self.board_size_var,
                value=size
            ).pack()

        tk.Button(
            center, text="Next",
            command=self.show_difficulty_screen
        ).pack(pady=20)

    def show_difficulty_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Select Difficulty").pack()
        for level in ("Easy", "Medium", "Hard"):
            tk.Radiobutton(
                center, text=level,
                variable=self.difficulty_var,
                value=level
            ).pack()

        tk.Button(
            center, text="Start Game",
            command=self.setup_game
        ).pack(pady=20)

    def back_to_start(self):
        self.animating = False
        self.show_start_screen()
