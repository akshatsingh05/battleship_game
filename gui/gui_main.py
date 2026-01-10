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
        self.root.resizable(True, True)

        # Ship configurations
        self.ship_configs = {
            5: [3, 2],
            7: [4, 3, 2],
            10: [5, 4, 3, 3, 2]
        }

        # Tkinter variables MUST exist before setup_game()
        self.board_size_var = tk.IntVar(value=5)
        self.difficulty_var = tk.StringVar(value="Hard")

        # Runtime state
        self.preview_cells = []
        self.board_size = 5

        #  Show start screen instead of starting game immediately
        self.show_start_screen()
        self.animating = False
        self.root.mainloop()

    # ================= GAME SETUP / RESTART =================

    def setup_game(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Read board size
        self.board_size = self.board_size_var.get()

        # Create boards
        self.player_board = create_board(self.board_size)
        self.computer_board = create_board(self.board_size)

        # Place computer ships only
        place_all_ships(
            self.computer_board,
            self.ship_configs[self.board_size]
        )

        # Placement state
        self.ships_to_place = self.ship_configs[self.board_size]
        self.current_ship_index = 0
        self.current_orientation = "H"
        self.placement_phase = True

        # AI state
        self.ai_state = {
            "mode": "hunt",
            "hunt_cells": generate_hunt_cells(self.board_size),
            "targets": []
        }

        # Build UI
        self.build_ui()
        self.board_size_menu.config(state="normal")
        self.refresh_ui()

        self.status.config(
            text=f"Place ship of size {self.ships_to_place[0]}"
        )

    def restart_game(self):
        self.setup_game()

    # ================= UI =================

    def build_ui(self):
        # Back to Start button (top-right)
        back_to_start_btn = tk.Button(
            self.root,
            text="← Back to Start",
            font=("Arial", 10),
            width=12,
            command=self.back_to_start
        )
        back_to_start_btn.place(relx=0.98, rely=0.03, anchor="ne")

        # Board size selector
        tk.Label(self.root, text="Board Size").pack()
        self.board_size_menu = tk.OptionMenu(
            self.root, self.board_size_var, 5, 7, 10
        )
        self.board_size_menu.pack(pady=4)

        # Difficulty selector
        tk.Label(self.root, text="Difficulty").pack()
        tk.OptionMenu(
            self.root,
            self.difficulty_var,
            "Easy", "Medium", "Hard"
        ).pack(pady=4)

        # Orientation button
        self.orientation_btn = tk.Button(
            self.root,
            text="Orientation: H",
            command=self.toggle_orientation
        )
        self.orientation_btn.pack(pady=5)

        container = tk.Frame(self.root)
        container.pack(padx=10, pady=10)

        # ---- COMPUTER BOARD ----
        comp_frame = tk.Frame(container)
        comp_frame.grid(row=0, column=0, padx=20)

        tk.Label(comp_frame, text="Computer Board", font=("Arial", 14)).pack()
        self.comp_counter = tk.Label(comp_frame, text="")
        self.comp_counter.pack()
        self.comp_result = tk.Label(comp_frame, text="Result: -")
        self.comp_result.pack(pady=5)

        self.computer_buttons = create_computer_board(
            comp_frame, self.on_computer_click, self.board_size
        )
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")

        # ---- PLAYER BOARD ----
        player_frame = tk.Frame(container)
        player_frame.grid(row=0, column=1, padx=20)

        tk.Label(player_frame, text="Your Board", font=("Arial", 14)).pack()
        self.player_counter = tk.Label(player_frame, text="")
        self.player_counter.pack()
        self.player_result = tk.Label(player_frame, text="Enemy Attack: -")
        self.player_result.pack(pady=5)

        self.player_buttons = create_player_board(player_frame, self.board_size)

        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = self.player_buttons[r][c]
                btn.config(
                    command=lambda r=r, c=c: self.on_player_place_click(r, c)
                )
                btn.bind("<Enter>", lambda e, r=r, c=c: self.show_preview(r, c))
                btn.bind("<Leave>", lambda e: self.clear_preview())

        self.status = tk.Label(self.root, text="", font=("Arial", 12))
        self.status.pack(pady=8)

        self.restart_btn = tk.Button(
            self.root, text="Restart Game", command=self.restart_game
        )
        self.restart_btn.pack(pady=4)

        self.finish_btn = tk.Button(
            self.root,
            text="Finish Placement",
            state="disabled",
            command=self.finish_placement
        )
        self.finish_btn.pack(pady=4)

    # ================= PLACEMENT PREVIEW =================

    def show_preview(self, row, col):
        if not self.placement_phase:
            return

        self.clear_preview()
        ship_size = self.ships_to_place[self.current_ship_index]

        valid = can_place_ship(
            self.player_board,
            row,
            col,
            ship_size,
            self.current_orientation
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

    # ================= GAME FLOW =================

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
            self.status.config(
                text="All ships placed. Click 'Finish Placement'."
            )
            self.finish_btn.config(state="normal")
        else:
            self.status.config(
                text=f"Place ship of size {self.ships_to_place[self.current_ship_index]}"
            )

    def finish_placement(self):
        self.placement_phase = False
        self.orientation_btn.config(state="disabled")
        self.finish_btn.config(state="disabled")
        self.board_size_menu.config(state="disabled")
        self.status.config(text="Your turn!")
        self.clear_preview()

        for row in self.player_buttons:
            for btn in row:
                btn.config(state="disabled")
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="normal")

    def on_computer_click(self, row, col):
        if self.animating or self.placement_phase:
            return

        if not is_valid_attack(self.computer_board, row, col):
            return

        self.animating = True  # 🔒 lock input

        hit = attack(self.computer_board, row, col)
        btn = self.computer_buttons[row][col]

        def after_player_animation():
            self.refresh_ui()

            if all_ships_sunk(self.computer_board):
                self.end_game("🎉 You win!")
                return

            self.status.config(text="Computer is thinking…")
            self.root.after(200, self.ai_move)  # hand over to AI

        if hit:
            hit_animation(btn, on_finish=after_player_animation)
            self.comp_result.config(text="Hit!")
        else:
            miss_animation(btn, on_finish=after_player_animation)
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

        def after_ai_animation():
            self.refresh_ui()

            if all_ships_sunk(self.player_board):
                self.end_game("💀 You lost!")
            else:
                self.status.config(text="Your turn")
                self.animating = False  # 🔓 unlock input

        if hit:
            hit_animation(btn, on_finish=after_ai_animation)
        else:
            miss_animation(btn, on_finish=after_ai_animation)



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

        for r in range(self.board_size):
            for c in range(self.board_size):
                cell = self.computer_board[r][c]
                btn = self.computer_buttons[r][c]

                if cell == "S":
                    btn.config(bg="gray")
                elif cell == "X":
                    btn.config(bg="red")
                elif cell == "O":
                    btn.config(bg="green")

                btn.config(state="disabled")

        for row in self.player_buttons:
            for btn in row:
                btn.config(state="disabled")

    def toggle_orientation(self):
        self.current_orientation = "V" if self.current_orientation == "H" else "H"
        self.orientation_btn.config(
            text=f"Orientation: {self.current_orientation}"
        )
    def show_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            center,
            text="🚢 Battleship",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            center,
            text="A Strategy Game",
            font=("Arial", 14)
        )
        subtitle.pack(pady=10)

        start_btn = tk.Button(
            center,
            text="Start Game",
            font=("Arial", 16),
            width=16,
            command=self.show_board_size_screen
        )
        start_btn.pack(pady=30)

    def show_board_size_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Back button (top-right)
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10),
            width=7,
            command=self.show_start_screen
        )
        back_btn.place(relx=0.98, rely=0.05, anchor="ne")

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            center,
            text="Select Board Size",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        for size in (5, 7, 10):
            tk.Radiobutton(
                center,
                text=f"{size} × {size}",
                variable=self.board_size_var,
                value=size,
                font=("Arial", 14),
                indicatoron=0,
                width=14,
                pady=10
            ).pack(pady=6)

        tk.Button(
            center,
            text="Next",
            font=("Arial", 14),
            width=14,
            command=self.show_difficulty_screen
        ).pack(pady=25)
    def show_difficulty_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10),
            width=7,
            command=self.show_board_size_screen
        )
        back_btn.place(relx=0.98, rely=0.05, anchor="ne")

        center = tk.Frame(self.root)
        center.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            center,
            text="Select Difficulty",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        for level in ("Easy", "Medium", "Hard"):
            tk.Radiobutton(
                center,
                text=level,
                variable=self.difficulty_var,
                value=level,
                font=("Arial", 14),
                indicatoron=0,
                width=14,
                pady=10
            ).pack(pady=6)

        tk.Button(
            center,
            text="Start Game",
            font=("Arial", 14),
            width=16,
            command=self.setup_game
        ).pack(pady=25)

    def back_to_start(self):
        # Optional: confirmation (recommended UX)
        # If you don’t want a prompt, remove the next 4 lines.
        from tkinter import messagebox
        if not messagebox.askyesno(
            "Exit Game",
            "Return to start screen? Current game will be lost."
        ):
            return

        # Go back to start screen (full reset)
        self.show_start_screen()
