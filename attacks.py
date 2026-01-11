def is_valid_attack(board, row, col):
    return board[row][col] in ("~", "S")


def attack(board, row, col):
    """
    Applies an attack to the board.
    Returns True if hit, False if miss.
    """
    if board[row][col] == "S":
        board[row][col] = "X"
        return True
    if board[row][col] == "~":
        board[row][col] = "O"
        return False

    # Defensive fallback (should never happen)
    return None
