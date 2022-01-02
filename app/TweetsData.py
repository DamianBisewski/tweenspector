import twint
from wordcloud import WordCloud, STOPWORDS
import morfeusz2
import matplotlib.pyplot as plt
import re
import networkx as nx
import igraph
import time

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
            c.Retweets = True
            c.Pandas_clean = True
            print(twint.run.Profile(c))
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
        time.sleep(3)
        try:
            def get_friend_tweets(username):
                n_count = 5
                while True :
                    con = twint.Config()
                    con.Username = username
                    con.Limit = self.num_of_tweets
                    con.Pandas = True
                    con.Pandas_clean = True
                    con.Retweets = True
                    twint.run.Profile(con)
                    n_count = n_count - 1
                    if n_count == 0:
                        break
                    if not twint.output.panda.Tweets_df.empty:
                        break
                if twint.output.panda.Tweets_df.empty:
                    print("No tweets from user: ", username)
                    return twint.output.panda.Tweets_df
                else:
                    return twint.output.panda.Tweets_df[["username", "tweet"]]
            g = igraph.Graph(directed=True)
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
            rtsmts = get_friends(self)
            for rtmt in rtsmts:
                print("Dodaje wierzcholek", rtmt)
                g.add_vertex(rtmt)
            vertex_names = g.vs["name"]
            color = ["blue" if vertex_name==self.username else "red" for vertex_name in vertex_names]
            print(g)
            for someone in rtsmts:
                friend_tweets = get_friend_tweets(someone)
                time.sleep(5)
                for r in friend_tweets.iterrows():
                    text = r[1]['tweet']
                    mts = set(re.findall(r"@(\w+)", text))
                    for mt in mts:
                        mt = mt.lower()
                        if mt in rtsmts:
                            if mt != someone:
                                print("adding edge between", someone, " and ", mt)
                                g.add_edge(someone, mt)
            layout = g.layout("drl")
            igraph.plot(g, "file.png", layout=layout, vertex_label=rtsmts, vertex_color=color, bbox=(4500, 2700), margin=30, vertex_label_dist=2,
                        vertex_size=40)

        except ValueError:
            print("warning")
    def generate_user_stats(self):
        def user_stats_to_csv(self):
              try:
                  file = self.username + "_stats.csv"
                  if(os.path.exists(file) and os.path.isfile(file)):
                      os.remove(file)
                  c = twint.Config()
                  c.Username = self.username
                  c.Store_csv = True
                  c.Limit = self.num_of_tweets
                  c.Pandas = True
                  c.Retweets = True
                  c.Pandas_clean = True
                  c.Profile_full = True
                  c.Output = self.username + "_stats.csv"
                  print(twint.run.Profile(c))
                  #return twint.output.panda.Tweets_df[["username", "tweet", "date", "time", "likes_count", "retweets_count", "geo", "hashtags", "mentions"]]
              except ValueError:
                  print("Taki uzytkownik nie istnieje")
        def get_user_stats(self):
            stats = pd.read_csv(self.username+"_stats.csv")
            return stats
        user_stats_to_csv()
        stats = get_user_stats()
        print(stats)
