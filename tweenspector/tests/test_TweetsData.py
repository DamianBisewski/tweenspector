from pathlib import Path
import sys

# Make sure Python sees files outside of test directory
sys.path.append(str(Path().absolute().parent))

import unittest
from tweenspector.TweetsData import TweetsData


class TestTweetsData(unittest.TestCase):
    def test_can_create_TweetsData(self):
        username = "TestUser"
        search_words = ""
        date_from = "04-10-2022"
        date_to = "03-11-2022"
        td = TweetsData(username, search_words, date_from, date_to)
        self.assertIsNotNone(td)
