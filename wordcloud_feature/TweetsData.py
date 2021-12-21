import twint
from wordcloud import WordCloud, STOPWORDS
import morfeusz2
import matplotlib.pyplot as plt


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

    def generate_another_one(self):
        plt.figure()
        plt.suptitle("Hello another one!")
        plt.savefig("file.png")
