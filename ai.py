import random
from attacks import is_valid_attack, attack

# ---------- HUNT GRID ----------

def generate_hunt_cells(board_size):
    cells = []
    for r in range(board_size):
        for c in range(board_size):
            if (r + c) % 2 == 0:
                cells.append((r, c))
    random.shuffle(cells)
    return cells


def get_adjacent_cells(row, col, board_size):
    candidates = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]

    return [
        (r, c)
        for r, c in candidates
        if 0 <= r < board_size and 0 <= c < board_size
    ]


# ---------- AI TURN ----------

def ai_turn(player_board, ai_state, difficulty):
    board_size = len(player_board)

    # ---------------- EASY ----------------
    if difficulty == "Easy":
        available = [
            (r, c)
            for r in range(board_size)
            for c in range(board_size)
            if is_valid_attack(player_board, r, c)
        ]

        if not available:
            return ai_state

        r, c = random.choice(available)
        attack(player_board, r, c)
        return ai_state

    # ---------------- TARGET MODE (HARD ONLY) ----------------
    if difficulty == "Hard" and ai_state["mode"] == "target":
        while ai_state["targets"]:
            r, c = ai_state["targets"].pop(0)

            if not is_valid_attack(player_board, r, c):
                continue

            hit = attack(player_board, r, c)

            if hit:
                for cell in get_adjacent_cells(r, c, board_size):
                    if cell not in ai_state["targets"]:
                        ai_state["targets"].append(cell)

            return ai_state

        ai_state["mode"] = "hunt"

    # ---------------- HUNT MODE (MEDIUM + HARD) ----------------
    while ai_state["hunt_cells"]:
        r, c = ai_state["hunt_cells"].pop()

        if not is_valid_attack(player_board, r, c):
            continue

        hit = attack(player_board, r, c)

        if hit and difficulty == "Hard":
            ai_state["mode"] = "target"
            ai_state["targets"] = get_adjacent_cells(r, c, board_size)

        return ai_state

    # Safety reset
    ai_state["hunt_cells"] = generate_hunt_cells(board_size)
    return ai_state
