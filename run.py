import os
import json
import requests
from flask import Flask, render_template, request, redirect
from random import choice

app = Flask(__name__)

app.secret_key = 'some_secret'


"""
functions for working with game text files
"""


def wipe_game_text(game_over=False):
    """
    wips all game text files
    if game over == True, don't wipe 
    correct_answer. This is so the final
    player's correct answer can be displayed
    in the leadboard page
    """
    
    f = open("active-game-files/game_over.txt", "r+")
    f.truncate()
    f.close()

    f = open("active-game-files/eliminated.txt", "r+")
    f.truncate()
    f.close()

    f = open("active-game-files/correct.txt", "r+")
    f.truncate()
    f.close()

    f = open("active-game-files/incorrect_guesses.txt", "r+")
    f.truncate()
    f.close()

    f = open("active-game-files/host.txt", "r+")
    f.truncate()
    f.close()

    if not game_over:
        f = open("active-game-files/answer.txt", "r+")
        f.truncate()
        f.close()

    f = open("active-game-files/question.txt", "r+")
    f.truncate()
    f.close()

    f = open("active-game-files/question.txt", "r+")
    f.truncate()
    f.close()


def add_correct_text(text):
    """
    add argument text to correct.txt wrapped 
    in span.correct
    """
    with open("active-game-files/correct.txt", "a") as f:
        f.writelines("<span class='correct'>{}</span>".format(text))


def add_incorrect_text(text):
    """
    add argument text to correct.txt wrapped 
    in span.incorrect
    """
    with open("active-game-files/correct.txt", "a") as f:
        f.writelines("<span class='incorrect'>{}</span>".format(text))


def add_incorrect_guesses_text(player):
    """
    add player's incorrect guesses to incorrect_guesses_text.txt
    """
    if len(player["incorrect guesses"]) > 0:
        text_to_write = "<span id='guesses-title'>Incorrect Guesses: </span> <span class='guesses'> {0} </span>".format(
            player["incorrect guesses"])
        with open("active-game-files/incorrect_guesses.txt", "a") as f:
            f.writelines(text_to_write)


def add_host_text(text):
    """
    add text to host.txt
    """
    with open("active-game-files/host.txt", "a") as f:
        f.writelines("{}<br>".format(text))


def add_correct_answer_text(player):
    """
    writes the correct answer to the player's
    question in answer.txt
    """
    question_tuple = player["question"]
    correct_answer = ""
    if question_is_picture_question(question_tuple):
        correct_answer = question_tuple[2]
    else:
        correct_answer = question_tuple[1]

    text_to_write = "The correct answer was: {0}<br>".format(correct_answer)
    with open("active-game-files/answer.txt", "a") as f:
        f.writelines(text_to_write)


def add_eliminated_text(player):
    """
    writes that the player in argument has been 
    eliminated in eliminated.txt
    """
    username = player["username"]
    text_to_write = "{} has been eliminated".format(username)
    with open("active-game-files/eliminated.txt", "a") as f:
        f.writelines(text_to_write)


def add_question_text(question):
    """
    writes the argument to question.txt
    """
    with open("active-game-files/question.txt", "a") as f:
        f.writelines("{}<br>".format(question))


def add_game_over_text():
    """
    writes 'Game over' to game_over.txt
    """
    with open("active-game-files/game_over.txt", "a") as f:
        f.writelines("Game Over")


def get_round_text():
    """
    creates a dictionary with values for all game
    txt files. Key names match the text files
    but with underscores instead of spaces
    """
    round_text_dictionary = {}

    with open("active-game-files/correct.txt", "r") as f:
        correct_text = f.readlines()
        round_text_dictionary["correct text"] = correct_text

    with open("active-game-files/eliminated.txt", "r") as f:
        eliminated_text = f.readlines()
        round_text_dictionary["eliminated text"] = eliminated_text

    with open("active-game-files/answer.txt", "r") as f:
        answer_text = f.readlines()
        round_text_dictionary["answer text"] = answer_text

    with open("active-game-files/host.txt", "r") as f:
        host_text = f.readlines()
        round_text_dictionary["host text"] = host_text

    with open("active-game-files/question.txt", "r") as f:
        question_text = f.readlines()
        round_text_dictionary["question text"] = question_text

    with open("active-game-files/incorrect_guesses.txt", "r") as f:
        incorrect_guesses_text = f.readlines()
        round_text_dictionary["incorrect guesses text"] = incorrect_guesses_text

    with open("active-game-files/game_over.txt", "r") as f:
        game_over_text = f.readlines()
        round_text_dictionary["game over text"] = game_over_text

    return round_text_dictionary


