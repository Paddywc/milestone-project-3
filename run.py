import os

from flask import Flask, render_template, request, redirect

from game_text_functions import wipe_game_text, add_game_over_text, get_round_text
from gameplay_loop import ask_question, set_previous_answer, check_previous_player_answer, set_player_question, \
    update_lives_and_score, get_correct_answer
from json_functions import dump_data, get_json_data, get_sorted_scores, initialize_used_question, \
    set_new_chosen_and_previous_player, eliminate_dead_players, create_game_data, all_players_gone

app = Flask(__name__)

app.secret_key = 'some_secret'

"""
username functions 
"""


def set_username():
    """
    sets the user's username
    """
    # username = input("Please enter your desired username: ")
    username = request.form["answer"]
    if len(username) > 0:
        print("Hello " + username)
        return username
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

    if players == 1:
        col_size = 12

    else:
        col_size = 6

    return col_size


def get_col_sm_size(game_data):
    """
    retrieves size of columns for devices 
    larger than xs (576 px width)
    """
    players = len(game_data)
    col_size = int(12 / players)

    return col_size


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
        players = request.args.get("players")
        if players is None:
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

    if request.method == "POST":  # only runs after form has been submitted once. Won't run first time page is loaded
        set_new_chosen_and_previous_player()
        set_previous_answer()
        was_correct = check_previous_player_answer()
        update_lives_and_score(was_correct)
        eliminated_player = eliminate_dead_players()
        if eliminated_player:
            get_correct_answer(eliminated_player)

        if not all_players_gone():
            set_player_question()
            ask_question()

        game_data = get_json_data()

    else:  # runs the first time the page is loaded, before the users submit any answers. Doesn't run again

        initialize_used_question()
        game_data[0]["turn"] = True
        dump_data(game_data)
        set_player_question()
        ask_question()

    if all_players_gone():  # adds game over and correct answer text and renders leaderboard template
        wipe_game_text(True)
        add_game_over_text()
        leaderboard_data = get_sorted_scores()
        round_text = get_round_text()
        return render_template("leaderboard.html", leaderboard_data=leaderboard_data,
                               answer_text="".join(round_text["answer text"]),
                               game_over_text="".join(round_text["game over text"]))

    col_size = get_col_size(game_data)
    col_sm_size = get_col_sm_size(game_data)

    round_text = get_round_text()
    game_data = get_json_data()

    return render_template("game.html", correct_text="".join(round_text["correct text"]),
                           eliminated_text="".join(round_text["eliminated text"]),
                           answer_text="".join(round_text["answer text"]), host_text="".join(round_text["host text"]),
                           question_text="".join(round_text["question text"]),
                           incorrect_guesses_text="".join(round_text["incorrect guesses text"]), col_size=col_size,
                           col_sm_size=col_sm_size, game_data=game_data)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
