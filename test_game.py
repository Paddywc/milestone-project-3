import unittest
import run




class testUsernameInput(unittest.TestCase):
    
    def test_can_change_usernames(self):
        
        """
        test to see if we can change our username
        """
        test_username = run.set_username()
        self.assertNotEqual(test_username, "default")
        
    def test_username_not_empty(self):
        """
        test to ensure empty inputs are rejected as usernames
        """
        test_username = run.set_username()
        username_length = len(test_username)
        self.assertTrue(username_length != 0)
        