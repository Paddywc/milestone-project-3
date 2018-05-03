import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for
from random import choice

app = Flask(__name__)

app.secret_key = 'some_secret'

username = "default"



def get_round_text():
    round_text = []
    with open("active-game-files/game_text.txt", "r") as game_text:
        round_text=  game_text.readlines()
    # print(round_text)
    return round_text
    
def wipe_game_text():
    f = open("active-game-files/game_text.txt", "r+")
    f.truncate()
    f.close()
    
def add_game_text(content):
    with open("active-game-files/game_text.txt", "a") as game_text:
        game_text.writelines(content + "\n")
        


def add_correct_text(text):
    correct_text = "<h3 class='correct'>{}</h3>".format(text)
    add_game_text(correct_text)
    return correct_text
    
def add_incorrect_text(text):
    incorrect_text="<h3 class='incorrect'>{}</h3>".format(text)
    add_game_text(incorrect_text)
    return incorrect_text
    
    
def add_eliminated_text(player):
    username= player["username"]
    add_game_text("<h3 class = 'elimination'>{} has been eliminated </h3>".format(username))

def add_question_text(question):
    add_game_text("<h2 class ='question'> {0} </h2>".format(question))

        
def dump_data(player_list):
    with open("active-game-files/players.json", mode="w", encoding="utf-8") as json_data:
            json.dump(player_list, json_data)
            
def get_json_data():
    with open("active-game-files/players.json", "r") as json_file:
        json_data =  json.load(json_file)
        return json_data
        
        
def get_leaderboard_data():
    with open("data/high_scores.json", "r") as f:
        leaderboard_data =  json.load(f)
        return leaderboard_data
        
def post_leaderboard_data(leaderboard_data):
    with open("data/high_scores.json", mode="w", encoding="utf-8") as f:
            json.dump(leaderboard_data, f)
            
            
def add_game_over_text():
    add_game_text("<h2 class='game-over-test'>Game Over</h2>")
            
            
def get_sorted_scores():
    # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
    leaderboard_data = get_leaderboard_data()
    sorted_data = sorted(leaderboard_data, reverse=True, key=lambda k: k["score"])
    return sorted_data
        
        
def return_player_to_game_data(player_to_return):
    game_data = get_json_data()
    
    player_index = 999
    
    for player in game_data:
        if player["no"] == player_to_return["no"]:
            
            player_index = game_data.index(player)
            
    game_data[player_index] = player_to_return
            
            
            
    dump_data(game_data)
    return game_data
    
    
def get_current_player():
    
    current_player = {}
    game_data = get_json_data()
    
    for player in game_data:
        if player["turn"] == True:
            current_player = player
            
    return current_player
    

def set_username():
    """
    sets the user's username
    """
    username = input("Please enter your desired username: ")
    # username = request.form["answer"]
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
        if amount > 1:
            print("Player {0}".format(i+1))
        username = set_username()
        username_list.append(username)
    return username_list
    
    

    
def create_gameplay_lists(username_list, lives, score):
    """
    returns a list of lists to be used in gameplay loop
    each list contains username,lives,score 
    and empty string (will be their question in game)
    and a boleen initially set as True(used to check if their last
    question was answered correctly )
    """
    gameplay_list = []
    for username in username_list:
        gameplay_list.append([username, lives, score, "", True ])
        
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
        pictures_tuples_list.append(("/static/img/{}".format(pictures_lines[i]), pictures_lines[i+1], pictures_lines[i+2], pictures_lines[i+3]))
    
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
    
    
def get_used_questions():
    
    with open("active-game-files/used_questions.json", "r") as f:
        used_questions = json.load(f)
        return used_questions
        
        
def initialize_used_question():
    
    question_list = []
    question_list.append({"question": "sameple_question"})
    
    with open("active-game-files/used_questions.json", mode="w", encoding="utf-8") as f:
        json.dump(question_list, f)
        
def add_to_used_questions(question, used_questions):
    
    used_questions.append({"question" : question[0]})
    
    with open("active-game-files/used_questions.json", mode="w", encoding="utf-8") as f:
            json.dump(used_questions, f)
            

    
def check_question_is_original(question_tuple):
    """
    checks to see if a question has
    already been asked
    """
    
    used_questions = get_used_questions()
    
    original_question = True
    
    for question in used_questions:
        if question["question"] == question_tuple[0]:
            original_question = False
            
            
    if not original_question:
        return False
        
    else:
        add_to_used_questions(question_tuple, used_questions)
        return True
        
            

    # if question_tuple not in used_questions:
    #     add_question_to_used_questions(question_tuple)
    #     return used_questions
    
    # else:
    #     return False

