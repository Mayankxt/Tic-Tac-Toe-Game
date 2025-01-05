import os

def display_board(board):
    print("\nCurrent Board:")
    print("+---+---+---+")
    for i in range(0, 9, 3):
        print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |")
        print("+---+---+---+")

def save_game_state(board, player_turn):
    with open("data/game_state.txt", "w") as file:
        for i in range(0, 9, 3):
            file.write(",".join(board[i:i+3]) + "\n")
        file.write(f"Player Turn: {player_turn}\n")
    print("Game state saved!")

def load_game_state():
    if not os.path.exists("data/game_state.txt"):
        return None, None

    with open("data/game_state.txt", "r") as file:
        lines = file.readlines()
        board = [cell for line in lines[:3] for cell in line.strip().split(",")]
        player_turn = int(lines[3].strip().split(": ")[1])
    return board, player_turn

def check_winner(board):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "-":
            return board[combo[0]]
    return None

def is_board_full(board):
    return "-" not in board

def play_game():
    if not os.path.exists("data"):
        os.makedirs("data")

    print("Welcome to Tic Tac Toe!")
    print("Player 1: X\nPlayer 2: O\n")

    board, player_turn = load_game_state()
    if board:
        print("Resuming saved game...")
    else:
        board = ["-"] * 9
        player_turn = 1

    while True:
        display_board(board)
        print(f"Player {player_turn}, it's your turn (1-9):")

        try:
            move = int(input().strip()) - 1
            if move < 0 or move >= 9 or board[move] != "-":
                print("Invalid move. Try again.")
                continue
        except ValueError:
            print("Please enter a number between 1 and 9.")
            continue

        board[move] = "X" if player_turn == 1 else "O"

        winner = check_winner(board)
        if winner:
            display_board(board)
            print(f"Player {player_turn} wins! Congratulations!")
            if os.path.exists("data/game_state.txt"):
                os.remove("data/game_state.txt")
            break

        if is_board_full(board):
            display_board(board)
            print("It's a tie!")
            if os.path.exists("data/game_state.txt"):
                os.remove("data/game_state.txt")
            break

        player_turn = 1 if player_turn == 2 else 2
        save_game_state(board, player_turn)

if __name__ == "__main__":
    play_game()
