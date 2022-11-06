from TestUtils import add_parent_dir_to_sys_path

add_parent_dir_to_sys_path()  # Make sure Python sees files outside of test directory

import unittest
from unittest.mock import MagicMock, patch
import tweenspector.TweetsData as TwDt
from tweenspector.TweetsData import TweetsData
import pandas as pd


class TestTweetsData(unittest.TestCase):
    def test_can_create_TweetsData(self):
        username = "TestUser"
        search_words = ""
        date_from = "04-10-2022"
        date_to = "03-11-2022"
        td = TweetsData(username, search_words, date_from, date_to)
        self.assertIsNotNone(td)

    @patch("tweenspector.TweetsData.pd.read_csv")
    def test_can_load_tweets_df_form_csv(self, mock_read_csv):
        filename = "TestFilename"
        mock_ret = MagicMock()
        mock_read_csv.return_value = mock_ret
        ret = TwDt.load_tweets_df_from_csv(filename)
        self.assertIsNotNone(ret)
        mock_read_csv.assert_called_once_with(filename)

    def test_can_save_tweets_df_to_csv(self):
        filename = "TestFilename"
        mock_to_csv = MagicMock(return_value=None)
        mock_tweets_df = MagicMock()
        mock_tweets_df.to_csv = mock_to_csv
        TwDt.save_tweets_df_to_csv(filename, mock_tweets_df)
        mock_to_csv.assert_called_once_with(filename)

    @patch("tweenspector.TweetsData.twint")
    def test_can_get_tweets(self, mock_twint):
        test_data = [
            [],
            ["tweet"],
            ["tweet1", "tweet2"],
            ["", "tweet", "msg"],
            ["", "", "", ""]
        ]
        for data in test_data:
            with self.subTest(data=data):
                df = pd.DataFrame(data)
                mock_twint.output.panda.Tweets_df = df
                td = generateTweetsData()
                tweets = td.get_tweets(td.user_name, td.search_words, td.Since, td.Until, td.num_of_tweets)
                self.assertIsNotNone(tweets)
                self.assertEqual(len(df), len(tweets))

    @patch("tweenspector.TweetsData.twint")
    def test_returns_empty_dataframe_when_twint_raises_exception(self, mock_twint):
        test_exceptions = [ValueError, TypeError, AttributeError, Exception]
        for exc in test_exceptions:
            with self.subTest(exc=exc):
                mock_twint.run.Profile = MagicMock(side_effect=exc)
                td = generateTweetsData()
                ret = td.get_tweets(td.user_name, td.search_words, td.Since, td.Until, td.num_of_tweets)
                self.assertIsNotNone(ret)
                self.assertEqual(len(ret), 0)
                mock_twint.run.Profile.assert_called_once()


# helpers

def generateTweetsData() -> TweetsData:
    username = "TestUser"
    search_words = ""
    date_from = "04-10-2022"
    date_to = "03-11-2022"
    return TweetsData(username, search_words, date_from, date_to)
