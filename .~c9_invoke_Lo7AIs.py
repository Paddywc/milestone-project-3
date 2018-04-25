import unittest
import run
from unittest.mock import patch
from io import StringIO




class testUsernames(unittest.TestCase):
    
    @patch("run.set_username" , return_value="Paddy")
  
    def test_username_is_input(self, input):
        self.assertEqual(run.set_username(), "Paddy")
        
    # def test_username_not_empty(self):
    #     """
    #     test to ensure empty inputs are rejected as usernames
    #     """
    #     test_username = run.set_username()
    #     username_length = len(test_username)
    #     self.assertTrue(username_length != 0)
    
    @patch("run.set_multiple_usernames" , return_value="name")
   
        
        
    def test_username_list_length_of_input(self, input):
        """
        tests that set_multiple_usernames returns
        a list that is the same length as the argument
        """
        username_list = run.set_multiple_usernames(4)
        length_of_list = len(username_list)

        self.assertEqual(length_of_list, 4)
        
    def test_multiple_users_correctly_recognized(self):
        """
        test to check if multiple_users returns true
        when a list of users is entered and false when
        a string is entered
        """
        self.assertFalse(run.multiple_users("Paddy"))
        self.assertTrue(run.multiple_users(["Paddy", "Wilfred"]))
     
        
   
    

    
