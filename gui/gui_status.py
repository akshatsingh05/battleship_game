# gui_status.py
def update_counters(player_board, computer_board, player_label, computer_label):
    comp_hits = sum(row.count("X") for row in computer_board)
    comp_safe = sum(row.count("S") for row in computer_board)
    computer_label.config(text=f"Hits: {comp_hits} | Remaining: {comp_safe}")

    player_hits = sum(row.count("X") for row in player_board)
    player_safe = sum(row.count("S") for row in player_board)
    player_label.config(text=f"Hits: {player_hits} | Remaining: {player_safe}")

