import unittest
import run
import json


class testGame(unittest.TestCase):
    
    
    def test_wiped_files_content_length_is_zero(self):
        """
        test to check that after calling wipe_files, the length
        of the content string is 0
        """
        text = "test text"
        
        run.add_incorrect_text(text)
        run.add_host_text(text)
        run.add_question_text(text)
        run.add_game_over_text()
        
        round_text = run.get_round_text()
        
        incorrect_text = round_text["correct text"]
        host_text = round_text["host text"]
        question_text = round_text["question text"]
        game_over_text= round_text["game over text"]
        
        self.assertTrue(len(incorrect_text)>0)
        self.assertTrue(len(host_text)>0)
        self.assertTrue(len(question_text)>0)
        self.assertTrue(len(game_over_text)>0)
        
        run.wipe_game_text()

        round_text = run.get_round_text()
        
        incorrect_text = round_text["correct text"]
        host_text = round_text["host text"]
        question_text = round_text["question text"]
        game_over_text= round_text["game over text"]
        
        self.assertTrue(len(incorrect_text)==0)
        self.assertTrue(len(host_text)==0)
        self.assertTrue(len(question_text)==0)
        self.assertTrue(len(game_over_text)==0)
        
        
    def test_game_over_answer_not_wiped(self):
        """
        test to check that answer.txt is not wiped if
        True is entred as an argument into wipe_game_test()
        """
        sample_text = "sample text"
        
        run.wipe_game_text()
        
        with open("active-game-files/answer.txt", "a") as f:
            f.writelines(sample_text) 
            
        run.wipe_game_text(True)
        round_text = run.get_round_text()
        answer_text = "".join(round_text["answer text"])
        self.assertEqual(answer_text, sample_text)
        
        
    def test_dump_data_and_get_data_return_equal_values(self):
        """
        test to check that the data entered into dump data will 
        be the same as the value returned by get_json_data
        """
        data_to_dump = [{
            "should be 1": 1,
            "should be false": False,
            "should be 'test'": "test"
            }, {
                "another": "dictionary"
            }]
            
        run.dump_data(data_to_dump)
        
        retrieved_data = run.get_json_data()
        retrived_dictionary = retrieved_data[0]
        
        self.assertEqual(len(retrieved_data), 2)
        self.assertEqual(retrived_dictionary["should be 1"], 1)
        self.assertEqual(retrived_dictionary["should be false"], False)
        self.assertEqual(retrived_dictionary["should be 'test'"], "test")
        

    def test_col_size_returns_int_that_24_is_devisable_by(self):
        """
        test to check that get_col_size and get_col_sm_size returns
        an int. 24 % that int should be 0
        """
        list_length_1 = [1]
        list_length_3 = [0,1,2]
        
        xs_one_list = run.get_col_size(list_length_1)
        xs_three_list = run.get_col_size(list_length_3)
        sm_one_list = run.get_col_sm_size(list_length_1)
        sm_three_list = run.get_col_sm_size(list_length_3)
        
        self.assertTrue(type(xs_one_list) is int)
        self.assertTrue(type(xs_three_list) is int)
        self.assertTrue(type(xs_one_list) is int)
        self.assertTrue(type(xs_three_list) is int)
        self.assertEqual(24 % xs_one_list, 0)
        self.assertEqual(24 % xs_three_list, 0)
        self.assertEqual(24 % sm_one_list, 0)
        self.assertEqual(24 % sm_three_list, 0)
        
        
        
    def test_used_questions_file_initializes_with_single_entry_list(self):
        """
        test to check that initialize_used_question() creates a list
        with exactly one entry
        """
        run.initialize_used_question()
        with open("active-game-files/used_questions.json", "r") as f:
            result = json.load(f)
        self.assertTrue(type(result) is list)
        self.assertEqual(len(result), 1)
        
        
    def test_initial_used_questions_list_contains_questions_dictionary (self):
        """
        test to check that initialize_used_question() creates a list
        with an entry that is a dictionary and has a 'question' key
        """
        run.initialize_used_question()
        with open("active-game-files/used_questions.json", "r") as f:
            result = json.load(f)
            only_result = result[0]
        self.assertNotEqual(only_result["question"], None)
        
        
    def test_get_current_player_does_not_return_players_with_turn_false(self):
        """
        test to check that get_current_player won't return players with a turn of
        false
        """
        one_true = [{"turn" : False}, {"turn": False}, {"turn": True}, {"turn": False}]
        run.dump_data(one_true)
        one_true_result = run.get_current_player()
        self.assertNotEqual(one_true_result["turn"], False)
        self.assertTrue(one_true_result["turn"])
        
        all_false = [{"turn" : False}, {"turn": False}]
        run.dump_data(all_false)
        all_false_result = run.get_current_player()
        self.assertEqual(all_false_result, {})
        
    def check_last_question_correct_returns_accurate_boolean(self):
        """
        test to check that last_question_correct returns a
        boolean. Should be true if dictionary's 
        'last question correct' value == True
        """
        first_test_value = "test"
        second_test_value = [1,2,3]
        should_return_false = {"last question correct": False}
        should_rreturn_true = {"last question correct": True}
        
        self.assertTrue(type(run.last_question_correct(first_test_value)), bool)
        self.assertTrue(type(run.last_question_correct(second_test_value)), bool)
        self.assertFalse(run.last_question_correct(should_return_false))
        self.assertTrue(run.last_question_correct(should_rreturn_true))
        
        
        
    def test_set_difficulty_returns_string(self):
        """
        test to check if the set_difficulty 
        function returns a string
        """
        response = run.set_difficulty(3)
        self.assertTrue(isinstance(response, str))
        
    def test_correct_difficulty_determined(self):
        """
        tests if set_difficulty returns 
        <2 Easy, <6 Normal, <8 Picture >7 Hard
        """
        self.assertEqual(run.set_difficulty(0),"Easy")
        self.assertEqual(run.set_difficulty(1),"Easy")
        self.assertEqual(run.set_difficulty(2),"Normal")
        self.assertEqual(run.set_difficulty(3),"Normal")
        self.assertEqual(run.set_difficulty(4),"Normal")
        self.assertEqual(run.set_difficulty(5),"Normal")
        self.assertEqual(run.set_difficulty(6),"Picture")
        self.assertEqual(run.set_difficulty(7),"Picture")
        self.assertEqual(run.set_difficulty(8),"Hard")
        self.assertEqual(run.set_difficulty(9),"Hard")
        self.assertEqual(run.set_difficulty(10),"Hard")
        self.assertEqual(run.set_difficulty(11),"Hard")
        
    
    def test_return_player_to_game_replaces_previous_value(self):
        """
        test to check that return_player_to_game_data replaces 
        the player entered as an argument. The player should be
        replaced in the dictionary, not appended
        """
        test_game_data = [
            {
                "no": 10,
                "test": "original value",
                
            },
            { "no": 5,
            "test": "original value"
            }
            ]
            
        run.dump_data(test_game_data)
        original_data = run.get_json_data()
        replacement_player = {
            "no": 5,
            "test": "success!",
            "additional key": True
        }
        
        run.return_player_to_game_data(replacement_player)
        new_data = run.get_json_data()
        
        self.assertEqual(len(original_data), len(new_data))
        self.assertNotEqual(original_data, new_data)
        self.assertEqual(new_data[1]["test"], "success!")
        self.assertTrue(new_data[1]["additional key"])
    
    
    def test_ask_question_writes_current_player_question(self):
        """
        test to check that ask_question writes the appropriate 
        question tuple entry for the player with a turn value of
        True
        """
        run.wipe_game_text()
        
        test_player_data =[{"previous": False, "last question correct": True, "no": 1, "incorrect guesses": "", "username": "Chris", "turn": False, "lives": 2, "question": ["This kind of coat can you put on only when it is wet. What is it?", "A coat of paint", "paint"], "answer": ["a", "paint", "of", "coat"], "score": 5}, {"previous": True, "last question correct": False, "no": 2, "incorrect guesses": "<br>the dictionary", "username": "Stewie", "turn": False, "lives": 1, "question": ["I am a word. If you pronounce me rightly, it will be wrong. If you pronounce me wrong it is right? What word am I?", "Wrong", "wrong"], "answer": ["the", "dictionary"], "score": 4}, {"previous": False, "last question correct": True, "no": 3, "incorrect guesses": "", "username": "Meg", "turn": True, "lives": 2, "question": ["It has Eighty-eight keys but can't open a single door? What is it?", "A piano", "piano"], "answer": "", "score": 4}]
        
        run.dump_data(test_player_data)
        
        run.ask_question()
        
        result_should_be = "It has Eighty-eight keys but can't open a single door? What is it?<br>"
        
        with open("active-game-files/question.txt", "r") as f:
            result= f.readlines()
            
            
        self.assertEqual("".join(result), result_should_be)
        
        
    def test_link_first_picture_value(self):
        """
        test to check if every index0 of a picture tuple
        is a link to the picture file. As both .jpg and
        .png end in 'g', this should be the last character 
        """
        pictures_tuples_list = run.get_picture_tuple_list()
        for tuple_entry in pictures_tuples_list:
            first_entry = tuple_entry[0]
            index_of_last_char = len(first_entry) -1
            self.assertEqual(first_entry[index_of_last_char], "g")
            
    
    def test_correctly_determine_picture_question(self):
        """
        test to check if question_is_picture_question returns
        true if picture question and false otherwise
        """
        pictures_tuples_list = run.get_picture_tuple_list()
        picture_question = pictures_tuples_list[0]
        text_question = run.random_question_tuple("Hard")
        
        self.assertTrue(run.question_is_picture_question(picture_question))
        self.assertFalse(run.question_is_picture_question(text_question))
        
    def test_picture_difficulty_returns_picture_tuple(self):
        """
        test to check that a picture tuple list is returned if 
        picture is eneted as an argument into get_questions_answers_keywords
        """
        returned_tuple_list = run.get_questions_answers_keywords("Picture")
        first_entry = returned_tuple_list[0]
        self.assertEqual(len(first_entry), 4)
        
    
        
    def test_can_add_host_text(self):
        """
        test to check that add_host_text adds the entered
        text into host.txt
        """
        run.wipe_game_text()
        test_text = "test text"
        
        run.add_host_text(test_text)
        
        with open("active-game-files/host.txt", "r") as f:
            result= f.readlines()
            
            
        self.assertEqual("".join(result), "{0}<br>".format(test_text))
        
    def test_can_add_incorrect_guesses(self):
        """
        test to check that add_incorrect_guesses_text writes 
        the incorrect guesses of the player entered as an 
        argument. Guesses should be written to incorrect_guesses.txt
        """
        test_player = {"username": "test", "incorrect guesses" : "<br>a wrong answer<br>another incorrect answer"}
        result_should_be = "<span id='guesses-title'>Incorrect Guesses: </span> <span class='guesses'> <br>a wrong answer<br>another incorrect answer </span>"
        
        run.wipe_game_text()
        run.add_incorrect_guesses_text(test_player)
        
        with open("active-game-files/incorrect_guesses.txt", "r") as f:
            result= f.readlines()
            
        self.assertEqual("".join(result), result_should_be)
        
        
    def test_chosen_player_changes_to_previous_player(self):
        """
        test to check that set_new_chosen_and_previous_player()
        the player with turn: True has turn changed to False and
        previous turned to true
        """
        test_players = [{"username": "p1", "turn": False, "previous": True}, {"username": "p2", "turn": True, "previous": False}, {"username": "p3", "turn": False, "previous": False}]
        
        run.dump_data(test_players)
        test_players = run.get_json_data()
        
        self.assertTrue(test_players[1]["turn"])
        self.assertFalse(test_players[1]["previous"])
        
        run.set_new_chosen_and_previous_player()
        test_players = run.get_json_data()
        
        self.assertFalse(test_players[1]["turn"])
        self.assertTrue(test_players[1]["previous"])
        
    
    def test_new_chosen_and_previous_player_can_restart_index(self):
        """
        test to check that set_new_chosen_and_previous_player returns
        to index 0 when and only when the final player in the list has
        a turn value of True
        """
        should_not_be_index_0_turn =[{"username": "p1", "turn": False, "previous": True}, {"username": "p2", "turn": True, "previous": False}, {"username": "p3", "turn": False, "previous": False}, {"username": "p4", "turn": False, "previous": False}]
        
        run.dump_data(should_not_be_index_0_turn)
        run.set_new_chosen_and_previous_player()
        result = run.get_json_data()
        
        self.assertFalse(result[0]["turn"])
        
        should_be_index_0_turn =[{"username": "p1", "turn": False, "previous": False}, {"username": "p2", "turn": False, "previous": False}, {"username": "p3", "turn": False, "previous": True}, {"username": "p4", "turn": True, "previous": False}]
        
        run.dump_data(should_be_index_0_turn)
        run.set_new_chosen_and_previous_player()
        result = run.get_json_data()
        
        self.assertTrue(result[0]["turn"])
        
        
    def test_get_previous_player_returns_empty_dictionary_if_no_previous_player(self):
        """
        test to check that get_previous_player returns an empty dictionary if json 
        file contains no previous player. Otherwise should return the player with a 
        previous value of True
        """
        no_previous_player = [{"username": "p1", "turn": False, "previous": False}, {"username": "p2", "turn": True, "previous": False}, {"username": "p3", "turn": False, "previous": False}, {"username": "p4", "turn": False, "previous": False}]
        run.dump_data(no_previous_player)
        previous_player = run.get_previous_player()
        self.assertEqual(previous_player, {})
        
        a_previous_player = [{"username": "p1", "turn": False, "previous": True}, {"username": "p2", "turn": True, "previous": False}, {"username": "p3", "turn": False, "previous": False}, {"username": "p4", "turn": False, "previous": False}]
        run.dump_data(a_previous_player)
        previous_player = run.get_previous_player()
        self.assertEqual(previous_player["username"], "p1")
        
        
    def test_check_previous_answer_correctly_grades_answer(self):
        """
        test to check that check_previous_player_answer adds 
        'Correct!' to correct.txt if the players answer contains 
        the questions keyword. If it does not, it should write 'incorrect'
        """
        run.wipe_game_text()
        should_write_incorrect = [{"question": ["What starts with a 'P', ends with an 'E'and has thousands of letters?", "The Post Office", "post"],  "answer": ["wrong", "answer"],  "previous": True, "incorrect guesses": "", "no": 1}]
        run.dump_data(should_write_incorrect)
        run.check_previous_player_answer()
        with open("active-game-files/correct.txt", "r") as f:
           result= f.readlines()
        result_should_be = "<span class='incorrect'>Incorrect</span>"
        self.assertEqual("".join(result), result_should_be)
        
        
        run.wipe_game_text()
        should_write_incorrect = [{"question": ["What starts with a 'P', ends with an 'E'and has thousands of letters?", "The Post Office", "post"],  "answer": ["test", "post"],  "previous": True, "incorrect guesses": "", "no": 1}]
        run.dump_data(should_write_incorrect)
        run.check_previous_player_answer()
        with open("active-game-files/correct.txt", "r") as f:
           result= f.readlines()
        result_should_be = "<span class='correct'>Correct!</span>"
        self.assertEqual("".join(result), result_should_be)
        
        
        
    def test_correctly_add_or_sum_score_and_lives(self):
        """
        test to check that update_lives_and_score adds 1
        to the previous player's score if True is entered 
        as an argument. If false is entered, it should 
        subtract 1 from the previous player's life
        """
        test_data = [{"previous": True, "lives":0, "score":0, "no":1}]
        run.dump_data(test_data)
        
        to_add_to_score = 5
        to_subtract_from_lives = 3
        
        for x in range(to_add_to_score):
            run.update_lives_and_score(True)
            
        for y in range(to_subtract_from_lives):
            run.update_lives_and_score(False)
        
        result= run.get_json_data()

        self.assertEqual(result[0]["score"], to_add_to_score)
        self.assertEqual(result[0]["lives"], (- to_subtract_from_lives))
        
        
    def test_players_with_0_lives_are_eliminated(self):
        """
        test to check that eliminate_dead_players will remove a
        player with 0 lives
        """
        no_dead_players = [{"no": 1, "lives" : 2, "username": "test"},{"no": 2, "lives" : 1, "username": "test"}, {"no": 3, "lives" : 6, "username": "test"}]
        
        run.dump_data(no_dead_players)
        run.eliminate_dead_players()
        result = run.get_json_data()
        self.assertEqual(len(no_dead_players), len(result))
        
        one_dead_player = [{"no": 1, "lives" : 2, "username": "test"},{"no": 2, "question": ("", "", "", ""), "score": 2, "lives" : 0, "username": "test"}, {"no": 3, "lives" : 6, "username": "test"}]
        
        run.dump_data(one_dead_player)
        run.eliminate_dead_players()
        result = run.get_json_data()
        self.assertEqual(len(result), len(one_dead_player)-1)
        for player in result:
            self.assertNotEqual(player["no"], 2)
            
            
    def test_elimination_text_correctly_identifies_player(self):
        """
        test to check that add_eliminated_text correctly identifies
        the username of the player that was eliminated
        """
        run.wipe_game_text
        test_game_data = [{"no": 1, "lives" : 2, "username": "wrong name"},{"no": 2, "question": ("", "", "", ""), "score": 2, "lives" : 0, "username": "success"}, {"no": 3, "lives" : 6, "username": "not this player"}]
        run.dump_data(test_game_data)
        run.eliminate_dead_players()
        with open("active-game-files/eliminated.txt", "r") as f:
           result= f.readlines()
           
        result_should_be = "success has been eliminated"
        self.assertEqual("".join(result), result_should_be)
        
        
    
    def test_get_leaderboard_data_returns_dictionary_with_username_score(self):
        """
        test to check that get_leaderboard_data() returns a list of 
        dictionaries. Each dictionary should have a username and score 
        value only
        """
        returned_list = run.get_leaderboard_data()
        
        for dictionary in returned_list:
            self.assertTrue(dictionary["username"])
            self.assertTrue(dictionary["score"] >=0)
            self.assertEqual(len(dictionary), 2)
        
    
    def test_post_leaderboard_adds_values_to_high_scores(self):
        """
        test to check that post_leaderboard_data adds its argument
        to high_scores.json, wipes other data
        """
        orginal_leaderboard_data = run.get_leaderboard_data()
        length_of_original_leaderboard_data = len(orginal_leaderboard_data)
        
        empty_leaderboard_data = []
        run.post_leaderboard_data(empty_leaderboard_data)
        
        new_leaderboard_data= run.get_leaderboard_data()
        self.assertEqual(len(new_leaderboard_data), 0)
        
        run.post_leaderboard_data(orginal_leaderboard_data)
        returned_leaderboard_data = run.get_leaderboard_data()
        self.assertEqual(len(returned_leaderboard_data), length_of_original_leaderboard_data)
        
        
    def test_add_to_leaderboard_appends_leaderboard_data(self):
        """
        test to check that all_to_leaderboard appends, but doesn't
        wipe, high_scores.json
        """
        orginal_leaderboard_data = run.get_leaderboard_data()
        length_of_original_leaderboard_data = len(orginal_leaderboard_data)
        
        run.add_to_leaderboard({"username": "unique test name", "score": 2})
        new_leaderboard_data = run.get_leaderboard_data()
        length_of_new_leaderboard_data = len(new_leaderboard_data)
        
        self.assertEqual(length_of_new_leaderboard_data, length_of_original_leaderboard_data+1)
        found_new_data = False
        
        for player in new_leaderboard_data:
            if player["username"] == "unique test name":
                found_new_data = True
                
        self.assertTrue(found_new_data)
        run.post_leaderboard_data(orginal_leaderboard_data)
        
        
    def test_add_correct_answer_test_write_answer_for_both_picture_and_text_questions(self):
        """
        test to check that add_correct_answer_text correctly posts the answer of the 
        argument player's question for both picture and text questions
        """
        run.wipe_game_text()
        
        text_question_plyaer = {"question": ["I have rivers, but do not have water. I have dense forests, but no trees and animals. I have cities, but no people live in those cities. What am I?", "A map", "map"]}
        picture_question_player = {"question":["/static/img/how-many-balls.jpg", "Can you count the number of balls in picture below?", "30 (16+9+4+1)", "30"]}
        
        run.add_correct_answer_text(text_question_plyaer)
        all_text = run.get_round_text()
        answer_text = "".join(all_text["answer text"])
        answer_should_be = "The correct answer was: A map<br>"
        self.assertEqual(answer_text, answer_should_be)
        
        run.wipe_game_text()
        run.add_correct_answer_text(picture_question_player)
        all_text = run.get_round_text()
        answer_text = "".join(all_text["answer text"])
        answer_should_be = "The correct answer was: 30 (16+9+4+1)<br>"
        self.assertEqual(answer_text, answer_should_be)
        
    def test_all_players_gone_returns_accurate_boolean(self):
        """
        test to check that all_players_gone returns a 
        boolean. Should be False if players.json is not 
        empty. Otherwise should be True
        """
        result = run.all_players_gone()
        self.assertEqual(type(result), bool)
        
        empty_list = []
        run.dump_data(empty_list)
        self.assertTrue(run.all_players_gone())
        
        not_empty_list = [1,2,3]
        run.dump_data(not_empty_list)
        self.assertFalse(run.all_players_gone())
        
        
    def test_get_soted_scores_returns_list_of_objects_sorted_by_descending_score(self):
        """
        test to check that get_sorted_scores returns a list of object where each 
        object's score value is greater than or equal to the following object
        """
        sorted_scores = run.get_sorted_scores()
        
        for i in range(len(sorted_scores)-1):
            self.assertTrue(sorted_scores[i]["score"] >= sorted_scores[i+1]["score"])
        