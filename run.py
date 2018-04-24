import os
import json
from flask import Flask
from random import choice

app = Flask(__name__)

app.secret_key = 'some_secret'

username = "default"

def set_username():
    """
    sets the user's username
    """
    username = input("Please enter your desired username: ")
    if len(username) > 0:
        print("Hello "+ username)
        return(username)
    else:
        print("Please enter a username")
        print("")
        set_username()
    

def get_questions_answers_keywords():
    """
    reads the questions document and asks user a questions
    """
    with open("data/easy.txt", "r") as easy_doc:
        easy_lines = easy_doc.read().splitlines()
        
    tuples_list = []
        
    for i in range(0, len(easy_lines), 4):
        tuples_list.append((easy_lines[i], easy_lines[i+1], easy_lines[i+2]))
        

    return (tuples_list)



def random_question_tuple():
    """
    selects a random tuple from the tuples list
    """
    
    questions_list = get_questions_answers_keywords()
    random_tuple = choice(questions_list)
    return(random_tuple)
    
    

def ask_question(question):
    """
    asks question to the user
    """
    print(question[0])
    
def answer_question(question):
    """
    asks user for an answer and
    check if it contains the keyword
    """
    user_answer = input(">> Your answer: ")
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()
    
    keyword = question[2]
    
    if keyword in user_answer_list:
        print("Correct!")
        return True
    else:
        print("Wrong!")
        return False
        
        

def add_point(score):
    """
    adds 1 to the parameter 
    then prints and returns it
    """
    score += 1
    print("Current score: {0}".format(score))
    return score
        
def game_rounds(initial_question, lives):
    
    score = 0
    
    if lives > 0:
        
        ask_question(initial_question)
        correct_answer= answer_question(initial_question)
        
        if correct_answer:
            print("\n Next question...")
            score = add_point(score)
            game_rounds(random_question_tuple(), lives)
        else:
            lives -= 1
            print("Remaining lives: {}\n".format(lives))
            print("Guess again...")
            game_rounds(initial_question, lives)
    
    else:
        return False
            
             
             
def set_difficulty(current_score):
    """
    returns a difficulty level string
    determined by the current score  
    entered as an int parameter
    """
    if current_score >= 7:
        return "Hard"
    elif current_score >=2:
        return "Normal"
    else:
        return "Easy"
    
    
    
    

#game_rounds(random_question_tuple(), 2)
   
   
      
        



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)