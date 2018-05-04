import unittest
import run


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
        
        incorrect_text = round_text[0]
        host_text = round_text[3]
        question_text = round_text[4]
        game_over_text= round_text[6]
        
        self.assertTrue(len(incorrect_text)>0)
        self.assertTrue(len(host_text)>0)
        self.assertTrue(len(question_text)>0)
        self.assertTrue(len(game_over_text)>0)
        
        run.wipe_game_text()

        round_text = run.get_round_text()
        
        incorrect_text = round_text[0]
        host_text = round_text[3]
        question_text = round_text[4]
        game_over_text= round_text[6]
        
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
        answer_text = "".join(round_text[2])
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
        
        