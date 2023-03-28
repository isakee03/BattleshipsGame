def sort_toplist(): #Sorts the toplist textfile
    with open("Toplist.txt", "r") as file:
        lines = file.readlines()
        list = []
        for line in lines:
            list.append(line)
        sorted_list = sorted(list, reverse=True)
        for i in range(0,len(lines)):
            lines[i] = sorted_list[i]
        with open("Toplist.txt", "w") as file:
            for line in lines:
                file.write(line)
    file.close()
#There must be an empty row in the textfile

def check_shot(board_size, row, col): #Checks if shot is valid
    try:
        if int(row) in range(1,board_size+1) and int(col) in range(1,board_size+1):
            if len(str(row))<=2 and len(str(col))<=2:
                return True
        else:
            return "Must be a number that is on the board"
    except:
        return "No letters allowed, must be number that is on the board"

def check_highscore(new_score): #Checks if new score is a top 10 score
    with open("Toplist.txt", "r+") as file:
        lines = file.readlines()
        if len(lines) < 10:
            file.close()
            return True
        else:
            old_score = float(lines[9].split(",")[0])
            if new_score > old_score:
                return True
            else:
                return False

def check_choice(choice, number_of_options): #Checks if a choice is valid
    try:
        if int(choice) in range(1,number_of_options+1):
            return True
        else:
            return "Must be a number between 1 and "+str(number_of_options)
    except:
        return "Must be a number"

def edit_scoreboard(new_score, peeks, name): #Writes new highscore to the toplist textfile
    with open("Toplist.txt", "r+") as file:
        lines = file.readlines()
        if len(lines) < 10:
            file.write(str(round(new_score,3))+", "+str(name)+", "+str(peeks)+"\n")
            file.close()
            sort_toplist()
        else:
            old_score = float(lines[9].split(",")[0])
            if new_score > old_score:
                lines[9] = str(round(new_score,3))+", "+str(name)+", "+str(peeks)+"\n"
                with open("Toplist.txt", "w") as file:
                    for line in lines:
                        file.write(line)
                file.close()
                sort_toplist()
    file.close()

def show_toplist(): #Returns a toplist string
    toplist = "Top 10 scores:\n"
    with open("Toplist.txt", "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines)):
            line_content = lines[i].split(",")
            accuracy = round(float(line_content[0])*100,3)
            name = line_content[1]
            peeks = line_content[2]
            toplist += (str(i+1)+". "+name+" - Accuracy: "+str(accuracy)+"% , "+"Peeks: "+peeks+"\n")
    file.close()
    return toplist
