import unittest
import run
from unittest.mock import patch
from io import StringIO




class testUsernameInput(unittest.TestCase):
    
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
        
   
    

    
class testQuestionsAnswersKeyWords(unittest.TestCase):
    
    
    def test_if_list_returned(self):
        """
        test to see if function returns
        a list
        """
        
        returned_list = run.get_questions_answers_keywords()
        self.assertTrue(type(returned_list) is list)
        
    def test_if_list_of_tuples(self):
        """
        test to check if returned list contains
        only tuples
        """
        returned_list = run.get_questions_answers_keywords()
        for entry in returned_list:
            self.assertTrue(type(entry) is tuple)

        
    
    def test_no_newline_text(self):
        """
        tests if '\n' appears in the question
        fails if it does
        """
        
        test_questions = run.get_questions_answers_keywords()
        self.assertNotIn("\n", test_questions[0])
        self.assertNotIn("\n", test_questions[3])
        self.assertNotIn("\n", test_questions[4])
        
        
    
    def test_question_is_a_question(self):
        """
        tests to ensure that the questions list only
        contains lines ending in a question mark
        """
        
        test_questions_answers_keywords = run.get_questions_answers_keywords();
        for entry in test_questions_answers_keywords:
            question = entry[0]
            index_of_last_char = len(question)-1
            self.assertEqual(question[index_of_last_char], "?")
            
            
    def test_if_keyword_only_one_word(self):
        """
        test to confirm that keyword entries 
        don't contain spaces
        """
        
        test_questions_answers_keywords = run.get_questions_answers_keywords();
        for entry in test_questions_answers_keywords:
            keyword = entry[2]
            self.assertNotIn(" ", keyword)
            
    def test_lowercase_answer_contains_keyword(self):
        """
        to to check that all keywords are 
        included in the answer
        """
        
        test_questions_answers_keywords = run.get_questions_answers_keywords();
        for entry in test_questions_answers_keywords:
            answer = entry[1].lower()
            keyword = entry[2]
            self.assertIn(keyword , answer)
        

        
        
class testGameMechanics(unittest.TestCase):
    
    def test_questions_randomly_selected(self):
        
        """
        checks if two complete lists of randomly generated
        tuples are not equal 
        """
     
        questions_list = run.get_questions_answers_keywords()
        
        first_list = []
        second_list = []
        
        for i in range(len(questions_list)):
            first_list.append(run.random_question_tuple())
        
        for i in range(len(questions_list)):
            second_list.append(run.random_question_tuple())
            
        self.assertNotEqual(first_list, second_list)
        
        
    
   
        
        
    def check_answer_framework(self, given_answer, expected_out):
        
        
        """
        framework to test if user input leads 
        to the desired response in the console
        used in tests below 
        code partly from https://stackoverflow.com/questions/21046717/python-mocking-raw-input-in-unittests
        keyword for question is 'age'
        """
        
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            questions_list = run.get_questions_answers_keywords() 
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
        self.assertFalse(run.game_rounds([], 0))
        

        
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
        <2 Easy, <7 Normal, >6 Hard
        """
        self.assertEqual(run.set_difficulty(0),"Easy")
        self.assertEqual(run.set_difficulty(1),"Easy")
        self.assertEqual(run.set_difficulty(2),"Normal")
        self.assertEqual(run.set_difficulty(3),"Normal")
        self.assertEqual(run.set_difficulty(4),"Normal")
        self.assertEqual(run.set_difficulty(5),"Normal")
        self.assertEqual(run.set_difficulty(6),"Normal")
        self.assertEqual(run.set_difficulty(7),"Hard")
        self.assertEqual(run.set_difficulty(8),"Hard")
        
        
        
