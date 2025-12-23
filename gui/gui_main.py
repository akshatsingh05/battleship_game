import tkinter as tk

from board import create_board, all_ships_sunk
from ships import place_all_ships
from attacks import attack, is_valid_attack
from ai import generate_hunt_cells, ai_turn

from gui.gui_boards import (
    create_computer_board,
    create_player_board,
    update_player_board
)
from gui.gui_status import update_counters
