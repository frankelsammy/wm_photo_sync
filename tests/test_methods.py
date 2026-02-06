import unittest
import os
from src.gmail import send_email, delete_email

class TestSendEmail(unittest.TestCase):
    def setUp(self):
        self.original_dir = os.getcwd()
        
        target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
        
        # Change the working directory to 'src'
        os.chdir(target_dir)

    def tearDown(self):
        # Always change back to the original directory after the test
        os.chdir(self.original_dir)
    def test_send_email(self):
        try:
            id = send_email("This is a test email from the WM Photo Sync application.")
            self.assertIsNotNone(id)  # If no exception is raised and id is returned, the test passes
            self.assertTrue(delete_email(id))
            
        except Exception as e:
            self.fail(f"send_email raised an exception: {e}")