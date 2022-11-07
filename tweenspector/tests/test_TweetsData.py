from TestUtils import add_parent_dir_to_sys_path

add_parent_dir_to_sys_path()  # Make sure Python sees files outside of test directory

import unittest
from unittest.mock import MagicMock, patch
import tweenspector.TweetsData as TwDt
from tweenspector.TweetsData import TweetsData
import pandas as pd
import itertools
from wordcloud import WordCloud
import igraph


class TestTweetsData(unittest.TestCase):
    tweets_dict = {}

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
            self.getSampleTweets(),
            pd.DataFrame()
        ]

        for data in test_data:
            with self.subTest(data=data):
                mock_twint.output.panda.Tweets_df = data
                td = self.generateTweetsData()
                tweets = td.get_tweets(td.user_name, td.search_words, td.Since, td.Until, td.num_of_tweets)
                self.assertIsNotNone(tweets)
                self.assertEqual(len(data), len(tweets))

    @patch("tweenspector.TweetsData.twint")
    def test_get_tweets_returns_empty_dataframe_on_exception(self, mock_twint):
        test_exceptions = [ValueError, TypeError, AttributeError, Exception]
        for exc in test_exceptions:
            with self.subTest(exc=exc):
                mock_twint.run.Profile = MagicMock(side_effect=exc)
                td = self.generateTweetsData()
                ret = td.get_tweets(td.user_name, td.search_words, td.Since, td.Until, td.num_of_tweets)
                self.assertIsNotNone(ret)
                self.assertEqual(len(ret), 0)
                mock_twint.run.Profile.assert_called_once()

    def test_can_generate_word_cloud(self):
        test_data = [True, False]
        for expected_res in test_data:
            with self.subTest(expected_res=expected_res):
                mock_td = MagicMock()
                mock_td.create_word_cloud = MagicMock(return_value=MagicMock() if expected_res else None)
                ret = TweetsData.generate_word_cloud(mock_td)
                self.assertEqual(ret, expected_res)
                mock_td.create_word_cloud.assert_called_once()

    @patch("tweenspector.TweetsData.spacy")
    @patch("tweenspector.TweetsData.WordCloud")
    def test_can_create_word_cloud(self, mock_WordCloud, mock_spacy):
        test_data = [
            (self.getSampleTweets(), True),
            (pd.DataFrame(), False)
        ]
        for (data, expected_res) in test_data:
            with self.subTest(data=data, expected_res=expected_res):
                mock_td = MagicMock()
                mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
                mock_td.get_tweets = MagicMock(return_value=data)
                mock_td.self.num_of_tweets_read = data.shape[0]
                mock_nlp = MagicMock(side_effect=lambda x: (MagicMock(lemma_=v) for v in x.split(" ")))
                mock_spacy.load = MagicMock(return_value=mock_nlp)
                ret = TweetsData.create_word_cloud(mock_td)
                self.assertEqual(ret is not None, expected_res)
                mock_WordCloud.assert_called_once()

    @patch("tweenspector.TweetsData.spacy")
    @patch("tweenspector.TweetsData.WordCloud")
    def test_create_word_cloud_returns_none_on_spacy_exception(self, mock_WordCloud, mock_spacy):
        tweets = self.getSampleTweets()
        test_exceptions = [ValueError, TypeError, AttributeError, Exception]
        for exc in test_exceptions:
            with self.subTest(exc=exc):
                mock_td = MagicMock()
                mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
                mock_td.get_tweets = MagicMock(return_value=tweets)
                mock_td.self.num_of_tweets_read = tweets.shape[0]
                mock_spacy.load = MagicMock(side_effect=exc)
                ret = TweetsData.create_word_cloud(mock_td)
                self.assertIsNone(ret)

    @patch("tweenspector.TweetsData.spacy")
    @patch("tweenspector.TweetsData.WordCloud")
    def test_create_word_cloud_returns_none_on_WordCloud_exception(self, mock_WordCloud, mock_spacy):
        tweets = self.getSampleTweets()
        test_exceptions = [ValueError, TypeError, AttributeError, Exception]
        for exc in test_exceptions:
            with self.subTest(exc=exc):
                mock_td = MagicMock()
                mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
                mock_td.get_tweets = MagicMock(return_value=tweets)
                mock_td.self.num_of_tweets_read = tweets.shape[0]
                mock_WordCloud.side_effect = exc
                ret = TweetsData.create_word_cloud(mock_td)
                self.assertIsNone(ret)

    @patch("tweenspector.TweetsData.spacy")
    @patch("tweenspector.TweetsData.WordCloud")
    def test_create_word_cloud_returns_correct_content(self, mock_WordCloud, mock_spacy):
        tweets = self.getSampleTweets()

        mock_td = MagicMock()
        mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
        mock_td.get_tweets = MagicMock(return_value=tweets)
        mock_td.self.num_of_tweets_read = tweets.shape[0]

        mock_nlp = MagicMock(side_effect=lambda x: (MagicMock(lemma_=v) for v in x.split(" ")))
        mock_spacy.load = MagicMock(return_value=mock_nlp)

        wordcloud, text = TweetsData.create_word_cloud(mock_td)
        wc_args = mock_WordCloud.call_args.kwargs
        real_wc = WordCloud(
            background_color=wc_args.get("background_color"),
            colormap=wc_args.get("colormap"),
            width=wc_args.get("width"),
            height=wc_args.get("height"),
            stopwords=wc_args.get("stopwords"))
        ret = real_wc.process_text(str(text))
        sample = {'Ala': 1, 'Alę': 1, 'Doprowadzili': 1, 'Europejską': 1, 'III': 1,
                  'Polsce': 1, 'Polską': 1, 'Sebastianowi': 1, 'Unia': 1, 'Zrobili': 1,
                  'a': 2, 'byle': 1, 'całej': 1, 'cały': 1, 'czas': 1, 'do': 2,
                  'głupota': 1, 'i': 1, 'innych': 1, 'jej': 1, 'jest': 1, 'katastrofy': 1,
                  'konfliktem': 1, 'kot': 1, 'kota': 1, 'którym': 1, 'kłamali': 1,
                  'kłamstw': 1, 'ma': 2, 'między': 1, 'na': 1, 'nie': 1, 'nieszczęść': 1,
                  'niszcząc': 1, 'odpowiedzialności': 1, 'ofiarę': 1, 'on': 1, 'po': 1,
                  'polityce': 1, 'polskiego': 1, 'poważnych': 1, 'premiera': 1,
                  'przyczyną': 1, 'seicento': 1, 'tak': 1, 'tylko': 1, 'uniknąć': 1,
                  'w': 2, 'winę': 1, 'większości': 1, 'wojnę': 1, 'wywiadzie': 1,
                  'wywołaną': 1, 'z': 1, 'zapowiada': 1, 'zdębiał': 1, 'zmuszali': 1,
                  'zrzucili': 1, 'Świat': 1, 'światową': 1, 'życie': 1}
        self.assertEqual(sample, ret)

    def test_can_generate_interconnections_network(self):
        test_rets = [True, False]
        test_options = ["Optimal Modularity", "Spinglass", "Label Propagation", "Infomap"]
        test_data = itertools.product(test_options, test_rets)

        for (option, expected_res) in test_data:
            with self.subTest(option=option, expected_res=expected_res):
                mock_td = MagicMock()
                mock_td.create_interconnections_network = MagicMock(return_value=MagicMock() if expected_res else None)
                ret = TweetsData.generate_interconnections_network(mock_td, option)
                self.assertEqual(ret, expected_res)
                mock_td.create_interconnections_network.assert_called_once()

    @patch("tweenspector.TweetsData.igraph")
    def test_can_create_interconnections_network(self, mock_igraph):
        tweet_df = self.getSampleTweets()
        test_data = [
            (tweet_df, "Optimal Modularity", True),
            (tweet_df, "Spinglass", True),
            (tweet_df, "Label Propagation", True),
            (tweet_df, "Infomap", True),
            (tweet_df, "invalid", False),
            (tweet_df, None, False),
            (pd.DataFrame(), "Optimal Modularity", False)
        ]

        for (tweets, option, expected_ret) in test_data:
            with self.subTest(option=option, expected_ret=expected_ret):
                mock_td = MagicMock()
                mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
                mock_td.get_tweets = MagicMock(return_value=tweets)
                mock_td.self.num_of_tweets_read = tweets.shape[0]
                ret = TweetsData.create_interconnections_network(mock_td, option)
                self.assertEqual(ret is not None, expected_ret)

    @patch("tweenspector.TweetsData.igraph")
    def test_create_interconnections_network_returns_none_on_exception(self, mock_igraph):
        tweets = self.getSampleTweets()
        test_exceptions = [ValueError, TypeError, AttributeError, Exception]
        test_options = ["Optimal Modularity", "Spinglass", "Label Propagation", "Infomap"]
        test_data = itertools.product(test_options, test_exceptions)

        for (option, exc) in test_data:
            with self.subTest(option=option, exc=exc):
                mock_td = MagicMock()
                mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
                mock_td.get_tweets = MagicMock(return_value=tweets)
                mock_td.self.num_of_tweets_read = tweets.shape[0]
                mock_igraph.Graph = MagicMock(side_effect=exc)
                ret = TweetsData.create_interconnections_network(mock_td, option)
                self.assertIsNone(ret)

    @patch("tweenspector.TweetsData.igraph")
    def test_create_interconnection_network_returns_correct_content(self, mock_igraph):
        print("--- test_create_interconnection_network_returns_correct_content() ---")

        option = "Label Propagation"

        mock_td = MagicMock()
        mock_td.user_name = "szczepimysie"
        mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
        mock_td.get_tweets = MagicMock(side_effect=lambda user_name, *_: self.getTweetsFromCsv(user_name))

        mock_igraph.Graph = MagicMock(side_effect=lambda directed: igraph.Graph(directed=directed))

        ig = TweetsData.create_interconnections_network(mock_td, option)
        sample = igraph.Graph(directed=True)
        sample.add_vertex("szczepimysie")
        sample.add_vertex("bealooa")
        sample.add_vertex("mz_gov_pl")
        sample.add_edge("szczepimysie", "bealooa")
        sample.add_edge("szczepimysie", "mz_gov_pl")
        self.assertTrue(sample.isomorphic_vf2(ig))

        print("--- test_create_interconnection_network_returns_correct_content() DONE ---")

    def test_can_generate_user_stats(self):
        test_rets = [True, False]
        test_options = [0, 1, 2, 3]
        test_data = itertools.product(test_options, test_rets)

        for (option, expected_res) in test_data:
            with self.subTest(option=option, expected_res=expected_res):
                mock_td = MagicMock()
                mock_td.create_user_stats = MagicMock(return_value=MagicMock() if expected_res else None)
                ret = TweetsData.generate_user_stats(mock_td, option)
                self.assertEqual(ret, expected_res)
                mock_td.create_user_stats.assert_called_once()

    @patch("tweenspector.TweetsData.pd")
    @patch("tweenspector.TweetsData.plt")
    @patch("tweenspector.TweetsData.matplotlib")
    def test_can_create_user_stats(self, mock_matplotlib, mock_plt, mock_pd):
        tweets_df = self.getSampleTweets()
        options = [
            (tweets_df, -1, False),
            (tweets_df, 0, True),
            (tweets_df, 1, True),
            (tweets_df, 2, True),
            (tweets_df, 3, True),
            (tweets_df, 4, False),
            (pd.DataFrame(), 1, False)
        ]

        for (tweets, option, expected_ret) in options:
            with self.subTest(option=option, expected_ret=expected_ret):
                mock_td = MagicMock()
                mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
                mock_td.get_tweets = MagicMock(return_value=tweets)
                mock_td.self.num_of_tweets_read = tweets.shape[0]
                ret = TweetsData.create_user_stats(mock_td, option)
                self.assertEqual(ret is not None, expected_ret)

    @patch("tweenspector.TweetsData.pd")
    @patch("tweenspector.TweetsData.plt")
    @patch("tweenspector.TweetsData.matplotlib")
    def test_create_user_stats_returns_correct_content(self, mock_matplotlib, mock_plt, mock_pd):
        tweets = self.getTweetsFromCsv("donaldtusk")
        option = 1

        mock_td = MagicMock()
        mock_td.test_mode_enabled = MagicMock(return_value=False)  # TODO remove
        mock_td.get_tweets = MagicMock(return_value=tweets)
        mock_td.num_of_tweets_read = tweets.shape[0]

        mock_pd.to_datetime = MagicMock(side_effect=pd.to_datetime)

        user_stats = TweetsData.create_user_stats(mock_td, option)

        sample = {'avglikes': 8886, 'maxlikes': 13480, 'minlikes': 2484, 'medianlikes': 10013.0,
                  'avgretweets': 1433, 'maxretweets': 2290, 'minretweets': 516, 'medianretweets': 1536.0,
                  'interval': pd.Timedelta('2 days 08:00:00'), 'places': set(), 'hashtagdict': {'lextvn': 1},
                  'usersdict': {'gazeta_wyborcza': 1},
                  'hourdict': {'12': 1, '18': 1, '09': 1, '15': 1, '17': 1, '10': 2, '19': 3}}
        self.assertEqual(user_stats, sample)

    # helpers

    def generateTweetsData(self):
        username = "TestUser"
        search_words = ""
        date_from = "04-10-2022"
        date_to = "03-11-2022"
        return TweetsData(username, search_words, date_from, date_to)

    def getSampleTweets(self):
        return self.getTweetsFromCsv("wordcloud_test")

    def getTweetsFromCsv(self, filename):
        if filename in self.tweets_dict:
            return self.tweets_dict.get(filename)
        try:
            fn = "{f}1.csv".format(f=filename)
            tweets = pd.read_csv(fn,
                                 converters={
                                     "place": lambda p: str(p),
                                     "hour": lambda h: str(h),
                                     "hashtags": lambda h: [x.strip(" '\"") for x in str(h).strip("[]").split(",")]
                                 })
            self.tweets_dict[filename] = tweets
            return tweets
        except Exception as exc:
            print("Failed to load {fn} - {excType}: {excMsg}".format(fn=fn,
                                                                         excType=type(exc).__name__,
                                                                         excMsg=str(exc)))
            raise exc