"""
functions for working with json files
"""

def dump_data(player_list):
    """
    adds argument to players.json. Wipes pre-existing content
    """
    with open("active-game-files/players.json", mode="w", encoding="utf-8") as json_data:
        json.dump(player_list, json_data)


def get_json_data():
    """
    returns the list in players.json
    """
    with open("active-game-files/players.json", "r") as json_file:
        json_data = json.load(json_file)
        return json_data


def get_leaderboard_data():
    """
    returns the list in high_scores.json
    """
    with open("data/high_scores.json", "r") as f:
        leaderboard_data = json.load(f)
        return leaderboard_data


def post_leaderboard_data(leaderboard_data):
    """
    adds argument to high_scores.json. Wipes pre-existing data
    """
    with open("data/high_scores.json", mode="w", encoding="utf-8") as f:
        json.dump(leaderboard_data, f)


def get_sorted_scores():
    """
    returns the list of dictionaries in high_scores.json, sorted in
    descending order by each distractions 'score' values
    Code from: https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
    """
    leaderboard_data = get_leaderboard_data()
    sorted_data = sorted(leaderboard_data, reverse=True,
                         key=lambda k: k["score"])
    return sorted_data


def return_player_to_game_data(player_to_return):
    """
    adds argument to players.json. Replaces dictionary with
    the same 'no' value. Each player has unique 'no' value
    """
    game_data = get_json_data()
    player_index = 999

    for player in game_data:
        if player["no"] == player_to_return["no"]:
            player_index = game_data.index(player)

    game_data[player_index] = player_to_return
    dump_data(game_data)


def get_current_player():
    """
    returns dictionary in players.json with a 
    'turn' value of True
    """
    current_player = {}
    game_data = get_json_data()

    for player in game_data:
        if player["turn"] == True:
            current_player = player

    return current_player
    
    

def get_used_questions():
    """
    returns list of question tuples from used_questions.json
    """
    with open("active-game-files/used_questions.json", "r") as f:
        used_questions = json.load(f)
        return used_questions


def initialize_used_question():
    """
    wipes used_questions.json and replaces content 
    with a list with one dictionary. Dictionary 
    must have 'question' key for other functions 
    to work
    """
    question_list = []
    question_list.append({"question": "sample_question"})

    with open("active-game-files/used_questions.json", mode="w", encoding="utf-8") as f:
        json.dump(question_list, f)


def add_to_used_questions(question, used_questions):
    """
    appends question to used_questions, then replaces
    used.question.json contents with appended used_questions
    """
    used_questions.append({"question": question[0]})

    with open("active-game-files/used_questions.json", mode="w", encoding="utf-8") as f:
        json.dump(used_questions, f)
        

def get_previous_player():
    """
    returns the dictionary in players.json with a 
    'previous' value of True
    """
    game_data = get_json_data()
    previous_player = {}

    for player in game_data:
        if player["previous"] == True:
            previous_player = player

    return previous_player


def set_new_chosen_and_previous_player():
    """
    player in players.json with a 'turn' value 
    of True replaced with False but 'previous' 
    set to true. Next player in list (or first player in 
    list if at end of list) has turn set to True. 
    All other players have turn and previous set to False
    """
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
        game_data[player_index + 1]["turn"] = True

    else:
        game_data[0]["turn"] = True

    dump_data(game_data)

def eliminate_dead_players():
    """
    removes player from players.json if their lives value
    is 0. If player removed, adds text saying that player has 
    been removed. Also adds text displaying the correct answer to
    their question
    """
    game_data = get_json_data()
    player_index = 999
    eliminated_player = {}

    for player in game_data:
        if player["lives"] <= 0:
            add_to_leaderboard(player)
            player_index = game_data.index(player)
            add_eliminated_text(player)
            add_correct_answer_text(player)

            eliminated_player = player

    if player_index != 999:
        game_data.pop(player_index)
        dump_data(game_data)

    dump_data(game_data)
    return game_data
    
    
def add_to_leaderboard(player):
    """
    appends high_scores.json with the argument player's
    username and score
    """
    username = player["username"]
    score = player["score"]

    saved_score = {"username": username, "score": score}
    leaderboard_data = get_leaderboard_data()
    leaderboard_data.append(saved_score)

    post_leaderboard_data(leaderboard_data)


