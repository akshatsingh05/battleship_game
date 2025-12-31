def create_board(size):
    return [["~"] * size for _ in range(size)]


def all_ships_sunk(board):
    for row in board:
        if "S" in row:
            return False
    return True