def random_question_tuple(difficulty):
    """
    selects a random tuple from the tuples list
    returns it if it has not already been asked
    """
    
    found_original_question = False
    questions_list = get_questions_answers_keywords(difficulty)
    
    while found_original_question == False:
        
        random_tuple = choice(questions_list)

        if check_question_is_original(random_tuple):
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
    

def ask_question():
    """
    asks question to the user
    """
    
    current_player = get_current_player()
    game_data = get_json_data()
    number_of_players = len(game_data)
    
    if number_of_players > 1:
        host_text = ("<h2 class = 'host'>You're up {}</h2>".format(current_player["username"]))
        add_game_text(host_text)
            
    
    question = current_player["question"]
    
    if question_is_picture_question(question): 
        print("remain for testing")
        img_text = "<img src ='{}'>".format(question[0])
        print(img_text)
        add_game_text(img_text)
        add_question_text(question[1])
    else:
        # print(question[0])
        add_question_text(question[0])
        
        
def answer_question(question):
    """
    asks user for an answer and
    check if it contains the keyword
    """
    # user_answer = input(">> Your answer: ")
    user_answer = request.form["answer"]
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()
    
    if question_is_picture_question(question):
        keyword = question[3]
    else:
        keyword = question[2]
    
    if keyword in user_answer_list:
        print("Correct!")
        add_game_text("Correct!")
        return True
    else:
        print("Incorrect")
        add_game_text("Incorrect!")
        return False
        
        

def add_point(score):
    """
    adds 1 to the parameter 
    then prints and returns it
    """
    score += 1
    print("Current score: {0}".format(score))
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
    
    
    
def sort_scores(scores_tuple_list):
    """
    sorts the scores tuple list in
    descending score. Code from:
    https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples/3121985#3121985
    """
    
    sorted_list = sorted(scores_tuple_list, reverse=True, key=lambda tup: tup[1])
    return sorted_list
    
    
    
def set_previous_player(game_data, previous_player_index):
    
    for player in game_data:
        player["previous"] = False
        
    game_data[previous_player_index]["previous"] = True
    
    dump_data(game_data)
    return game_data
    
    
def get_previous_player():
    
    game_data = get_json_data()
    
    previous_player = {}
    
    for player in game_data:
        if player["previous"] == True:
            previous_player = player
        
    return previous_player
        
    
    
    
def set_new_chosen_and_previous_player():
    
    game_data = get_json_data()
    
    number_of_players = len(game_data)
    
    player_index = 0
    
    for player in game_data:
        player["previous"] = False
    
    for player in game_data:
        if player["turn"] == True:
            player["previous"] = True
            player_index = game_data.index(player)
            player["turn"] = False
            
            
    if player_index < number_of_players-1:
        game_data[player_index +1]["turn"] = True
        
    else:
        game_data[0]["turn"] = True
        
    dump_data(game_data)
    
    # if previous_player_index < number_of_players-1:
    #     game_data[previous_player_index + 1]["turn"] = True
    # else:
    #     game_data[0]["turn"] = True
        
    # set_previous_player(game_data, previous_player_index)
        
    # dump_data(game_data)
        
    # return game_data
        
        

    

def select_player(game_data):
    
    chosen_player = {}
    index_of_chosen_player = 0
    
    set_new_chosen_and_previous_player()


    for player in (game_data):
        if player["turn"] == True:
            chosen_player = player
            # player["turn"] = False
            # index_of_chosen_player = game_data.index(player)
            
            
    
    return chosen_player
            

    
        

def set_previous_answer():

    user_answer = request.form["answer"]
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()
    
    previous_player = get_previous_player()
    previous_player["answer"] = user_answer_list

    return_player_to_game_data(previous_player)
    


def set_user_answer(player, game_data):
  
    
    user_answer = request.form["answer"]
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()
    
    player["answer"] = user_answer_list
    
    return_player_to_game_data(player)
    dump_data(game_data)
    return game_data
    
