import tkinter as tk

import random
import time



root = tk.Tk()
root.geometry("450x560")
root.title("Memory Game")
root.iconbitmap("brain.ico")
global memoryList
global attemptedList
global game_round_num
game_round_num = 0
memoryList = []
attemptedList = []



def DisableAllButtons(): # disables buttons 
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.DISABLED)
    button3.config(state=tk.DISABLED)
    button4.config(state=tk.DISABLED)
    button5.config(state=tk.DISABLED)
    button6.config(state=tk.DISABLED)
    button7.config(state=tk.DISABLED)
    button8.config(state=tk.DISABLED)
    button9.config(state=tk.DISABLED)
def EnableAllButtons(): # enables buttons
    button1.config(state=tk.NORMAL)
    button2.config(state=tk.NORMAL)
    button3.config(state=tk.NORMAL)
    button4.config(state=tk.NORMAL)
    button5.config(state=tk.NORMAL)
    button6.config(state=tk.NORMAL)
    button7.config(state=tk.NORMAL)
    button8.config(state=tk.NORMAL)
    button9.config(state=tk.NORMAL)

def flash_button(button, delay):
    button.config(bg="red")
    root.after(delay, lambda: button.config(bg="white"))

def flash_sequence():
    DisableAllButtons()
    for i in range(len(memoryList)):
        num = memoryList[i]
        delay = i * 1500
        if num == 1:
            root.after(delay, lambda: flash_button(button1, 1000)) # flashes a random number for 1000ms
        elif num == 2:
            root.after(delay, lambda: flash_button(button2, 1000))
        elif num == 3:
            root.after(delay, lambda: flash_button(button3, 1000))
        elif num == 4:
            root.after(delay, lambda: flash_button(button4, 1000))
        elif num == 5:
            root.after(delay, lambda: flash_button(button5, 1000))
        elif num == 6:
            root.after(delay, lambda: flash_button(button6, 1000))
        elif num == 7:
            root.after(delay, lambda: flash_button(button7, 1000))
        elif num == 8:
            root.after(delay, lambda: flash_button(button8, 1000))
        elif num == 9:
            root.after(delay, lambda: flash_button(button9, 1000))
                       
    total_delay = len(memoryList) * 1500
    root.after(total_delay, EnableAllButtons)

def readLines(file_path, num):
    content = ""
    try:
        with open(file_path, 'r') as file:
            for _ in range(num):
                line = file.readline()
                if not line:
                    break
                content += line
    except FileNotFoundError:
        content = "No highscores yet!"
    return content

                       
def startround(): # as in the round of a game
    
    global game_round_num
    attemptedList.clear()
    newNum = random.randint(1,9)
    game_round_num = game_round_num + 1
    memoryList.append(newNum)
    
    
    flash_sequence()
    
def DESTROYALL():
    button1.destroy()
    button2.destroy()
    button3.destroy()
    button4.destroy()
    button5.destroy()
    button6.destroy()
    button7.destroy()
    button8.destroy()
    button9.destroy()
    startGame.destroy()
    
