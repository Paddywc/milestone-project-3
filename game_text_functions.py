def wipe_game_text(game_over=False):
    """
    wipes all game text files
    if game over == True, don't wipe
    correct_answer. This is so the final
    player's correct answer can be displayed
    in the leaderboard page
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


def add_correct_answer_text(correct_answer):
    """
    writes the correct answer to the player's
    question in answer.txt
    """

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