class testQuestionsAnswersKeyWords(unittest.TestCase):
    
    
    def test_if_list_returned(self):
        """
        test to see if function returns
        a list
        """
        
        returned_list = run.get_questions_answers_keywords("Easy")
        self.assertTrue(type(returned_list) is list)
        
    def test_if_list_of_tuples(self):
        """
        test to check if returned list contains
        only tuples
        """
        returned_list = run.get_questions_answers_keywords("Easy")
        for entry in returned_list:
            self.assertTrue(type(entry) is tuple)

        
    
    def test_no_newline_text(self):
        """
        tests if '\n' appears in the question
        fails if it does
        """
        
        test_questions = run.get_questions_answers_keywords("Normal")
        self.assertNotIn("\n", test_questions[0])
        self.assertNotIn("\n", test_questions[3])
        self.assertNotIn("\n", test_questions[4])
        
        
    
    def test_question_is_a_question(self):
        """
        tests to ensure that the questions list only
        contains lines ending in a question mark
        """
        
        test_questions_answers_keywords = run.get_questions_answers_keywords("Easy");
        for entry in test_questions_answers_keywords:
            question = entry[0]
            index_of_last_char = len(question)-1
            self.assertEqual(question[index_of_last_char], "?")
            
        test_questions_answers_keywords = run.get_questions_answers_keywords("Normal");
        for entry in test_questions_answers_keywords:
            question = entry[0]
            index_of_last_char = len(question)-1
            self.assertEqual(question[index_of_last_char], "?")
            
        test_questions_answers_keywords = run.get_questions_answers_keywords("Hard");
        for entry in test_questions_answers_keywords:
            question = entry[0]
            index_of_last_char = len(question)-1
            self.assertEqual(question[index_of_last_char], "?")
            
            
    def test_correct_file_chosen(self):
        """
        tests if the correct file with chosen for 
        the difficulty by verifying that index[0]
        of the first tuple is the first line of
        the appropriate file
        """
        
        easy_tuple_list= run.get_questions_answers_keywords("Easy")
        normal_tuple_list= run.get_questions_answers_keywords("Normal")
        hard_tuple_list= run.get_questions_answers_keywords("Hard")
        
        first_line_easy_doc = "What goes up but never goes down?"
        first_line_normal_doc = "It is higher without the head, than with it. What is it?"
        first_line_hard_doc = "A cloud is my mother, the wind is my father, my son is the cool stream, and my daughter is the fruit of the land. A rainbow is my bed, the earth my final resting place, and I am the torment of man. What am I?"
        
        self.assertEqual(easy_tuple_list[0][0], first_line_easy_doc)
        self.assertEqual(normal_tuple_list[0][0], first_line_normal_doc)
        self.assertEqual(hard_tuple_list[0][0], first_line_hard_doc)
        
            
    def test_if_keyword_only_one_word(self):
        """
        test to confirm that keyword entries 
        don't contain spaces
        """
        
        test_questions_answers_keywords = run.get_questions_answers_keywords("Easy")
        for entry in test_questions_answers_keywords:
            keyword = entry[2]
            self.assertNotIn(" ", keyword)
            
        test_questions_answers_keywords = run.get_questions_answers_keywords("Normal")
        for entry in test_questions_answers_keywords:
            keyword = entry[2]
            self.assertNotIn(" ", keyword)
            
        test_questions_answers_keywords = run.get_questions_answers_keywords("Hard")
        for entry in test_questions_answers_keywords:
            keyword = entry[2]
            self.assertNotIn(" ", keyword)
            
        test_questions_answers_keywords = run.get_questions_answers_keywords("Picture")
        for entry in test_questions_answers_keywords:
            keyword = entry[3]
            self.assertNotIn(" ", keyword)
            
            
    def test_lowercase_answer_contains_keyword(self):
        """
        to to check that all keywords are 
        included in the answer
        """
        
        test_questions_answers_keywords = run.get_questions_answers_keywords("Easy");
        for entry in test_questions_answers_keywords:
            answer = entry[1].lower()
            keyword = entry[2]
            self.assertIn(keyword , answer)
            
        test_questions_answers_keywords = run.get_questions_answers_keywords("Normal");
        for entry in test_questions_answers_keywords:
            answer = entry[1].lower()
            keyword = entry[2]
            self.assertIn(keyword , answer)
            
              
        test_questions_answers_keywords = run.get_questions_answers_keywords("Hard");
        for entry in test_questions_answers_keywords:
            answer = entry[1].lower()
            keyword = entry[2]
            self.assertIn(keyword , answer)
            
    
    
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
        used_questions = []
        text_question = run.random_question_tuple("Hard", used_questions)
        
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
        
    
    
    def test_questions_randomly_selected(self):
        
        """
        checks if two complete lists of randomly generated
        tuples are not equal 
        """
     
        questions_list = run.get_questions_answers_keywords("Easy")
        
        first_list = []
        second_list = []
        first_list_used_questions = []
        second_list_used_questions = []
        
        for i in range(len(questions_list)):
            first_list.append(run.random_question_tuple("Easy", first_list_used_questions))
        
        for i in range(len(questions_list)):
            second_list.append(run.random_question_tuple("Easy", second_list_used_questions))
            
        self.assertNotEqual(first_list, second_list)
        
    def test_repeat_questions_return_false(self):
        """
        Test to see if check_question_is_original returns
        false if the question has already been asked
        """
        questions_list = run.get_questions_answers_keywords("Easy") 
        question = questions_list[0]
        used_questions = []
        used_questions = run.check_question_is_original(question, used_questions)
        
        self.assertFalse(run.check_question_is_original(question, used_questions))
    
    def test_original_question_returns_true(self):
        """
        test to check if check_question_is_original returns
        truthy if question has NOT already been asked
        """
        questions_list = run.get_questions_answers_keywords("Easy") 
        question1 = questions_list[0]
        question2 = questions_list[1]
        used_questions = []
        used_questions = run.check_question_is_original(question1, used_questions)
        
        self.assertTrue(run.check_question_is_original(question2, used_questions))

        
        
      
    def test_question_is_not_repeated(self):
        """
        test to check that an initial question is 
        not asked again 
        """
        used_questions = []
        initial_question= run.random_question_tuple("Normal", used_questions)
        subsequent_questions = []
        for i in range (10):
            another_question = run.random_question_tuple("Normal", used_questions)
            subsequent_questions.append(another_question)
            
        
        self.assertTrue(len(subsequent_questions)==10)
        self.assertNotIn(initial_question, subsequent_questions)
        
        
    
        
        
    
   

        
        
