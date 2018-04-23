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
    
    



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)