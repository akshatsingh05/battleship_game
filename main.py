from ai import generate_hunt_cells, ai_turn
from board import create_board, print_board, all_ships_sunk
from ships import place_all_ships, player_place_ships
from attacks import player_turn, computer_turn

def choose_difficulty():
    while True:
        print("\nChoose Difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        else:
            print("❌ Invalid choice. Try again.")

def play_game():
    print("\n🚢 Welcome to Battleship!\n")

    player_board = create_board()
    computer_board = create_board()

    player_place_ships(player_board)
    place_all_ships(computer_board)

    difficulty = choose_difficulty()

    ai_state = {
        "mode": "hunt",
        "hunt_cells": generate_hunt_cells(),
        "targets": []
        }



    while True:
        print("\n🧍 Your Board:")
        print_board(player_board, hide_ships=False)

        print("\n💻 Computer Board:")
        print_board(computer_board, hide_ships=True)

        print("\n🎯 Your turn!")
        if not player_turn(computer_board):
            print("\n🚪 You exited the game.")
            break

        if all_ships_sunk(computer_board):
            print("\n🎉 YOU WIN! All enemy ships sunk!")

            print("\n🧍 Final Player Board:")
            print_board(player_board, hide_ships=False)

            print("\n💻 Final Computer Board:")
            print_board(computer_board, hide_ships=False)

            break

        print("\n🤖 Computer's turn...")

        if difficulty == "easy":
            computer_turn(player_board)

        elif difficulty == "medium":

            ai_state["mode"] = "hunt"
            ai_state = ai_turn(player_board, ai_state)

        elif difficulty == "hard":
            ai_state = ai_turn(player_board, ai_state)

        if all_ships_sunk(player_board):
            print("\n💀 YOU LOST! All your ships have sunk.")

            print("\n🧍 Final Player Board:")
            print_board(player_board, hide_ships=False)

            print("\n💻 Final Computer Board:")
            print_board(computer_board, hide_ships=False)

            break


if __name__ == "__main__":
    play_game()
