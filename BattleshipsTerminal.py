#Written by Isak Elbelin Edlund 2022-12-01

import time
from Functions import *
from Game import Game

def main(): #Main function (loop) for the game
    print(show_toplist())
    game_on = True
    game_won = False
    while game_on: #Main menu where you choose to start new game or exit
        print("You are in the main menu! Please choose an alternative below \n 1. Start new game \n 2. Exit")
        main_choice = input("Choose an option (number): ")
        if check_choice(main_choice, 2) == True:
            if int(main_choice) == 1:
                in_game = True
                game = Game()
                while in_game: #In game, here you choose from 3 alternatives what you want to do in the game
                    print("Please choose from the options below: \n 1. Shoot \n 2. Peek at the board (for 2 seconds, cost 5 shots) \n 3. End game")
                    print(game.show_reduced_board())
                    choice = input("Choose an option (number): ")
                    if check_choice(choice, 3) == True:
                        if int(choice) == 1:
                            choice_row=input("Choose a row: ")
                            choice_col=input("Choose a column: ")
                            while True:
                                if check_shot(game.board_size, choice_row, choice_col) == True:
                                    print(game.shot(int(choice_row)-1, int(choice_col)-1)) #Returns what happened with the shot attempt
                                    if game.check_win() == True: #If all ships are sunk, you have won
                                        in_game=False
                                        game_on=False
                                        game_won=True
                                        print(game.show_reduced_board())
                                        accuracy = game.shots_hit/game.shots_taken
                                        peeks = game.peeks
                                        print("You won! Here are the results: \nAccuracy: "+str(round(accuracy*100,1))+"% , Peeks: "+str(peeks))
                                        if check_highscore(accuracy): #If score is top 10
                                            name = input("New highscore! Enter your name: ")
                                            edit_scoreboard(accuracy, peeks, name)
                                        print(show_toplist())
                                    break
                                else:
                                    print(check_shot(game.board_size, choice_row, choice_col)+". Try again!")
                                    choice_row=input("Choose a row: ")
                                    choice_col=input("Choose a column: ")
                        elif int(choice) == 2:
                            print(game.show_visible_board(peek = True))
                            time.sleep(2)
                            print("\n"*10)
                        else:
                            print(game.show_visible_board())
                            in_game = False
                            break
                    else:
                        print(check_choice(choice, 3)+". Try again!")
            else:
                game_on = False
                break
        else:
            print(check_choice(main_choice, 2)+". Try again!")
    if game_won == True:
        continue_game = input("\n Do you wish to continue playing? \n 1. Yes \n 2. No \n Please choose an option:")
        while True:
            if check_choice(continue_game, 2) == True:
                if int(continue_game) == 1:
                    main() #Starts a new game if player chooses to
                    break
                else:
                    game_on = False #Exits the game if players chooses to
                    break
            else:
                print(check_choice(continue_game, 2))
                continue_game = input("\n Do you wish to continue playing? \n 1. Yes \n 2. No \n Please choose an option:")

main()