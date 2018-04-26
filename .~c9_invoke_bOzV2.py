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
        
def set_multiple_usernames(amount):
    username_list = []
    for i in range(amount):
        print("Player {0}".format(i+1))
        username = set_username()
        username_list.append(username)
    return username_list
    
    
    
def multiple_users(user_value):
    if isinstance(user_value, str):
        return False
    else:
        return True
    
    
def create_multiple_users_gameplay_lists(username_list, lives, score):
    """
    returns a list of lists to be used in gameplay loop
    each list contains username,lives,score
    """
    gameplay_list = []
    for username in username_list:
        gameplay_list.append([username, lives, score])
        
    return gameplay_list

    
             
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
    
    found_original_question = False
    questions_list = get_questions_answers_keywords(difficulty)
    
    while found_original_question == False:
        
        random_tuple = choice(questions_list)

        if check_question_is_original(random_tuple, used_questions):
            found_original_question = True
        
        
    return random_tuple
        


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
        
def solo_game_rounds(initial_question, lives, score, used_questions):
    
    
    print("TEST: start of function score: {}".format(score))
    
    if lives > 0:
        
        ask_question(initial_question)
        correct_answer= answer_question(initial_question)
        
        
        if correct_answer:
            score = add_point(score)
            difficulty = set_difficulty(score)
            print("Difficulty: "+ difficulty)
            print("Next question...\n")
            solo_game_rounds(random_question_tuple(difficulty, used_questions), lives, score, used_questions)
        else:
            lives -= 1
            print("Remaining lives: {}\n".format(lives))
            if lives == 0:
                return score
            else:
                print("Guess again...")
                solo_game_rounds(initial_question, lives, score, used_questions)

    
       
        

    
    
    
    
        
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
    
    
    
def sort_scores(scores_tuple_list):
    """
    sorts the scores tuple list in
    descending score. Code from:
    https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples/3121985#3121985
    """
    
    sorted_list = sorted(scores_tuple_list, reverse=True, key=lambda tup: tup[1])
    return sorted_list
    
    

        
def multiplayer_game_rounds(gameplay_list, used_questions):
    
    for player in gameplay_list:
        difficulty = set_difficulty(player[2])
        print("{0}, it's your turn...".format(player[0]))
        print("Difficulty: "+ difficulty)
        
        question = random_question_tuple(difficulty, used_questions)
        ask_question(question)
        correct_answer= answer_question(question)
        if correct_answer:
            print("Well done {0}!".format(player[0]))
            player[2] = add_point(player[2])
            print("")
        else:
            player[1] -= 1
            print("remaining lives: {0}\n".format(player[1]))
            if player[1] == 0:
                print("{0} has been eliminated. \nFinal score: {1}\n".format(player[0], player[2]))

            
        
def remove_eliminated_players(gameplay_list):
    
    player_removed = False

    for player in gameplay_list:
        
        player_lives = player[1]
        if player_lives <= 0:
            gameplay_list.remove(player)
            player_removed = True
            
            
    if player_removed:
        remove_eliminated_players(gameplay_list)
    
  
        
    return gameplay_list
            
            

            
            
        


        
        
    
        
        
    
    
            
            
# def play_solo_game():
    
#     username=set_username()
    
#     score = 0
#     lives = 3
#     used_questions = []
#     initial_question= random_question_tuple("Easy", used_questions)
#     # print (initial_question)
    
#     score = solo_game_rounds(initial_question, lives, score, used_questions)
#     log_score(username, score)
#     sort_scores(create_scores_tuple_list())
             
        
        
# play_solo_game()     

# def play_multiplayer_game(players):
#     usernames = set_multiple_usernames(players)
#     lives =  1
#     score = 0 
#     used_questions = []
    
#     gameplay_lists =create_multiple_users_gameplay_lists(usernames, lives, score)
    
#     while len(gameplay_lists) > 0:
#         multiplayer_game_rounds(gameplay_lists, used_questions)
#         remove_eliminated_players(gameplay_lists)
        
        
# # play_multiplayer_game(3)
        
   
def play_game(players):
    lives = 1
    score = 1
    used_questions = []
    
    if players == 1:
        username = set_username()
        
        initial_question = random_question_tuple("Easy", used_questions)
        score = solo_game_rounds(initial_question, lives, score, used_questions)
        print ("Score inside play_game function: {}".format(score))
        log_score(username, score)
        scores_tuple_list = create_scores_tuple_list()
        sort_scores(scores_tuple_list)
        
    else:
        usernames = set_multiple_usernames(players)
        gameplay_lists =create_multiple_users_gameplay_lists(usernames, lives, score)
        
        while len(gameplay_lists) > 0:
            multiplayer_game_rounds(gameplay_lists, used_questions)
            remove_eliminated_players(gameplay_lists)
            
        
play_game(1)
# play_game(2)
# play_game(4)
    
    


   
      
        



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)










