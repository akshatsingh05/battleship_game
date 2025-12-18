# ai.py
import random
from constants import BOARD_SIZE
from attacks import is_valid_attack, attack

# ---------- Helpers ----------

def generate_hunt_cells():
    cells = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if (r + c) % 2 == 0:
                cells.append((r, c))
    random.shuffle(cells)
    return cells


def get_adjacent_cells(row, col):
    candidates = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]
    valid = []
    for r, c in candidates:
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            valid.append((r, c))
    return valid


# ---------- AI Turn ----------

def ai_turn(player_board, ai_state):
    """
    Performs one AI turn using Hunt + Target modes.
    Returns updated ai_state.
    """

    # -------- TARGET MODE --------
    if ai_state["mode"] == "target":
        while ai_state["targets"]:
            row, col = ai_state["targets"].pop(0)

            if not is_valid_attack(player_board, row, col):
                continue

            hit = attack(player_board, row, col)
            print(f"\n🤖 Computer attacks ({row}, {col})")

            if hit:
                print("💥 Computer HIT your ship!")
                # Add new adjacent cells
                for cell in get_adjacent_cells(row, col):
                    if cell not in ai_state["targets"]:
                        ai_state["targets"].append(cell)
            else:
                print("🌊 Computer MISSED!")

            return ai_state

        # No more target cells → back to hunt
        ai_state["mode"] = "hunt"

    # -------- HUNT MODE --------
    while ai_state["hunt_cells"]:
        row, col = ai_state["hunt_cells"].pop()

        if not is_valid_attack(player_board, row, col):
            continue

        hit = attack(player_board, row, col)
        print(f"\n🤖 Computer attacks ({row}, {col})")

        if hit:
            print("💥 Computer HIT your ship!")
            ai_state["mode"] = "target"
            ai_state["targets"] = get_adjacent_cells(row, col)
        else:
            print("🌊 Computer MISSED!")

        return ai_state

    return ai_state