def check_previous_player_answer():
    
    previous_player = get_previous_player()
    answer = previous_player["answer"]

    question = previous_player["question"]
    
    
    if question_is_picture_question(question):
        keyword = question[3]
    else:
        keyword = question[2]
        
    if keyword in answer:
        print("Correct!")
        add_correct_text("Correct!")
        previous_player["last question correct"] = True
        return_player_to_game_data(previous_player)
        return True
    else:
        print("Wrong!")
        add_incorrect_text("Incorrect")
        previous_player["last question correct"] = False
        return_player_to_game_data(previous_player)
        return False
        

        
    
def check_user_answer(player, game_data):
    question = player["question"]
    answer = player["answer"]
    
    
    if question_is_picture_question(question):
        keyword = question[3]
    else:
        keyword = question[2]
        
    if keyword in answer:
        print("Correct!")
        add_game_text("Correct!")
        return True
    else:
        print("Incorrect")
        add_game_text("Incorrect!")
        return False
        
        
        
def set_player_question():
    
    current_player = get_current_player()
    
    if current_player["last question correct"] == True:
        difficulty = set_difficulty(current_player["score"])
        current_player["question"] = random_question_tuple(difficulty)
    
    return_player_to_game_data(current_player)

    
    
# def render_game_round(game_data, used_questions):
    
#     wipe_game_text()
#     player = select_player(game_data)
#     add_game_text("You're up {0}".format(player["username"]))
#     difficulty = set_difficulty(player["score"])
    
#     player["question"] = random_question_tuple(difficulty, used_questions)
    
#     ask_question(player["question"])
    
#     answer_question(player["question"])
    
#     return_player_to_game_data(player, game_data)
    
#     dump_data(game_data)
    
    
    # for player in game_data:
        
    #     score = player["score"]
    #     add_game_text("You're up: {0}".format(player["username"]))
    #     difficulty = set_difficulty(score)
        
    #     player["question"] = random_question_tuple("Easy", used_questions)
        
    #     ask_question(player.get("question"))
        
    #     return render_template("game.html", game_data = game_data,)


        
# def game_round(gameplay_list, used_questions):
    
#     for player in gameplay_list:
        
#         print(player)
        
#         difficulty = set_difficulty(player[2])
#         last_question_correct = player[4]
        
#         if last_question_correct:
#             player[3] = random_question_tuple(difficulty, used_questions)
            
         
#         if len(gameplay_list)>1:  
#             print("You're up {}".format(player[0]))
            
#         if not last_question_correct:
#             print("Let's try that again...")
            
   
        
        
#         ask_question(player[3])
#         correct_answer= answer_question(player[3])
#         if correct_answer:
#             print("Well done {0}!".format(player[0]))
#             player[4] = True
#             player[2] = add_point(player[2])
#             print("")
#         else:
#             player[1] -= 1
#             print("remaining lives: {0}\n".format(player[1]))
#             player[4] = False
#             if player[1] == 0 and len(gameplay_list) > 1:
#                 print("{0} has been eliminated. \nFinal score: {1}\n".format(player[0], player[2]))



def update_lives_and_score(correct):
    
    previous_player = get_previous_player()
    
    if correct:
        previous_player["score"] += 1
    else:
        previous_player["lives"]  -= 1
        
    return_player_to_game_data(previous_player)
    
    
    
        
def remove_eliminated_players(gameplay_list):
    
    player_removed = False

    for player in gameplay_list:
        
        player_lives = player[1]
        if player_lives <= 0:
            gameplay_list.remove(player)
            log_score(player[0], player[2])
            player_removed = True
            
            
    if player_removed:
        remove_eliminated_players(gameplay_list)
    
  
        
    return gameplay_list
            
            
            
            

            
   
# def play_game(players):
#     lives = 3
#     score = 0
#     used_questions = []
#     eliminated_players = []

    
    
#     usernames = set_multiple_usernames(players)
#     gameplay_lists =create_gameplay_lists(usernames, lives, score)


        
#     while len(gameplay_lists) > 0:
#         game_round(gameplay_lists, used_questions)
#         remove_eliminated_players(gameplay_lists)
        
#     scores_list = create_scores_tuple_list()
#     sort_scores(scores_list)
    



def is_first_round(game_data):
    
    
    first_round = True
    for player in game_data:
        if player["previous"]==True:
            first_round = False
            
            
            
    
    return first_round
    
def initial_player():
    game_data = get_json_data()
    game_data[0]["turn"] = True
    
    dump_data(game_data)
    
    
