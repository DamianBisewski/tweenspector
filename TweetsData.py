import twint
from wordcloud import WordCloud, STOPWORDS
import morfeusz2
import re
import igraph
import pandas as pd
import statistics
import spacy
import pl_core_news_lg
import matplotlib.pyplot as plt
import matplotlib
from App_variables import *


def save_tweets_df_to_csv(filename, tweets_df):
    tweets_df.to_csv(filename)


def load_tweets_df_form_csv(filename):
    return pd.read_csv(filename)


class TweetsData:
    def __init__(self, username, search_words, date_from, date_to, num_of_tweets=500):
        self.morf = morfeusz2.Morfeusz()
        self.username = username
        self.num_of_tweets = num_of_tweets
        self.num_of_tweets_read = 0
        self.Since = date_from
        self.Until = date_to
        self.search_words = search_words
        self.test_mode = False
        self.wordcloud = None  # test mode only
        self.account_stats = None  # test mode only
        self.interconnection_graph = None    # test mode only

    def test_mode_enable(self):
        self.test_mode = True

    def test_mode_disable(self):
        self.test_mode = False

    def test_mode_enabled(self):
        return self.test_mode

    def check_username(self):
        pass

    def get_tweets(self, username, search_words, date_from, date_to, num_of_tweets):
        if self.test_mode_enabled():
            print('TEST MODE: loading tweets from disc')
            df = load_tweets_df_form_csv(username + '.csv')
            self.num_of_tweets_read = df.shape[0]
            return df
        try:
            c = twint.Config()
            c.Username = username
            c.Limit = num_of_tweets
            c.Pandas = True
            c.Retweets = True
            c.Pandas_clean = True
            c.Stats = True
            c.Count = True
            c.Since = date_from
            c.Until = date_to
            c.Search = search_words
            twint.run.Profile(c)
            self.num_of_tweets_read = twint.output.panda.Tweets_df.shape[0]
            print('Number of tweets read: ', self.num_of_tweets_read)
            #if self.test_mode_enabled():
            #    print('saving')
            #    save_tweets_df_to_csv(username + '.csv', twint.output.panda.Tweets_df)
            if twint.output.panda.Tweets_df.empty:
                print("No tweets from user: ", username)
                return twint.output.panda.Tweets_df
            else:
                return twint.output.panda.Tweets_df  # [["username", "tweet"]]
        except ValueError:
            return False

    def generate_word_cloud(self):
        tweets = self.get_tweets(self.username, self.search_words, self.Since, self.Until, self.num_of_tweets, )
        print(tweets.tweet)
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
            if lemmatizer_enabled:
                original_tweets_text = tweets.tweet.values  # adding movie script specific stopwords
                # nlp = spacy.load("pl_core_news_lg")
                nlp = pl_core_news_lg.load()
                tweets_text_from_lemmatizer = nlp(str(original_tweets_text))
                preprocessed_tweets_text = ''
                for t in tweets_text_from_lemmatizer:
                    # print(f"{t.text:<8} => {t.lemma_:<8}")
                    if t.lemma_ not in stopwords:
                        # print("added")
                        preprocessed_tweets_text = preprocessed_tweets_text + ' ' + t.lemma_
                    # else:
                        # print("filtered")
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
        except ValueError:
            print("warning")

    # users account connections feature
    def generate_interconnections_network(self):
        tweets = self.get_tweets(self.username, self.search_words, self.Since, self.Until, self.num_of_tweets)
        print(type(tweets))
        try:
            def get_friends(self):
                rtsmts = set()
                rtsmts.add(self.username)
                for r in tweets.iterrows():
                    text = r[1]['tweet']
                    mts = set(re.findall(r"@(\w+)", text))
                    for mt in mts:
                        mt = mt.lower()
                        rtsmts.add(mt)
                return rtsmts
            g = igraph.Graph(directed=True)
            rtsmts = get_friends(self)
            for rtmt in rtsmts:
                print("Adding vertex: ", rtmt)
                g.add_vertex(rtmt)
            print(g)
            relations = dict()
            for someone in rtsmts:
                relations[someone] = dict()
                friend_tweets = self.get_tweets(someone, self.search_words, self.Since, self.Until, self.num_of_tweets)
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
                print(temp)
                for key, value in temp.items():
                    g.add_edge(someone, key)
            visual_style = {}
            visual_style["vertex_size"] = 40
            visual_style["vertex_label_size"] = 50
            visual_style["vertex_label_dist"] = 2
            visual_style["margin"] = 250
            visual_style["bbox"] = (5000, 3000)
            visual_style["vertex_color"] = ["blue" if vertex_name == self.username else "red" for vertex_name in
                                            g.vs["name"]]
            visual_style["vertex_label"] = rtsmts
            visual_style["layout"] = g.layout("circle")
            visual_style["edge_width"] = [relations[g.vs[edge.source]["name"]][g.vs[edge.target]["name"]] for edge in
                                          g.es]
            # visual_style["edge_label"] = [str(relations[g.vs[edge.source]["name"]][g.vs[edge.target]["name"]]) for edge in
            #                              g.es]
            visual_style["edge_arrow_width"] = [relations[g.vs[edge.source]["name"]][g.vs[edge.target]["name"]] for edge
                                                in g.es]
            igraph.plot(g, "images/file.png", **visual_style)
            if self.test_mode_enabled():
                self.interconnection_graph = g
        except ValueError:
            print("warning")

    def generate_user_stats(self, option):
        def generate_account_info(df):
            print(df)
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
            print(df.retweet)
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
            print("avglikes ", account_stats['avglikes'])
            print(account_stats['maxlikes'])
            print(account_stats['minlikes'])
            print(account_stats['medianlikes'])
            print(account_stats['avgretweets'])
            print(account_stats['maxretweets'])
            print(account_stats['minretweets'])
            print(account_stats['medianretweets'])
            print(type(account_stats['interval']))
            print(account_stats['interval'])
            if account_stats['places']:
                print(account_stats['places'])
            else:
                print("No places found.")
            print("hashtagdict ", account_stats['hashtagdict'])
            print(account_stats['usersdict'])
            print(account_stats['hourdict'])
            return account_stats

        data_frame = self.get_tweets(self.username, self.search_words, self.Since, self.Until, self.num_of_tweets)
        account_stats = generate_account_info(data_frame)
        if self.test_mode_enabled():
            self.account_stats = account_stats
        print(account_stats)

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