from pathlib import Path
import sys

# Make sure Python sees files outside of test directory
sys.path.append(str(Path().absolute().parent))

import unittest
from tweenspector import App_variables

class TestAppVariables(unittest.TestCase):
    def test_tweets_count_list_not_empty(self):
        self.assertGreater(len(App_variables.tweets_count_list), 0)
    def test_features_not_empty(self):
        self.assertGreater(len(App_variables.features), 0)
    def test_timezone_to_string(self):
        tm = App_variables.timezone_to_string()
        self.assertIsInstance(tm, str)
        self.assertGreater(len(tm), 0)