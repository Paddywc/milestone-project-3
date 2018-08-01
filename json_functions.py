import json

from flask import request

from game_text_functions import add_eliminated_text, add_correct_answer_text

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
        if player["turn"]:
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
    question_list = [{"question": "sample_question"}]

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
        if player["previous"]:
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
        if player["turn"]:
            player["previous"] = True
            player_index = game_data.index(player)
            player["turn"] = False

    if player_index < number_of_players - 1:
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
    eliminated_player = False

    for player in game_data:
        if player["lives"] <= 0:
            add_to_leaderboard(player)
            player_index = game_data.index(player)
            add_eliminated_text(player)
            eliminated_player = player
            

    if player_index != 999:
        game_data.pop(player_index)
        dump_data(game_data)

    dump_data(game_data)
    return eliminated_player


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
        username = request.form["player-{0}-username".format(i + 1)]
        player_object = {
            "username": username,
            "lives": 3,
            "score": 0,
            "question": "",
            "last question correct": True,  # determines if a new question is set. Therefore initially set to True
            "turn": False,  # first player in list will have this changed to True
            "previous": False,
            "answer": "",
            "no": i + 1,
            # a unique number for identifying each player in the game. Also used for card styling in game.html
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
