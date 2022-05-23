import twint
from wordcloud import WordCloud, STOPWORDS
import re
import igraph
import pandas as pd
import statistics
import pl_core_news_lg
import matplotlib.pyplot as plt
import matplotlib
import math
from App_variables import *


def save_tweets_df_to_csv(filename, tweets_df):
    tweets_df.to_csv(filename)


def load_tweets_df_form_csv(filename):
    return pd.read_csv(filename)


class TweetsData:
    def __init__(self, user_name, search_words, date_from, date_to, num_of_tweets=500):
        self.user_name = user_name
        self.num_of_tweets = num_of_tweets
        self.num_of_tweets_read = 0
        self.Since = date_from
        self.Until = date_to
        self.search_words = search_words
        self.test_mode = False
        self.wordcloud = None  # test mode only
        self.account_stats = None  # test mode only
        self.interconnection_graph = None  # test mode only

    def test_mode_enable(self):
        self.test_mode = True

    def test_mode_disable(self):
        self.test_mode = False

    def test_mode_enabled(self):
        return self.test_mode

    def get_tweets(self, user_name, search_words, date_from, date_to, num_of_tweets):
        if self.test_mode_enabled():
            print('TEST MODE: loading tweets from disc')
            df = load_tweets_df_form_csv(user_name + '.csv')
            self.num_of_tweets_read = df.shape[0]
            return df
        try:
            c = twint.Config()
            c.Username = user_name
            c.Limit = num_of_tweets
            c.Pandas = True
            c.Retweets = True
            c.Pandas_clean = True
            c.Stats = True
            c.Count = True
            c.Since = date_from
            c.Until = date_to
            c.Search = search_words
            c.Hide_output = True
            twint.run.Profile(c)
            if twint.output.panda.Tweets_df.empty:
                print("No tweets from user: ", user_name)
                return twint.output.panda.Tweets_df
            else:
                return twint.output.panda.Tweets_df
        except ValueError:
            print("Get tweets - Blad wartosci, user:", user_name)
            return pd.DataFrame()
        except:
            print("Get tweets - Cos poszlo nie tak, user:", user_name)
            return pd.DataFrame()

    def generate_word_cloud(self):
        tweets = self.get_tweets(self.user_name, self.search_words, self.Since, self.Until, self.num_of_tweets)
        if tweets.empty:
            return False
        try:
            stopwords = set(STOPWORDS)
            lemmatizer_enabled = True
            file = open("stopwords.txt", "r", encoding="utf8")
            word = file.readline().replace('\n', '')
            while word:
                stopwords.add(word)
                word = file.readline().replace('\n', '')
            preprocessed_tweets_text = ''
            original_tweets_text = ''
            for tweet in tweets.iterrows():
                text = tweet[1]['tweet']
                mts = set(re.findall(r"@(\w+)", text))
                for mt in mts:
                    stopwords.add(mt)
                rts = set(re.findall(r"(RT @\w+)", text))
                for rt in rts:
                    stopwords.add(rt)
            if lemmatizer_enabled:
                original_tweets_text = tweets.tweet.values
                nlp = pl_core_news_lg.load()
                tweets_text_from_lemmatizer = nlp(str(original_tweets_text))
                preprocessed_tweets_text = ''
                for t in tweets_text_from_lemmatizer:
                    if t.lemma_ not in stopwords:
                        preprocessed_tweets_text = preprocessed_tweets_text + ' ' + t.lemma_
            else:
                preprocessed_tweets_text = tweets.tweet.values
            if self.test_mode_enabled():
                wordcloud = WordCloud(
                    background_color='black',
                    colormap='Pastel1',
                    width=1000,
                    height=500,
                    stopwords=stopwords)
                self.wordcloud = wordcloud.process_text(str(preprocessed_tweets_text))
            else:
                wordcloud = WordCloud(
                    background_color='black',
                    colormap='Pastel1',
                    width=1000,
                    height=500,
                    stopwords=stopwords).generate(str(preprocessed_tweets_text))
                wordcloud.to_file("images/file.png")
                return True
        except ValueError:
            print("Generate word cloud - Blad wartosci")
            return False
        except:
            print("Generate word cloud - Cos poszlo nie tak")
            return False

    def generate_interconnections_network(self, option):
        tweets = self.get_tweets(self.user_name, self.search_words, self.Since, self.Until, self.num_of_tweets)
        if tweets.empty:
            return False
        try:
            def get_friends():
                rtsmts = set()
                rtsmts.add(self.user_name.lower())
                for r in tweets.iterrows():
                    text = r[1]['tweet']
                    mts = set(re.findall(r"@(\w+)", text))
                    for mt in mts:
                        mt = mt.lower()
                        rtsmts.add(mt)
                return rtsmts

            g = igraph.Graph(directed=True)
            rtsmts = get_friends()
            for rtmt in rtsmts:
                g.add_vertex(rtmt)
            relations = dict()
            for someone in rtsmts:
                relations[someone] = dict()
                friend_tweets = self.get_tweets(someone, self.search_words, self.Since, self.Until, self.num_of_tweets)
                if friend_tweets.empty:
                    print("Generate interconnections network - Brak konta, user:", someone)
                    continue
                for r in friend_tweets.iterrows():
                    text = r[1]['tweet']
                    mts = set(re.findall(r"@(\w+)", text))
                    for mt in mts:
                        mt = mt.lower()
                        if mt in rtsmts:
                            if mt != someone:
                                if mt in relations[someone]:
                                    relations[someone][mt] = relations[someone][mt] + 1
                                else:
                                    relations[someone][mt] = 1

            for someone in rtsmts:
                temp = relations[someone]
                for key, value in temp.items():
                    g.add_edge(someone, key)
            x = 1000 * math.log(len(rtsmts))
            y = 600 * math.log(len(rtsmts))
            visual_style = {
                "vertex_size": 40,
                "vertex_label_size": 50,
                "vertex_label_dist": 2,
                "margin": 250,
                "bbox": (x, y),
                "vertex_label": rtsmts,
                "edge_width":
                    [math.log(2 * relations[g.vs[edge.source]["name"]][g.vs[edge.target]["name"]], 1.5)
                     for edge in g.es]
            }

            if option == "Optimal Modularity":
                comm = g.community_optimal_modularity()
            elif option == "Spinglass":
                comm = g.community_spinglass()
            elif option == "Label Propagation":
                comm = g.community_label_propagation()
            elif option == "Infomap":
                comm = g.community_infomap()
            else:
                return False
            igraph.plot(comm, "images/file.png", **visual_style, mark_groups=True)
            if self.test_mode_enabled():
                self.interconnection_graph = g
            return True
        except ValueError:
            print("Generate interconnections network - Blad wartosci")
            return False
        except:
            print("Generate interconnections network - Cos poszlo nie tak")
            return False

    def generate_user_stats(self, option):
        def generate_account_info(df):
            date1 = pd.to_datetime(df.iloc[0].date)
            date2 = pd.to_datetime(df.iloc[int(self.num_of_tweets_read) - 1].date)
            usersdict = dict()
            for tweet in df.tweet:
                mts = set(re.findall(r"@(\w+)", tweet))
                for mt in mts:
                    mt = mt.lower()
                    if mt in usersdict:
                        usersdict[mt] = usersdict[mt] + 1
                    else:
                        usersdict[mt] = 1
            hourdict = dict()
            for hour in df.hour:
                if hour in hourdict:
                    hourdict[hour] = hourdict[hour] + 1
                else:
                    hourdict[hour] = 1
            account_stats = {
                'avglikes': round(sum(df[df.retweet == False].nlikes) / len(df[df.retweet == False].nlikes)),
                'maxlikes': max(df[df.retweet == False].nlikes),
                'minlikes': min(df[df.retweet == False].nlikes),
                'medianlikes': statistics.median(df[df.retweet == False].nlikes),
                'avgretweets': round(sum(df[df.retweet == False].nretweets) /
                                     len(df[df.retweet == False].nretweets)),
                'maxretweets': max(df[df.retweet == False].nretweets),
                'minretweets': min(df[df.retweet == False].nretweets),
                'medianretweets': statistics.median(df[df.retweet == False].nretweets),
                'interval': (date1 - date2) / (int(self.num_of_tweets_read) - 1),
                'places': set(),
                'hashtagdict': dict(),
                'usersdict': dict(sorted(usersdict.items(), key=lambda x: x[1])),
                'hourdict': dict(sorted(hourdict.items(), key=lambda x: x[1]))}
            if not self.test_mode_enabled():
                # due to the bug in twint loading place field from csv this feature is disabled in test mode
                for place in df.place:
                    if place != '':
                        account_stats['places'].add(place)
            if self.test_mode_enabled():
                # due to the bug in the twint hashtags loaded from csv are provided as string
                for hashtags in df.hashtags:
                    stripped_hashtags = hashtags.strip('\'[]  ')
                    hashtags_list = stripped_hashtags.split(',')
                    for hashtag in hashtags_list:
                        if hashtag:
                            if hashtag in account_stats['hashtagdict']:
                                account_stats['hashtagdict'][hashtag] = account_stats['hashtagdict'][hashtag] + 1
                            else:
                                account_stats['hashtagdict'][hashtag] = 1
            else:
                # for hashtags loaded from tweeter twint provides them as list of strings
                for hashtags in df.hashtags:
                    for hashtag in hashtags:
                        if hashtag:
                            if hashtag in account_stats['hashtagdict']:
                                account_stats['hashtagdict'][hashtag] = account_stats['hashtagdict'][hashtag] + 1
                            else:
                                account_stats['hashtagdict'][hashtag] = 1
            return account_stats

        data_frame = self.get_tweets(self.user_name, self.search_words, self.Since, self.Until, self.num_of_tweets)
        if data_frame.empty:
            return False
        account_stats = generate_account_info(data_frame)
        if self.test_mode_enabled():
            self.account_stats = account_stats

        def generate_statistics_chart():
            plt.figure(figsize=(12, 5))

            values_name = {'maxlikes': "Największa liczba like'ów",
                           'avglikes': "Średnia ilość like'ów",
                           'medianlikes': "Mediana liczby like'ów",
                           'maxretweets': "Największa liczba retweet'ów",
                           'avgretweets': "Średnia liczba retweet'ów",
                           'medianretweets': "Mediana liczby retweetów",
                           }
            values_count = []
            for name in list(values_name.keys()):
                values_count.append(account_stats[name])
            plt.barh(list(values_name.values()), values_count)
            plt.xlabel("Wartość"), plt.ylabel("Nazwa")
            plt.tight_layout()
            plt.savefig("images/file.png")

        def generate_tweets_hour_chart():
            hours_dict = account_stats["hourdict"]

            hours = []
            for i in range(10):
                hours.append("0" + str(i))
            for i in range(10, 24):
                hours.append(str(i))

            tweets_hour_count = []
            for hour in hours:
                if hour in list(hours_dict.keys()):
                    tweets_hour_count.append(hours_dict[hour])
                else:
                    tweets_hour_count.append(0)

            utc = timezone_to_string()

            plt.figure(figsize=(12, 5))

            plt.bar(hours, tweets_hour_count)
            plt.title("Wykres ilości publikowanych tweetów w zależności od godziny")
            plt.xlabel("Godzina UTC+" + utc)
            plt.ylabel("Ilość wstawionych tweetów")
            plt.ylim(0, max(list(hours_dict.values())) + 10)
            plt.tight_layout()
            plt.savefig("images/file.png")

        def generate_hashtag_chart():
            hashtag_dict = account_stats["hashtagdict"]
            sorted_hashtag = list((sorted(hashtag_dict.items(), key=lambda item: item[1])))[::-1]
            filter_hashtag = sorted_hashtag[:10]  # 10 most popular hashtags

            hashtag_name = [i[0] for i in filter_hashtag]
            hashtag_count = [i[1] for i in filter_hashtag]

            plt.figure(figsize=(12, 5))
            plt.barh(hashtag_name, hashtag_count)
            plt.title("Wykres 10 najczęściej występujących hashtagów")
            plt.xlabel("Ilość wystąpień hashtagu"), plt.ylabel("Nazwa hashtagu")
            plt.tight_layout()
            plt.savefig("images/file.png")

        matplotlib.use('Agg')  # block showing extra images
        plt.style.use('ggplot')
        if option == 0:
            pass
        elif option == 1:
            generate_statistics_chart()
        elif option == 2:
            generate_tweets_hour_chart()
        elif option == 3:
            generate_hashtag_chart()
        return True
