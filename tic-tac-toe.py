import csv
import random
import pygame
from pygame import mixer

# Set music file path
MUSIC_FILE = "audio/mymusic.mp3"

pygame.mixer.init()

try:
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Couldn't load or play the music file. The game will proceed without music.")
    print("Error details:", e)

def render_gameboard(gameBoard):
    print("\n")
    print('-------------')
    for line in gameBoard:
        print('|', end="")
        for symbol in line:
            print(' ' + symbol + ' |', end="")
        print("\n-------------")
    print("\n")

def winner_check(gameBoard):
    for i in range(len(gameBoard)):
        if all(gameBoard[i][j] == gameBoard[i][0] and gameBoard[i][0] != ' ' for j in range(1, len(gameBoard))):
            return True
        if all(gameBoard[j][i] == gameBoard[0][i] and gameBoard[0][i] != ' ' for j in range(1, len(gameBoard))):
            return True
    if all(gameBoard[i][i] == gameBoard[0][0] and gameBoard[0][0] != ' ' for i in range(1, len(gameBoard))) or all(
            gameBoard[i][len(gameBoard) - i - 1] == gameBoard[0][len(gameBoard) - 1] and gameBoard[0][len(gameBoard) - 1] != ' ' for i in
            range(1, len(gameBoard))):
        return True
    return False

def stalemate_check(gameBoard):
    for row in gameBoard:
        if ' ' in row:
            return False
    return True

def update_hall_of_fame(winner, loser, games_played):
    with open('hall_of_fame.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([winner, loser, games_played])

def game_rules():
    print("\nRULES OF THE GAME:\n")
    print("1️⃣ The game board is a 3x3 or 5x5 grid. Each cell in the grid is referenced by its row and column number (both starting from 0).")
    print("2️⃣ The first player uses 'X', the second player uses 'O' and if there is a third player they use 'Y'.")
    print("3️⃣ Players take turns to place their symbol in an empty cell.")
    print("4️⃣ The first player to align 3 of their symbols in a row, column or diagonal wins.")
    print("5️⃣ If the board is filled and no player has won, the game is a draw.\n")

def control_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play()

def display_hall_of_fame():
    print("\n\n\n******** Hall of Fame *******:\n\n")
    with open('hall_of_fame.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print("Winner: " + row[0] + " - Loser: " + row[1] + " - Number of games: " + row[2])

def start_game(player_list, size):
    gameBoard = [[' '] * size for _ in range(size)]
    game_over = False
    games_played = 1
    current_player_index = 0
    symbols = random.sample(['X', 'O', 'Y'], len(player_list))
    print("\n🎉 It's " + player_list[current_player_index] + "'s turn!\n")
    while not game_over:
        render_gameboard(gameBoard)
        row = int(input("Enter the row number: "))
        col = int(input("Enter the column number: "))
        symbol = symbols[current_player_index]
        if gameBoard[row][col] == ' ':
            gameBoard[row][col] = symbol
            if winner_check(gameBoard):
                render_gameboard(gameBoard)
                print("\n🎉 " + player_list[current_player_index] + " won!\n")
                game_over = True
                losers = [player for player in player_list if player != player_list[current_player_index]]
                for loser in losers:
                    update_hall_of_fame(player_list[current_player_index], loser, games_played)
            elif stalemate_check(gameBoard):
                render_gameboard(gameBoard)
                print("\t😮 It's a draw!\n")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % len(player_list)
                games_played += 1
                print("\n🎉 It's " + player_list[current_player_index] + "'s turn!\n")
        else:
            print("\n\n⚠️ This cell is being used, choose another!\n\n")

def game_menu(player_list, size):
    print("\n\n\n\t --> Welcome to Tic Tac Toe! <--\n\n\n")
    print("1️⃣ Display game rules")
    print("2️⃣ Start a game")
    print("3️⃣ View the Hall of Fame")
    print("4️⃣ Control Music (On/Off)")
    print("5️⃣ Exit the game")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        game_rules()
        game_menu(player_list, size)
    elif choice == 2:
        start_game(player_list, size)
    elif choice == 3:
        display_hall_of_fame()
        game_menu(player_list, size)
    elif choice == 4:
        control_music()
        game_menu(player_list, size)
    elif choice == 5:
        print("\n😢 We are sad to see you leave. See you next time! 😢\n")
        exit()

def main():
    print("\n\n\n\n  HERE WE GO ")
    size = int(input("\nEnter the game board size (3 for 3x3, 5 for 5x5): "))
    players = 3 if size == 5 else 2
    player_list = []
    for i in range(1, players + 1):
        player_list.append(input("Player " + str(i) + ", please enter your name: "))
    game_menu(player_list, size)

if __name__ == "__main__":
    main()
