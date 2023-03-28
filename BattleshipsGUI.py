#Written by Isak Elbelin Edlund 2022-12-01

import tkinter as tk
import time
from Functions import *
from Game import Game

def main(): #Main function for the game
    game=Game()
    #Below are functions specifically used for the graphical user input
    
    def delete(r,c): #Deletes a widget, based on row and column
        try:
            root.grid_slaves(row=r,column=c)[0].destroy()
        except:
            pass

    def score_board_GUI_edit(name_entry, name_enter_button, accuracy): #Edits the scoreboard and updates it
        name_input = name_entry.get()
        edit_scoreboard(accuracy,game.peeks,name_input)
        scoreboard = root.grid_slaves(row=0,column=game.board_size+4)[0]
        scoreboard["text"] = show_toplist()
        name_entry.destroy()
        name_enter_button.destroy()
        output('Your score has\nbeen added to\nthe scoreboard\nPress "Start new game" to play again',1)

    def square_click(row,col): #Function for when you click a square on the board
        output(game.shot(row,col),2) #Tries a shot, changes the game matrix values and returns the output of the shot in "output 2"
        if game.check_win():
            accuracy = game.shots_hit/game.shots_taken
            peeks = game.peeks
            buttons_state(3,game.board_size+1,enabled=False) #Disables peek button to prevent adding peeks to score after game won
            if check_highscore(accuracy): #If new highscore
                output("You won!\nNew highscore (top 10)\nPlease enter your name below",1)
                name_entry = tk.Entry(root,width=30)
                name_entry.grid(row=8,column=game.board_size+1,columnspan=3,padx=30,pady=10)
                name_enter_button = tk.Button(root, text = "Press here after name has been entered", command = lambda: score_board_GUI_edit(name_entry, name_enter_button, accuracy))
                name_enter_button.grid(row=9,column=game.board_size+1,columnspan=3,padx=30,pady=10)
            else:
                output("You won!\nAccuracy: "+str(round(accuracy*100,1))+"%",1)
        update_board() #Updates any changes to the board in reduced visibility

    def output(output_text, output): #Changes the text of output 1 or 2
        if output == 1:
            root.grid_slaves(row=6,column=game.board_size+1)[0]["text"] = output_text
        else:
            root.grid_slaves(row=game.board_size+1,column=4)[0]["text"] = output_text

    def buttons_state(r,c,enabled=True): #Enables and disables buttons
        if enabled==True:
            root.grid_slaves(row=r,column=c)[0]["state"] = "normal"
        else:
            root.grid_slaves(row=r,column=c)[0]["state"] = "disabled"

    def update_board(visibility=False): #Updates board with either reduced or full visibility
        #Creating the row and column bar at the side
        for i in range(1,game.board_size+1):
            delete(i,0)
            column_label = tk.Label(root, text=str(i))
            column_label.grid(row=i,column=0,columnspan=1,rowspan=1)
            delete(0,i)
            column_label = tk.Label(root, text=str(i))
            column_label.grid(row=0,column=i,columnspan=1,rowspan=1)
        #Creating the board squares
        for i in range(0,game.board_size):            
            for j in range(0,game.board_size):
                delete(i+1,j+1)
                if game.game_won == True or visibility == True: #If you have already won, the buttons are disabled
                    button = tk.Button(root, text="X", padx=10, pady=10,bg="blue", fg="white") #Disabled button
                else:
                    button = tk.Button(root, text="X", padx=10, pady=10, command=lambda a=i,b=j: square_click(a,b), bg="blue", fg="white")
                if visibility == False:
                    if game.board[i][j][0] == 2:
                        button.config(text="O", bg="black")
                    elif game.board[i][j][0] == 3:
                        button.config(text="#", bg="green")
                    elif game.board[i][j][0] == 4:
                        button.config(text="-", bg="red")
                if visibility == True:
                    if game.board[i][j][0] == 1:
                        button.config(text="1", bg="green")
                    else:
                        button.config(text="0", bg="blue")
                button.grid(row=i+1,column=j+1)
        if visibility == True:
            game.show_visible_board(peek=True)
            buttons_state(3,game.board_size+1,enabled=False) #Peek button temporarily disabled
            buttons_state(0,11,enabled=False) #New game button temporarily disabled
            root.after(2000,lambda:[update_board(visibility=False),buttons_state(3,game.board_size+1),buttons_state(0,11)])
            #After 2s board goes back to reduced visibility and enables the primary buttons again
    
    #Cleaning up GUI whenever new game button is pressed
    for i in range(0,game.board_size+10):
        for j in range(0,game.board_size+10):
            square = root.grid_slaves(row=i,column=j)
            try:
                if square[0]["text"] != "Start new game" and square[0]["text"] != show_toplist(): #Deletes every widget except the new game button and the scoreboard
                    print(square["text"])
                    delete(i,j)
                else:
                    pass
            except: #If square is empty
                delete(i,j)
    update_board() #Shows the game board with reduced visibility

    #Creating primary widgets which are to be used
    output_label1 = tk.Label(root, text="Output 1:")
    output_label1.grid(row=6,column=game.board_size+1,columnspan=2,rowspan=2)

    output_label2 = tk.Label(root, text="Output 2:")
    output_label2.grid(row=game.board_size+1,column=4,rowspan=3,columnspan=5)

    peek_button = tk.Button(root, text="Peek for\n2 seconds\n(Cost 5 shots)", padx=30, pady=30, command=lambda: update_board(visibility=True), fg="red")
    peek_button.grid(row=3,column=game.board_size+1,columnspan=3,rowspan=3,sticky="nsew")

#Getting information from textfile (Parameters.txt), information needed for buttons (below) which do not have access to game properties
with open("Params.txt", "r") as file:
    lines = file.readlines()
    board_size = int(lines[1])
file.close

#TKInter (Creating main buttons and labels, applies settings and starts the TKInter loop)
root = tk.Tk()
root.title = ("Battleships")
root.geometry("950x600")
root.resizable(False, False)
start_game = tk.Button(root, text="Start new game", padx=30, pady=30, command=lambda: main())
start_game.grid(row=0,column=board_size+1,rowspan=3,columnspan=3,sticky="nsew")
scoreboard = tk.Label(root,text=show_toplist())
scoreboard.grid(row=0,column=board_size+4,rowspan=8,columnspan=6,sticky="n")
root.mainloop()
