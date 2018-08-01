from random import choice

from flask import request

from game_text_functions import add_host_text, add_incorrect_guesses_text, add_question_text, add_correct_text, \
    add_incorrect_text, add_correct_answer_text
from json_functions import get_used_questions, add_to_used_questions, get_current_player, get_json_data, \
    set_new_chosen_and_previous_player, get_previous_player, return_player_to_game_data


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
            pictures_lines[i]), pictures_lines[i + 1], pictures_lines[i + 2], pictures_lines[i + 3]))

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
            tuples_list.append((doc_lines[i], doc_lines[i + 1], doc_lines[i + 2]))

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

    while not found_original_question:

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


def get_correct_answer(player):
    """
    gets the correct answer for the players question,
    then adds it to the answer text
    """
    question_tuple = player["question"]
    if question_is_picture_question(question_tuple):
        correct_answer = question_tuple[2]
    else:
        correct_answer = question_tuple[1]

    add_correct_answer_text(correct_answer)


def select_player(game_data):
    """
    returns player from argument with a 'Turn'
    value of True
    """
    chosen_player = {}

    set_new_chosen_and_previous_player()

    for player in game_data:
        if player["turn"]:
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
    this with the value entered into answer form. Returns
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
    value accordingly. Adds appropriate text to correct.txt. Returns
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
    if player["last question correct"]:
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
