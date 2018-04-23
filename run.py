import os
import json
from flask import Flask

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
    

def get_questions():
    """
    reads the questions document and asks user a questions
    """
    with open("data/easy.txt", "r") as easy_doc:
        easy_lines = easy_doc.read().splitlines()
        
    easy_questions = []
        
    for i in range(0, len(easy_lines), 4):
        easy_questions.append(easy_lines[i])
        
    return (easy_questions)
    
get_questions()


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)