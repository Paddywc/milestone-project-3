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
    
             
def set_difficulty(current_score):
    """
    returns a difficulty level string
    determined by the current score  
    entered as an int parameter
    """
    if current_score >= 8:
        return "Hard"
    elif current_score >= 6:
        return "Picture"
    elif current_score >=2:
        return "Normal"
    else:
        return "Easy"
        
        
    
def get_picture_tuple_list():
    """
    returns a list tuple of picture questions
    each tuple consists of link, question, answer, 
    keyword
    """
    
    with open("data/pictures.txt") as pictures_doc:
        pictures_lines = pictures_doc.read().splitlines()
        
    pictures_tuples_list = []
    
    for i in range(0, len(pictures_lines), 5):
        pictures_tuples_list.append(("/data/images/{}".format(pictures_lines[i]), pictures_lines[i+1], pictures_lines[i+2], pictures_lines[i+3]))
    
    return pictures_tuples_list
    
    
        
    
def get_questions_answers_keywords(difficulty):
    """
    returns list of tuples in format of (question, answer, keyword)
    read from questions document, determined by difficulty 
    """
    
    if difficulty == "Picture":
        return get_picture_tuple_list()
        
    else:
        with open("data/{}.txt".format(difficulty.lower()), "r") as questions_doc:
            doc_lines = questions_doc.read().splitlines()
            
        tuples_list = []
            
        for i in range(0, len(doc_lines), 4):
            tuples_list.append((doc_lines[i], doc_lines[i+1], doc_lines[i+2]))
            

        return tuples_list
    
    
    
    
def check_question_is_original(question_tuple, used_questions):
    """
    checks to see if a question has
    already been asked
    """
   
        
    if question_tuple not in used_questions:
        used_questions.append(question_tuple)
        return used_questions
    
    else:
        return False

def random_question_tuple(difficulty, used_questions):
    """
    selects a random tuple from the tuples list
    returns it if it has not already been asked
    """
    
    questions_list = get_questions_answers_keywords(difficulty)
    random_tuple = choice(questions_list)
    
    if check_question_is_original(random_tuple, used_questions):
        return random_tuple
    
    else:
        random_question_tuple(difficulty, used_questions)
        


def question_is_picture_question(question):
    """
    checks if question tuple is a picture
    question
    """
    if len(question)==4: 
        return True
    else: 
        return False
    

def ask_question(question):
    """
    asks question to the user
    """
    if question_is_picture_question(question): 
        print (question[0])
        print (question[1])
    else:
        print(question[0])
    
def answer_question(question):
    """
    asks user for an answer and
    check if it contains the keyword
    """
    user_answer = input(">> Your answer: ")
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()
    
    if question_is_picture_question(question):
        keyword = question[3]
    else:
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
        
def game_rounds(initial_question, lives, score, used_questions):
    
    
    
    
    if lives > 0:
        
        ask_question(initial_question)
        correct_answer= answer_question(initial_question)
        
        
        if correct_answer:
            score = add_point(score)
            difficulty = set_difficulty(score)
            print("Difficulty: "+ difficulty)
            print("Next question...\n")
            game_rounds(random_question_tuple(difficulty, used_questions), lives, score, used_questions)
        else:
            lives -= 1
            print("Remaining lives: {}\n".format(lives))
            print("Guess again...")
            game_rounds(initial_question, lives, score, used_questions)
    
    else:
        return score
        
        
        
        
        
def log_score(username, score):
    """
    appends all_scores.txt with 'username,score'
    """
    
    
    with open("data/all_scores.txt", "a") as all_scores:
        all_scores.write("{0},{1}\n".format(username,score))
        
        
def create_scores_tuple_list():
    """
    returns a list of tuples. Each 
    tuple is a line from all_scores.txt
    """
    
    scores_tuple_list  = []
    with open ("data/all_scores.txt", "r") as all_scores:
        for i in all_scores.readlines():
            tuple_entry = i.split(",")
            scores_tuple_list.append((str(tuple_entry[0]), int(tuple_entry[1])))
    
    return scores_tuple_list
    
    
    

        
        
    
        
        
    
    
            
            
def play_game():
    
    username=set_username()
    
    score = 0
    lives = 3
    used_questions = []
    initial_question= random_question_tuple("Easy", used_questions)
    print (initial_question)
    
    score = game_rounds(initial_question, lives, score, used_questions)
             
             
             
#play_game()

# log_score("Paddy",6)
# log_score("Pat",9)
# log_score("Mike",3)

    
    
    


   
      
        



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)