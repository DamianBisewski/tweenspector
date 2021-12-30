import twint
from wordcloud import WordCloud, STOPWORDS
import morfeusz2
import matplotlib.pyplot as plt
import re
import networkx as nx
import igraph

class TweetsData:
    def __init__(self, username, num_of_tweets=500):
        self.morf = morfeusz2.Morfeusz()
        self.username = username
        self.num_of_tweets = num_of_tweets

    def get_tweets(self):
        try:
            c = twint.Config()
            c.Username = self.username
            c.Limit = self.num_of_tweets
            c.Pandas = True
            c.Pandas_clean = True
            print(twint.run.Search(c))
            return twint.output.panda.Tweets_df[["username", "tweet"]]
        except ValueError:
            print("Taki uzytkownik nie istnieje")

    def generate_word_cloud(self):
        tweets = self.get_tweets()
        try:
            text1 = tweets.tweet.values
            stopwords = set(STOPWORDS)
            file = open("stopwords.txt", "r", encoding="utf8")
            word = file.readline().replace('\n', '')
            while word:
                stopwords.add(word)
                word = file.readline().replace('\n', '')
            wordcloud = WordCloud(
                background_color='black',
                width=1000,
                height=500,
                stopwords=stopwords).generate(str(text1))
            wordcloud.to_file("file.png")
        except ValueError:
            print("warning")

    # users account connections feature
    def generate_another_one(self):
        tweets = self.get_tweets()
        try:
            g = igraph.Graph()
            users = set()
            rtsmts = set()
            rtsmts.add(self.username)
            g.add_vertices(1)
            G_retweet = nx.DiGraph()
            G_mention = nx.DiGraph()
            for r in tweets.iterrows():
                author = r[1]['username']
                author = f'@{author}'
                text = r[1]['tweet']
                rts = set(re.findall(r"RT @(\w+)", text))
                mts = set(re.findall(r"@(\w+)", text))
                for rt in rts:
                    rt = rt.lower()
                    rtsmts.add(rt)
                for mt in mts:
                    mt = mt.lower()
                    rtsmts.add(mt)
            num = len(rtsmts)
            g.add_vertices(num - 1)
            g.vs["name"] = rtsmts
            interactions = list(rtsmts)
            x = 0
            for i in range(0, num):
                if interactions[i] == self.username:
                    x = i
            for i in range(0, num):
                if x != i:
                    g.add_edges([(x, i)])
            print(g)
            layout = g.layout("drl")
            igraph.plot(g, "file.png", layout=layout, vertex_label=rtsmts, bbox=(1500, 900), margin=30, vertex_label_dist=2,
                        vertex_size=3)

        except ValueError:
            print("warning")
