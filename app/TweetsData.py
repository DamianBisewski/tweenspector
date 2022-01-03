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
import statistics
import datetime
import numpy as np
import spacy


class TweetsData:
    def __init__(self, username, search_words, date_from, date_to, num_of_tweets=500):
        self.morf = morfeusz2.Morfeusz()
        self.username = username
        self.num_of_tweets = num_of_tweets
        self.Since = date_from
        self.Until = date_to
        self.search_words = search_words

    def get_tweets(self, username, search_words, date_from, date_to, num_of_tweets):
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
            # testing = True
            # if testing:
            #    twint.output.panda.Tweets_df.to_csv(username)
            if twint.output.panda.Tweets_df.empty:
                print("No tweets from user: ", username)
                return twint.output.panda.Tweets_df
            else:
                return twint.output.panda.Tweets_df  # [["username", "tweet"]]
        except ValueError:
            print("Invalid username", username)

    def generate_word_cloud(self):
        tweets = self.get_tweets(self.username, self.search_words, self.Since, self.Until, self.num_of_tweets, )
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
                    print(f"{t.text:<8} => {t.lemma_:<8}")
                    if t.lemma_ not in stopwords:
                        print("added")
                        preprocessed_tweets_text = preprocessed_tweets_text + ' ' + t.lemma_
                    else:
                        print("filtered")
            else:
                preprocessed_tweets_text = tweets.tweet.values
            wordcloud = WordCloud(
                background_color='black',
                colormap='Pastel1',
                width=1000,
                height=500,
                stopwords=stopwords).generate(str(preprocessed_tweets_text))
            wordcloud.to_file("file.png")
        except ValueError:
            print("warning")

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

        except ValueError:
            print("warning")

    def generate_user_stats(self):

        def generate_account_info(df):
            print(df)

            date1 = pd.to_datetime(df.iloc[0].date)
            date2 = pd.to_datetime(df.iloc[int(self.num_of_tweets) - 1].date)
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
            account_stats = {'avglikes': sum(df[df.retweet == False].nlikes) / len(df[df.retweet == False].nlikes),
                             'maxlikes': max(df[df.retweet == False].nlikes),
                             'minlikes': min(df[df.retweet == False].nlikes),
                             'medianlikes': statistics.median(df[df.retweet == False].nlikes),
                             'avgretweets': sum(df[df.retweet == False].nretweets) /
                                            len(df[df.retweet == False].nretweets),
                             'maxretweets': max(df[df.retweet == False].nretweets),
                             'minretweets': min(df[df.retweet == False].nretweets),
                             'medianretweets': statistics.median(df[df.retweet == False].nretweets),
                             'interval': (date1 - date2) / (int(self.num_of_tweets) - 1),
                             'places': set(),
                             'hashtagdict': dict(),
                             'usersdict': dict(sorted(usersdict.items(), key=lambda x: x[1])),
                             'hourdict': dict(sorted(hourdict.items(), key=lambda x: x[1]))}
            for place in df.place:
                if place != '':
                    account_stats['places'].add(place)
            for hashtags in df.hashtags:
                for hashtag2 in hashtags:
                    prochashtags = hashtag2.strip("[]")
                    proc2hashtags = prochashtags.split(", ")
                    for hashtag in proc2hashtags:
                        hashtag.strip(" ")
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
        print(account_stats)  # TBD to trzeba wyswietlic w GUI
