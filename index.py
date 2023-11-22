import csv
import random
import pygame
from pygame import mixer
import pygame
pygame.mixer.init()
pygame.mixer.music.load("mymusic.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy(): 
    pygame.time.Clock().tick(10)

# Set music file path
MUSIC_FILE = "audio/mymusic.mp3"

# Function to display the game board
def render_gameboard(gameBoard):
    print("\n")
    print('-------------')
    for line in gameBoard:
        print('|', end="")
        for symbol in line:
            print(' ' + symbol + ' |', end="")
        print("\n-------------")
    print("\n")

# Function to verify if a player has won
def winner_check(gameBoard):
    for i in range(len(gameBoard)):
        if gameBoard[i][0] == gameBoard[i][1] == gameBoard[i][2] != ' ' or gameBoard[0][i] == gameBoard[1][i] == gameBoard[2][i] != ' ':
            return True
    if gameBoard[0][0] == gameBoard[1][1] == gameBoard[2][2] != ' ' or gameBoard[0][2] == gameBoard[1][1] == gameBoard[2][0] != ' ':
        return True
    return False

# Function to verify if the game is a draw
def stalemate_check(gameBoard):
    for row in gameBoard:
        if ' ' in row:
            return False
    return True

# Function to update the "Hall of Fame"
def update_hall_of_fame(winner, loser, games_played):
    with open('hall_of_fame.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([winner, loser, games_played])

# Function to display the game rules
def game_rules():
    print("\nRULES OF THE GAME:\n")
    print("1️⃣ The game board is a 3x3 or 5x5 grid. Each cell in the grid is referenced by its row and column number (both starting from 0).")
    print("2️⃣ The first player uses 'X', the second player uses 'O' and if there is a third player they use 'Y'.")
    print("3️⃣ Players take turns to place their symbol in an empty cell.")
    print("4️⃣ The first player to align 3 of their symbols in a row, column or diagonal wins.")
    print("5️⃣ If the board is filled and no player has won, the game is a draw.\n")

# Function to display the game menu
def game_menu(player_list):
    print("\n\n\n\t --> Welcome to Tic Tac Toe! <--\n\n\n")
    print("1️⃣ Display game rules")
    print("2️⃣ Start a game")
    print("3️⃣ View the Hall of Fame")
    print("4️⃣ Exit the game")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        game_rules()
        game_menu(player_list)
    elif choice == 2:
        start_game(player_list)
    elif choice == 3:
        display_hall_of_fame()
        game_menu(player_list)
    elif choice == 4:
        print("\n😢 We are sad to see you leave. See you next time! 😢\n")
        exit()

# Function to display the "Hall of Fame"
def display_hall_of_fame():
    print("\n\n\n🏆 Hall of Fame 🏆:\n\n")
    with open('hall_of_fame.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print("Winner: " + row[0] + " - Loser: " + row[1] + " - Number of games: " + row[2])

# Function to start a game
def start_game(player_list):
    size = int(input("\nEnter the game board size (3 for 3x3, 5 for 5x5): "))
    gameBoard = [[' ']*size for _ in range(size)]
    game_over = False
    games_played = 1
    current_player = random.choice(player_list)
    print("\n🎉 It's " + current_player + "'s turn!\n")
    while not game_over:
        render_gameboard(gameBoard)
        row = int(input("Enter the row number: "))
        col = int(input("Enter the column number: "))
        symbol = 'X' if current_player == player_list[0] else 'O' if current_player == player_list[1] else 'Y'
        if gameBoard[row][col] == ' ':
            gameBoard[row][col] = symbol
            if winner_check(gameBoard):
                render_gameboard(gameBoard)
                print("\n🎉 " + current_player + " won!\n")
                game_over = True
                losers = [player for player in player_list if player != current_player]
                for loser in losers:
                    update_hall_of_fame(current_player, loser, games_played)
            elif stalemate_check(gameBoard):
                render_gameboard(gameBoard)
                print("\t😮 It's a draw!\n")
                game_over = True
            else:
                player_list.remove(current_player)
                player_list.append(current_player)
                current_player = player_list[0]
                games_played += 1
        else:
            print("\n\n⚠️ This cell is already occupied, choose another cell!\n\n")
    game_menu(player_list)

# Main function to run the game
def main():
    print("\n\n\n\n  HERE WE GO ")
    size = int(input("\nEnter the game board size (3 for 3x3, 5 for 5x5): "))
    players = 3 if size == 5 else 2
    player_list = []
    for i in range(1, players + 1):
        player_list.append(input("Player " + str(i) + ", enter your username: "))
    # Load and play music
    mixer.init()
    mixer.music.load(MUSIC_FILE)
    mixer.music.play()
    game_menu(player_list)

if __name__ == "__main__":
    main()