def create_game_data(number_of_players):
    """
    initializes players.json file with a list
    containing a dictionary for each player
    """
    player_list = []
    for i in range(number_of_players):
        username = request.form["player-{0}-username".format(i+1)]
        player_object = {
            "username": username,
            "lives": 1,
            "score": 0,
            "question": "",
            "last question correct": True, #determines if a new question is set. Therefore initially set to True
            "turn": False, #first player in list will have this changed to True
            "previous": False,
            "answer": "",
            "no": i+1, #a unique number for identifying each player in the game. Also used for card styling in game.html
            "incorrect guesses": ""
        }
        player_list.append(player_object)
    dump_data(player_list)


def all_players_gone():
    """
    returns True if players.json list empty. Otherwise
    returns False
    """
    game_data = get_json_data()

    if len(game_data) > 0:
        return False
    else:
        return True



"""
functions for setting usernames 
"""


def set_username():
    """
    sets the user's username
    """
    username = input("Please enter your desired username: ")
    # username = request.form["answer"]
    if len(username) > 0:
        print("Hello " + username)
        return(username)
    else:
        print("Please enter a username")
        print("")
        set_username()

"""
functions to rending templates 
"""

def get_col_size(game_data):
    """
    retrieves col size (xs) for player
    cards in  game.html
    """
    players = len(game_data)
    col_size = int(24/players)

    if players == 1:
        col_size = 12

    return col_size


def get_col_sm_size(game_data):
    """
    retrieves size of columns for devices 
    larger than xs (576 px width)
    """
    players = len(game_data)
    col_size = int(12/players)

    return col_size
    
"""
functions for gameplay loop (that are not directly related to JSON files)
"""


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
    elif current_score >= 2:
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
        pictures_tuples_list.append(("/static/img/{}".format(
            pictures_lines[i]), pictures_lines[i+1], pictures_lines[i+2], pictures_lines[i+3]))

    return pictures_tuples_list


def get_questions_answers_keywords(difficulty):
    """
    returns list of tuples in format of (question, answer, keyword)
    read from questions document. Question document selected by
    difficulty. Picture questions in format of (link, question, answer, keyword)
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


def check_question_is_original(question_tuple):
    """
    returns False if argument is in used_questions.json,
    otherwise adds question to used_questions.json and returns True
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