def sort_highscores(): 
    try:
        with open("highscores.txt", 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    scores = []
    for line in lines:
        line = line.strip()
        if " - " in line: # a line is {username - score} in the highscores.txt file
            username, score_str = line.rsplit(" - ", 1) # splits the line into username and score
            try:
                score = int(score_str)
                scores.append((username, score))
            except ValueError:
                continue  # skip malformed lines

    # Sort scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Return top 3  
    return [f"{user} - {score}" for user, score in scores[:3]]
         
         
    
def save_score(username, score, highScoresLabel):
    if username.strip() == "":
        return  
    # Append new score to file
    with open("highscores.txt", "a") as file:
        file.write(f"{username} - {score}\n")
    
    # Read top 3 scores after adding the new one
    updated_scores = readLines("highscores.txt", 3)
    
    # Update the high score label
    highScoresLabel.config(text=updated_scores)
    #read NEW top 3 scores
    new_scores = readLines("highscores.txt", 3)
    #updates the top 3 list 
    top_scores = sort_highscores()
    highScoresLabel.config(text="\n".join(top_scores) if top_scores else "No highscores yet!")
    highScoresLabel.grid(column=1, row=5)

    
def endgame():
    DESTROYALL()
    root.geometry("675x300")
    endFrame = tk.Frame(root)
    endFrame.grid(row=0, column=0)

    endGameLabel = tk.Label(endFrame, font=("Cascadia Code", 20), text=f"Game Over! Well done you lasted {game_round_num} rounds! \nEnter your username to record your score:")
    usernameEntry = tk.Entry(endFrame)
    usernameSubmit = tk.Button(endFrame, text="Submit", fg="red",font=("Cascadia Code", 10), command=lambda: save_score(usernameEntry.get(), game_round_num, highScoresLabel))
    highScores = tk.Label(endFrame, font=("Cascadia Code", 20), text="Top 3 Highscores:")
    highScoresLabel = tk.Label(endFrame, font=("Cascadia Code", 13))
    endGameLabel.grid(column=1, row=1)
    usernameEntry.grid(column=1, row=2)
    usernameSubmit.grid(column=1, row=3)
    highScores.grid(column=1,row=4)
    #sorted High scores
    top_scores = sort_highscores()
    highScoresLabel.config(text="\n".join(top_scores) if top_scores else "No highscores yet!")
    highScoresLabel.grid(column=1, row=5)

    



 
def buttonPressed(numberPressed):
    attemptedList.append(numberPressed)
    if(attemptedList == memoryList[:len(attemptedList)]):
        if(len(attemptedList)==len(memoryList)):
            startround()
            
    else:
        endgame()
def start():
    
    startGame.config(bg="green")
    startGame.config(state=tk.DISABLED)
    root.after(100, lambda:startGame.config(bg="white"))
    startround()

        
    
#adds the buttons to the tkinter GUI
startGame = tk.Button(root,font=("Cascadia Code", 9), text="Start", width=20, height=2, command=start)
button1 = tk.Button(root,font=("Cascadia Code", 9), text="1", width=20, height=10, bg="white", command=lambda:buttonPressed(1))
button2 = tk.Button(root,font=("Cascadia Code", 9), text="2", width=20, height=10, bg="white",command=lambda:buttonPressed(2))
button3 = tk.Button(root,font=("Cascadia Code", 9), text="3", width=20, height=10, bg="white",command=lambda:buttonPressed(3))
button4 = tk.Button(root,font=("Cascadia Code", 9), text="4", width=20, height=10, bg="white",command=lambda:buttonPressed(4))
button5 = tk.Button(root,font=("Cascadia Code", 9), text="5", width=20, height=10, bg="white",command=lambda:buttonPressed(5))
button6 = tk.Button(root,font=("Cascadia Code", 9), text="6", width=20, height=10, bg="white",command=lambda:buttonPressed(6))
button7 = tk.Button(root,font=("Cascadia Code", 9), text="7", width=20, height=10, bg="white",command=lambda:buttonPressed(7))
button8 = tk.Button(root,font=("Cascadia Code", 9), text="8", width=20, height=10, bg="white",command=lambda:buttonPressed(8))
button9 = tk.Button(root,font=("Cascadia Code", 9), text="9", width=20, height=10, bg="white",command=lambda:buttonPressed(9))


startGame.grid(column=2,row=0)
button1.grid(column=1, row=1)
button2.grid(column=2, row=1)
button3.grid(column=3, row=1)
button4.grid(column=1, row=2)
button5.grid(column=2, row=2)
button6.grid(column=3, row=2)
button7.grid(column=1, row=3)
button8.grid(column=2, row=3)
button9.grid(column=3, row=3)




root.mainloop()
