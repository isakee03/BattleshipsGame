#Written by Isak Elbelin Edlund 2022-12-01
#Here lies the game class

import random

class Game():
    def __init__(self):
        self.ships = []
        self.board_size = 0
        self.shots_taken = 0
        self.shots_hit = 0
        self.peeks = 0
        self.ship_number_counter = 1
        self.game_won = False

        #Getting information from textfile (Parameters.txt), fills the shipslist with different shiplengths for ships, and gets the boardsize
        with open("Params.txt", "r") as file:
            lines = file.readlines()
            ships = lines[0].split(",")
            for ship in ships:
                self.ships.append(int(ship))
            self.board_size = int(lines[1])
        file.close

        #Creating board (matrix)
        self.board = []
        for i in range(0,self.board_size):
            self.board.append([])
            for j in range(0,self.board_size):
                self.board[i].append([0,0])

        #Below are functions for placing out ships

        def __check_empty(row, col, length, direction): #Goes through every square of a ship and the squares around it in the matrix/board, checks if they are all empty
            if direction == 0: #Ship in vertical direction
                for i in range(-1,length+2):
                    for j in range(-1,2):
                        try:
                            if row+i in range(0,self.board_size) and col+j in range(0,self.board_size) and self.board[row+i][col+j][0] != 0:
                                return False
                        except:
                            pass
            else: #Ship in horizontal direction
                for i in range(-1, length+2):
                    for j in range(-1,2):
                        try:
                            if row+j in range(0,self.board_size) and col+i in range(0,self.board_size) and self.board[row+j][col+i][0] != 0:
                                return False
                        except:
                            pass
            return True

        def __create_ship(row, col, length, direction): #Creates a list/matrix with ship coordinates
            ship = []
            if direction == 0: #Ship in vertical direction
                for i in range(0,length):
                    ship.append([row+i,col])
            else: #Horizontal direction
                for i in range(0,length):
                    ship.append([row,col+i])
            return ship

        def __place_one_ship(shiplength):
            random_direction = random.randint(0,1) #Randomizes a direction, horizontal or vertical

            #Randomizing ship coordinates inside the board
            if random_direction == 0:
                random_position_row = random.randint(0,self.board_size-1-shiplength)
                random_position_col = random.randint(0,self.board_size-1)           
            else:
                random_position_row = random.randint(0,self.board_size-1)
                random_position_col = random.randint(0,self.board_size-1-shiplength)

            ship = __create_ship(random_position_row,random_position_col,shiplength,random_direction) #Creates a list with a ships coordinates
            if __check_empty(random_position_row, random_position_col, shiplength, random_direction): #Checks if squares where ship is to be placed are empty
                for i in range(0,shiplength): #Placing out a ship on the board (changing the matrix values)
                    self.board[ship[i][0]][ship[i][1]][0] = 1
                    self.board[ship[i][0]][ship[i][1]][1] = self.ship_number_counter #Assigns shipnumber to the square/position
                self.ship_number_counter += 1
                return True
            else:
                return False #If ship couldn't be placed the function returns false

        #Place ships on board   
        shiplist = self.ships
        while len(shiplist) > 0: #Tries to place out ships from the list, at random positions, until all ships are placed out
            if __place_one_ship(shiplist[0]):
                shiplist.pop(0)

    def show_matrix(self): #Returns the matrix as a string with all its stored information
        matrix_string = ""
        for i in range(0,len(self.board)):
            for j in range(0,len(self.board[i])):
                for x in range(0,len(self.board[i][j])):
                    matrix_string += self.board[i][j][x]
                matrix_string += " "
            matrix_string += '\n'
        return matrix_string

    def show_visible_board(self, peek=False): #Returns the board as a string with information of where ships lie
        board_string = "   "
        for i in range(1,self.board_size+1):
            board_string += str(i)+" "
        board_string += '\n'
        for i in range(0, self.board_size):
            number_length = len(str(i+1))
            if number_length > 1:
                board_string += str(i+1)+" "
            else:
                board_string += str(i+1)+"  "
            for j in range(0,self.board_size):
                if self.board[i][j][0] == 1:
                    board_string += ('\033[1m'+"1"+'\033[0m'+" ")
                else:
                    board_string += "0 "
            board_string += '\n'
        if peek == True: #If the function is called as a peek
            self.peeks += 1
            self.shots_taken += 5
        return board_string

    def shot(self, row, col): #Function for shooting
        
        def __ship_sunk(shipnumber): #Inner function for changing values of squares around sunken ship
            for i in range(0, len(self.board)):
                for j in range(0,len(self.board[i])):
                    if self.board[i][j][1] == shipnumber:
                        for x in range(-1,2):
                            for z in range(-1,2):
                                try:
                                    if i+x in range(0,self.board_size) and j+z in range(0,self.board_size) and self.board[i+x][j+z][0] == 0:
                                        self.board[i+x][j+z][0] = 4
                                except:
                                    pass

        if self.board[row][col][0] == 0:
            self.shots_taken += 1
            self.board[row][col][0] = 2
            return "Miss"
        elif self.board[row][col][0] == 1:
            self.shots_taken += 1
            self.shots_hit += 1
            shipnumber = self.board[row][col][1]
            self.board[row][col][0] = 3            
            for i in range(0, len(self.board)):
                for j in range(0,len(self.board[i])):
                    if self.board[i][j][1] == shipnumber and self.board[i][j][0]==1:
                        return "Hit!"
            __ship_sunk(shipnumber)
            return "Hit!\nShip number "+str(shipnumber)+"\nhas been sunk"
        elif self.board[row][col][0] == 2:
            return "Already tried this\npoint before,\ntry again"
        elif self.board[row][col][0] == 4:
            return "This point already\nmade sure\nno ships in,\ntry again"
        else:
            return "You have already hit a\n ship at this point,\ntry again"

    def show_reduced_board(self): #Returns the board as a string where ships that have not been hit are invisible
        reduced_board_string = "   "
        for i in range(1,self.board_size+1):
            reduced_board_string += str(i)+" "
        reduced_board_string += '\n'
        for i in range(0, self.board_size):
            number_length = len(str(i+1))
            if number_length > 1:
                reduced_board_string += str(i+1)+" "
            else:
                reduced_board_string += str(i+1)+"  "
            for j in range(0, self.board_size):
                if self.board[i][j][0] == 0 or self.board[i][j][0] == 1:
                    reduced_board_string += "X "
                elif self.board[i][j][0] == 2:
                    reduced_board_string += "O "
                elif self.board[i][j][0] == 3:
                    reduced_board_string += "# "
                elif self.board[i][j][0] == 4:
                    reduced_board_string += "- "
            reduced_board_string += '\n'
        return reduced_board_string

    def check_win(self): #Checks if the game is won
        for i in range(0,self.board_size):
            for j in range(0,self.board_size):
                if self.board[i][j][0] == 1:
                    return False
        self.game_won = True
        return True