def random_question_tuple(difficulty):
    """
    selects a random tuple from the tuples list
    returns it if it has not already been asked.
    Keeps running until original question found
    WARNING: this creates risk of infinite loop if all
    questions in hard.txt have been asked
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
    if len(question) == 4:
        return True
    else:
        return False


def ask_question():
    """
    asks question to the user
    also adds introduction host text
    """
    current_player = get_current_player()
    game_data = get_json_data()
    number_of_players = len(game_data)

    if number_of_players > 1:
        add_host_text("You're up {}".format(current_player["username"]))

    if not last_question_correct(current_player):
        add_host_text("Let's try that again...")
        add_incorrect_guesses_text(current_player)

    question = current_player["question"]

    if question_is_picture_question(question):
        img_text = "<img src ='{}'>".format(question[0])
        add_question_text(img_text)
        add_question_text(question[1])
    else:
        add_question_text(question[0])


def select_player(game_data):
    """
    returns player from argument with a 'Turn'
    value of True
    """
    chosen_player = {}

    set_new_chosen_and_previous_player()

    for player in (game_data):
        if player["turn"] == True:
            chosen_player = player
            
    return chosen_player


def set_previous_answer():
    """
    called following a post request. Gets the answer
    entered into answer form. The player in players.json
    with a previous value of true has this set as their
    'answer' value. Answer converted to a list of lower case strings
    """
    user_answer = request.form["answer"]
    lower_user_answer = user_answer.lower()
    user_answer_list = lower_user_answer.split()

    previous_player = get_previous_player()
    previous_player["answer"] = user_answer_list

    return_player_to_game_data(previous_player)


def append_and_return_incorrect_guesses_string(player):
    """
    Gets the argument player's 'answer' value. Appends 
    this with the value enterd into answer form. Returns
    appended string
    """
    incorrect_guesses = player["incorrect guesses"]
    last_guess = player["answer"]

    last_guess_string = " ".join(str(word) for word in last_guess)
    new_text = "{0}<br>{1}".format(incorrect_guesses, last_guess_string)
    return new_text


def check_previous_player_answer():
    """
    checks if the previous player's answer contains their question's
    answer keyword. Updates that player's 'last question correct' 
    value accordingly. Adds appropriate text to corrrect.txt. Returns
    True if player was correct, false otherwise
    """
    previous_player = get_previous_player()
    answer = previous_player["answer"]

    question = previous_player["question"]

    if question_is_picture_question(question):
        keyword = question[3]
    else:
        keyword = question[2]

    if keyword in answer:
        add_correct_text("Correct!")
        previous_player["last question correct"] = True
        previous_player["incorrect guesses"] = ""
        return_player_to_game_data(previous_player)
        return True
    else:
        add_incorrect_text("Incorrect")
        previous_player["last question correct"] = False
        previous_player["incorrect guesses"] = append_and_return_incorrect_guesses_string(
            previous_player)
        return_player_to_game_data(previous_player)
        return False



def last_question_correct(player):
    """
    returns the boolean value of the argument player's 
    'last question correct' 
    """
    if player["last question correct"] == True:
        return True

    else:
        return False


def set_player_question():
    """
    sets question for the player in players.json with a 'turn' value of 
    True. If that player has a 'last question correct' value of False, no 
    new question is set
    """
    current_player = get_current_player()

    if last_question_correct(current_player):
        difficulty = set_difficulty(current_player["score"])
        current_player["question"] = random_question_tuple(difficulty)

    return_player_to_game_data(current_player)


def update_lives_and_score(correct):
    """
    effects previous player. Correct is a boolean value.
    If True, add 1 to player's score. If false, subtract one
    from player's lives
    """
    previous_player = get_previous_player()

    if correct:
        previous_player["score"] += 1
    else:
        previous_player["lives"] -= 1

    return_player_to_game_data(previous_player)

"""
routing functions
"""

@app.route("/", methods=["GET"])
def index():
    """
    gets template for landing page. If user clicks 
    'start game' button (and therefore players != None), 
    they are redirected to the set usernames page for the 
    number of players (1-4 inclusive) they selected
    """
    if request.method == "GET":
        round_text = get_round_text()
        players = request.args.get("players")
        if players == None:
            return render_template("index.html")
        else:
            return redirect("/setusernames/{}".format(players))


@app.route("/setusernames/<players>", methods=["POST", "GET"])
def set_username_page(players):
    """
    gets template for set usernames page. The number of text
    areas is determined by the value of <players>. After posting 
    usernames, users are redirected to the game page
    """
    players = int(players)

    if request.method == "POST":
        create_game_data(players)
        return redirect("/game")

    return render_template("usernames.html", players=players)


@app.route("/leaderboard")
def show_leaderboard():
    """
    gets sorted scores and renders the top 30 scores as 
    a table using the leaderboard.html template
    """
    leaderboard_data = get_sorted_scores()
    return render_template("leaderboard.html", leaderboard_data=leaderboard_data)


@app.route("/game", methods=["GET", "POST"])
def render_game():
    """
    main game loop
    """

    wipe_game_text()
    game_data = get_json_data()

    col_size = get_col_size(game_data)
    col_sm_size = get_col_sm_size(game_data)
 
    if request.method == "POST":#only runs after form has been submitted once. Won't run first time page is loaded
        set_new_chosen_and_previous_player()
        set_previous_answer()
        was_correct = check_previous_player_answer()
        update_lives_and_score(was_correct)
        eliminate_dead_players()
        
        
        if not all_players_gone():
            set_player_question()
            ask_question()

        game_data = get_json_data()
    
    else: #runs the first time the page is loaded, before the users submit any answers. Doesn't run again

        initialize_used_question()
        game_data[0]["turn"] = True
        dump_data(game_data)
        set_player_question()
        ask_question()

    round_text = get_round_text()
    
    if all_players_gone(): #adds game over and correct answer text and renders leaderboard template 
        wipe_game_text(True)
        add_game_over_text()
        leaderboard_data = get_sorted_scores()
        round_text = get_round_text()
        return render_template("leaderboard.html", leaderboard_data=leaderboard_data, answer_text="".join(round_text["answer text"]), game_over_text="".join(round_text["game over text"]))

    round_text = get_round_text()
    game_data = get_json_data()

    return render_template("game.html", correct_text="".join(round_text["correct text"]), eliminated_text="".join(round_text["eliminated text"]), answer_text="".join(round_text["answer text"]), host_text="".join(round_text["host text"]), question_text="".join(round_text["question text"]), incorrect_guesses_text="".join(round_text["incorrect guesses text"]),   col_size=col_size, col_sm_size=col_sm_size,  game_data=game_data)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

