import pandas
import twint
from wordcloud import WordCloud, STOPWORDS
import morfeusz2
import matplotlib.pyplot as plt
import re
import networkx as nx
import igraph
import time
import pandas as pd
import os
import sys
import statistics
import datetime
import numpy as np
import spacy
from datetime import timedelta

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
            print("Invalid username", username)

    def generate_word_cloud(self):
        tweets = self.get_tweets(self.username, self.search_words, self.Since, self.Until, self.num_of_tweets, )
        print(tweets.tweet)
        try:
            stopwords = set(STOPWORDS)
            lemmatizer_enabled = True
            file = open("stopwords.txt", "r", encoding="utf8")  # TBD dodac obsluge nieudanego otwarcia pliku
            word = file.readline().replace('\n', '')
            while word:
                stopwords.add(word)
                word = file.readline().replace('\n', '')
            preprocessed_tweets_text = ''
            original_tweets_text = ''
            if lemmatizer_enabled:
                original_tweets_text = tweets.tweet.values  # adding movie script specific stopwords
                nlp = spacy.load("pl_core_news_lg")
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
                wordcloud.to_file("file.png")
        except ValueError:
            print("warning")

    def wordcloud_test1_check(self):
        sample = {'świat': 1, 'zdęboeć': 1, 'wywiad': 1, 'polski': 1, 'premier': 1, 'zapowiadać': 1, 'wojna': 1, 'światowy': 1, 'wywołaną': 1, 'konflikt': 1, 'Polska': 2, 'unia': 1, 'europejski': 1, 'polityka': 1, 'głupota': 1, 'przyczyna': 1, 'większość': 1, 'poważny': 1, 'nieszczęście': 1, 'Alo': 1, 'mieć': 2, 'kot': 1, 'kota': 1, 'Ala': 1, 'doprowadzić': 1, 'katastrofa': 1, 'wina': 1, 'zrzucić': 1, 'ofiara': 1, 'niszczyć': 1, 'żyto': 1, 'czas': 1, 'kłamać': 1, 'zmuszać': 1, 'kłamstwo': 1, 'byle': 1, 'uniknąć': 1, 'odpowiedzialność': 1, 'zrobić': 1, 'Sebastian': 1, 'seicento': 1}
        if sample == self.wordcloud:
            return True
        else:
            print("Expected: ", sample)
            print("Received: ", self.wordcloud)
            return False

    # users account connections feature
    def generate_interconnections_network(self):
        tweets = self.get_tweets(self.username, self.search_words, self.Since, self.Until, self.num_of_tweets)
        try:
            def get_friends(self):
                # rtsmts.add(self.username)
                rtsmts = set()
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
            visual_style["layout"] = g.layout("drl")
            visual_style["edge_width"] = [relations[g.vs[edge.source]["name"]][g.vs[edge.target]["name"]] for edge in
                                          g.es]
            # visual_style["edge_label"] = [str(relations[g.vs[edge.source]["name"]][g.vs[edge.target]["name"]]) for edge in
            #                              g.es]
            visual_style["edge_arrow_width"] = [relations[g.vs[edge.source]["name"]][g.vs[edge.target]["name"]] for edge
                                                in g.es]
            igraph.plot(g, "file.png", **visual_style)
            if self.test_mode_enabled():
                self.interconnection_graph = g
        except ValueError:
            print("warning")

    def generate_user_stats(self):

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
            print(account_stats['avglikes'])
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
            print(account_stats['hashtagdict'])
            print(account_stats['usersdict'])
            print(account_stats['hourdict'])
            return account_stats

        data_frame = self.get_tweets(self.username, self.search_words, self.Since, self.Until, self.num_of_tweets)
        account_stats = generate_account_info(data_frame)
        if self.test_mode_enabled():
            self.account_stats = account_stats
        print(account_stats)  # TBD to trzeba wyswietlic w GUI
    def account_info_test1_check(self):
        intervalexp = pd.Timedelta('0 days 01:45:30.313131313')
        sample = {'avglikes': 8, 'maxlikes': 75, 'minlikes': 0, 'medianlikes': 1.0, 'avgretweets': 2, 'maxretweets': 29, 'minretweets': 0, 'medianretweets': 0.0, 'interval': intervalexp, 'places': set(), 'hashtagdict': {'comirnaty': 1, 'covid_19': 1, "zaszczepsię'": 2, " 'mojeikp": 2, 'mojeikp': 5, "comirnaty'": 1, " 'omicron'": 1, " 'delta": 1, 'szczecin': 1, 'szczepimysię': 1, 'fakenews': 1, 'koronawirus': 1}, 'usersdict': {'tgidelski': 1, 'marekma32433534': 1, 'lazy_climber_': 1, 'pbeatap': 1, 'soipruk': 1, 'sjastrzebowski': 1, 'why_duck_': 1, 'radekpiasecki1': 1, 'krzyszt05935814': 1, 'zuzanna50267266': 1, 'cwik_aw': 1, 'mefistofelleess': 1, 'ema_news': 1, 'makrawczyk1': 1, 'valdikasator': 1, 'boguckizbigniew': 1, 'st_feu': 1, 'ania_curly': 1, 'davoff994_d': 1, 'filip77341432': 1, 'pdutkals': 1, 'caletomasz': 1, 'andrzejduda': 1, 'polsatnewspl': 1, 'prezydentpl': 1, 'bealooa': 2, 'kolusiamiki': 2, 'unnuna': 2, 'prokurent74': 2, 'r_a_ziemkiewicz': 2, 'kasperson36': 2, 'pawelbartosik': 2, 'rafal81981747': 2, 'joanna_czarna': 2, 'danuta29827246': 2, 'miroka30045644': 2, 'michaldworczyk': 2, 'osieckanguyet': 2, 'ryszard39144183': 2, 'waldekkraska': 2, 'maswitala': 2, 'tvp': 2, 'adam_giza': 2, 'aldowiwi1': 2, 'wojt_pcimia': 2, 'gfkot': 2, 'annazorba': 2, 'wojtekwojtula': 2, 'teryasic1': 3, 'klubnauer': 3, 'placzekgrzegorz': 4, 'katarzyna_ts': 4, 'ordomedicus': 4, 'iwona_paulewicz': 4, 'gcessak': 6, 'szczepienie': 6, 'piotrwitczak_': 7, 'a_niedzielski': 8, 'mz_gov_pl': 24}, 'hourdict': {18: 1, 9: 2, 19: 3, 12: 4, 16: 8, 17: 10, 13: 10, 10: 12, 11: 13, 15: 15, 14: 22}}
        if self.account_stats == sample:
            return True
        else:
            print("Expected: ", sample)
            print("Received: ", self.account_stats)
            return False