def eliminate_dead_players():
    
    game_data = get_json_data()
    

    player_index = 999
    
    for player in game_data:
        if player["lives"] <= 0:
            add_to_leaderboard(player)
            player_index = game_data.index(player)
            add_eliminated_text(player)
            
    if player_index != 999:
        game_data.pop(player_index)
        dump_data(game_data)
        eliminate_dead_players()
        
            
            
            
    dump_data(game_data)
    return game_data
    
    
def add_to_leaderboard(player):
    
    username = player["username"]
    score = player["score"]
    
    saved_score = {"username": username, "score": score}
    
    
    leaderboard_data = get_leaderboard_data()
    
    leaderboard_data.append(saved_score)
    
    post_leaderboard_data(leaderboard_data)
    
    
    
    
    
    
    
def all_players_gone():
    game_data = get_json_data()
    
    print(len(game_data))
    if len(game_data)>0:
        return False
    else:
        return True
    
    
@app.route("/" , methods=["GET"])
def index():

    if request.method=="GET":
        round_text = get_round_text()
        players = request.args.get("players")
        if players == None:
            return render_template("index.html")
        else:
            return redirect("/setusernames/{}".format(players))
            
            

            
@app.route("/setusernames/<players>" , methods=["POST", "GET"])
def set_username_page(players):
    
    

    players = int(players)

    player_list = []
    if request.method=="POST":
        for i in range(players):
            i_string = str(i)
            username = request.form["player-{0}-username".format(i+1)]
            player_object = {
                "username" : username,
                "lives" : 3,
                "score" : 4,
                "question": "",
                "last question correct": True,
                "turn" : False,
                "previous": False,
                "answer": "",
                "no": i+1
            }
            player_list.append(player_object)
            
        # initial_player = player_list[0]
        # initial_player["turn"] = True
        used_questions = []
        # set_player_question(initial_player, player_list, used_questions)
        
        # return_player_to_game_data(initial_player, player_list)
        
        
        dump_data(player_list)
        
        return redirect("/game")
    
    

    return render_template("usernames.html", players=players)
    
    
@app.route("/leaderboard")
def show_leaderboard():
    
    leaderboard_data = get_sorted_scores()
    
    return render_template("leaderboard.html", leaderboard_data = leaderboard_data)
    
    
    
    
    
    
@app.route("/game" , methods=["GET" , "POST"])
def render_game():
    
    wipe_game_text()

    game_data = get_json_data()
    
    players = len(game_data)
    col_size = 12/players
    
    
    if request.method == "POST":
        
        set_new_chosen_and_previous_player()
        
        
        set_previous_answer()
        was_correct = check_previous_player_answer()
        update_lives_and_score(was_correct)
        set_player_question()
        ask_question()
    
    game_data = get_json_data()
        
        
    if is_first_round(game_data):
       
       
       initialize_used_question()
       game_data[0]["turn"] = True
       
       dump_data(game_data)
       
       set_player_question()

       ask_question()
    
       
    
    eliminate_dead_players()

    round_text = get_round_text()
    if all_players_gone():
        wipe_game_text()
        add_game_over_text()
        round_text = get_round_text()
        leaderboard_data = get_sorted_scores()
    
        return render_template("leaderboard.html", leaderboard_data = leaderboard_data, round_text=round_text)
        
        
    round_text = get_round_text()
    game_data = get_json_data()

        
        
    return render_template("game.html", game_data = game_data, col_size = col_size, round_text = round_text)

        
        
        
    

       
      
          

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @app.route("/" , methods=["POST"])
# def submit_response():
    
#     usernames = []
#     for i in range(2):
#         usernames.append(set_username())
#     return str(usernames)
#     # answer = request.form["answer"]
#     # answer2 = request.form["answer2"]
#     # username_list = set_multiple_usernames(2)
#     # for user in username_list:
    #     return user

       
       

   
        
        
        
        

# play_game(1)
# play_game(2)
# # play_game(4)
    
    


   
      
        



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
            
            





    
    
# @app.route("/" , methods=["POST", "GET"])
# def index():

#     if request.method=="POST":
#         players = request.args.get("players")
#         request.args('players', "one")
#         return render_template("players-{0}.html".format(players))
    
#     return render_template("index.html")
    
    
# @app.route("/" , methods=["POST", "GET"])
# def start_game():
#     if request.method=="POST":
#         players = request.args.get("players")
#         return redirect(url_for("/play/{}".format(players)))
    
       
#     return render_template("index.html")
    

    
