import unittest
import run




class test(unittest.TestCase):
    
    def test_can_change_usernames(self):
        
        """
        test to see if we can change our username
        """
        username = run.set_username()
        self.assertNotEqual(username, "default")