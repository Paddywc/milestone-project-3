import unittest
import run




# class testUsernameInput(unittest.TestCase):
    
#     def test_can_change_usernames(self):
        
#         """
#         test to see if we can change our username
#         """
#         test_username = run.set_username()
#         self.assertNotEqual(test_username, "default")
        
#     def test_username_not_empty(self):
#         """
#         test to ensure empty inputs are rejected as usernames
#         """
#         test_username = run.set_username()
#         username_length = len(test_username)
#         self.assertTrue(username_length != 0)
        
    
class testQuiz(unittest.TestCase):
    
    def test_no_newline_text(self):
        """
        tests if '\n' appears in the question
        fails if it does
        """
        
        test_questions = run.get_questions()
        self.assertNotIn("\n", test_questions[0])
        self.assertNotIn("\n", test_questions[3])
        self.assertNotIn("\n", test_questions[4])
        
        
    
    def test_question_is_a_question(self):
        """
        tests to ensure that the questions list only
        contains lines ending in a question mark
        """
        
        test_questions = run.get_questions();
        for question in test_questions:
            index_of_last_char = len(question)-1
            self.assertEqual(question[index_of_last_char], "?")
        
        
