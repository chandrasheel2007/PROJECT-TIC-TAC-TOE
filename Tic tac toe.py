import os
import argparse

# ----------------------------- Argument Parser -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Play Tic Tac Toe in the terminal!")
    parser.add_argument(
        "--player",
        choices=["X", "O"],
        help="Choose which player goes first (X or O)."
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show previous game results and exit."
    )
    return parser.parse_args()

# ----------------------------- Utility Functions -----------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 5)
    print("\n")

def check_win(board, player):
    # Check rows, columns, and diagonals for win
    for i in range(3):
        if all(cell == player for cell in board[i]) or all(row[i] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_tie(board):
    return all(cell != " " for row in board for cell in row)

def save_game_result(winner, board):
    with open("game_history.txt", "a") as file:
        file.write(f"Winner: {winner}\n")
        for row in board:
            file.write(" | ".join(row) + "\n")
        file.write("-" * 10 + "\n")

def show_game_history():
    try:
        with open("game_history.txt", "r") as file:
            print("\n📜 Game History:\n")
            print(file.read())
    except FileNotFoundError:
        print("No game history found.")

# ----------------------------- Main Game Logic -----------------------------
def main():
    args = parse_args()

    if args.history:
        show_game_history()
        return

    current_player = args.player if args.player else "X"

    while True:
        board = [[" " for _ in range(3)] for _ in range(3)]
        winner = None

        while True:
            clear_screen()
            print(f"Player {current_player}'s turn")
            print_board(board)

            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter col (0-2): "))

                if not (0 <= row <= 2 and 0 <= col <= 2):
                    print("⚠️ Position out of bounds. Please use numbers 0 to 2.")
                    continue

                if board[row][col] != " ":
                    print("❌ Cell already taken! Try again.")
                    continue

                board[row][col] = current_player

                if check_win(board, current_player):
                    winner = current_player
                    break
                elif check_tie(board):
                    break

                current_player = "O" if current_player == "X" else "X"

            except ValueError:
                print("❗ Invalid input. Please enter a number.")
            except IndexError:
                print("❗ Invalid position. Enter numbers between 0 and 2.")

        clear_screen()
        print_board(board)
        if winner:
            print(f"🎉 Player {winner} wins!")
        else:
            print("It's a tie!")

        save_game_result(winner or "Tie", board)

        play_again = input("Play again? (y/n): ").lower()
        if play_again != 'y':
            break

# ----------------------------- Run the Game -----------------------------
if __name__ == "__main__":
    main()