class testGameMechanics(unittest.TestCase):
    
    
    
    def test_user_gameplay_lists_correct_variable_types(self):
        """
        test to check that each list created by 
        create_multiple_users_gameplay_lists is [string,int,int]
        """
        
        username_list= ["John", "Paul", "Ringo", "George"]
        gameplay_list = run.create_multiple_users_gameplay_lists(username_list, 3 , 0)
        for player in gameplay_list:
            username = player[0]
            lives = player[1]
            score = player[2]
            self.assertTrue(isinstance(username, str))
            self.assertTrue(isinstance(lives, int))
            self.assertTrue(isinstance(score, int))
            
        
    
    

        
        
    def check_answer_framework(self, given_answer, expected_out):
        
        
        """
        framework to test if user input leads 
        to the desired response in the console
        used in tests below 
        code partly from https://stackoverflow.com/questions/21046717/python-mocking-raw-input-in-unittests
        keyword for question is 'age'
        """
        
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            questions_list = run.get_questions_answers_keywords("Easy") 
            question = questions_list[0]
            run.answer_question(question)
            self.assertEqual(fake_out.getvalue().strip(), expected_out)
            
            

    def test_correct_answer_returns_correct(self):
        self.check_answer_framework('age', 'Correct!')
        
    def test_incorrect_answer_returns_wrong(self):
        self.check_answer_framework('time', "Wrong!")
        
    def test_answer_case_insensitive(self):
        self.check_answer_framework('AGe', "Correct!")

        
    def test_no_lives_returns_false(self):
        """
        test to check that game_rounds()
        returns false if user has no lives
        """
        used_questions = []
        initial_question = run.random_question_tuple("Easy", used_questions)
        self.assertFalse(run.game_rounds(initial_question, 0, 0, used_questions))
        

        
    def test_add_point_increases_score(self):
        """
        test to check if score is increased
        """
        score = run.add_point(2)
        self.assertEqual(score, 3)
        score = run.add_point(3)
        self.assertEqual(score,4)
    
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
        
        
        
        
        
    def test_game_rounds_returns_score(self):
        """
        tests if game rounds returns the user's
        score
        """
        used_questions = []
        score = 5
        lives = 0
        initial_question= run.random_question_tuple("Normal", used_questions)
        
        returned_value = run.game_rounds(initial_question, lives, score, used_questions)
        self.assertEqual(returned_value, score)
        
        score = 3 
        returned_value = run.game_rounds(initial_question, lives, score, used_questions)
        self.assertEqual(returned_value, score)
        
        
        
class testLeaderboards(unittest.TestCase):
    
    def test_log_score_appends_doc(self):
        """
        test to check that the number of lines in
        all_scores.txt increases by 1 when a score is logged
        """
      
        lines_before_log = 0  
        all_scores = open("data/all_scores.txt", "r") 
        for line in all_scores:
            lines_before_log += 1
                
        lines_after_log = 0
        run.log_score("test", 5)
        
        all_scores.seek(0)
        for line in all_scores:
            lines_after_log +=1
            
        all_scores.close()
            
        self.assertEqual(lines_before_log, lines_after_log-1)
        
    def test_creates_scores_tuple_list(self):
        """
        test to check that create_scores_tuple_list
        returns a list of tuples
        """
        returned = run.create_scores_tuple_list()
        self.assertTrue(isinstance(returned, list))
        
        first_entry = returned[0]
        self.assertTrue(isinstance(first_entry, tuple))
        
    
    def test_second_entry_is_int(self):
        """
        test to check that the second entry of a 
        tuple created by create_scores_tuple_list 
        is an integer
        """
        
        tuple_list = run.create_scores_tuple_list()
        first_tuple = tuple_list[0]
        second_entry = first_tuple[1]
        
        self.assertTrue(isinstance(second_entry ,int))
        
    
    def test_scores_sorted_by_score(self):
        """
        test to check that sort_scores returns
        a list of tuple where no tuple score
        is larger than the previous entry
        """
        scores_tuple_list = run.create_scores_tuple_list()
        sorted_list = run.sort_scores(scores_tuple_list)
        for i in range (len(sorted_list)-1):
            self.assertTrue(sorted_list[i][1] >= sorted_list[i+1][1])
        
        
        
        
  