import twint
import pandas
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import nltk
import collections
import numpy as np
import morfeusz2
import spacy
#def cleanup(text):
#    to_dump = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789"       #czyscimy z cyfr, znakow przestankowych, nawiasow i innych znakow
#    tr = str.maketrans("", "", to_dump)
#    return text.translate(tr)

morf = morfeusz2.Morfeusz()
def get_tweets(search, date_from, date_to):
    c = twint.Config()
    c.Username = search
    c.Since = date_from
    c.Until = date_to
    c.Pandas = True
    c.Pandas_clean = True
    twint.run.Search(c)
    #print(twint.run.Search(c))
    return twint.output.panda.Tweets_df[["username","tweet"]]
# tweets = get_tweets("data science", limit=10000)
# tweets.count() # 10003
def generate_word_cloud(tweets):
    stopwords = set(STOPWORDS)
    file = open("stopwords.txt", "r", encoding="utf8")
    word = file.readline().replace('\n', '')
    while word:
        stopwords.add(word)
        word = file.readline().replace('\n', '')
    text1 = tweets.tweet.values# adding movie script specific stopwords
    nlp = spacy.load("pl_core_news_lg")
    text2 = nlp(str(text1))
    text3 = ''
    for t in text2:
        print(f"{t.text:<8} => {t.lemma_:<8}")
        if t.lemma_ not in stopwords:
            print(text3)
            text3 = text3 + ' ' + t.lemma_
    #for text in text1:
#        analysis = morf.analyse(text)
#        for interpretation in analysis:
#            print(interpretation)
    #text = cleanup(text)
    wordcloud = WordCloud(
        background_color = 'black',
        colormap = 'Pastel1',
        width = 1000,
        height = 500,
        stopwords = stopwords).generate(str(text3))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.rcParams['figure.figsize'] = [10, 10]
    plt.show()
usrname = input("Podaj nazwe uzytkownika: ")
date_from = input("Podaj date poczatkowa wyszukiwania tweetow: ")
date_to = input("Podaj date koncowa wyszukiwania tweetow: ")
#num_of_tweets = input("Podaj liczbe ostatnich tweetow: ")
tweets = get_tweets(usrname, date_from, date_to)
generate_word_cloud(tweets)

#testy jednostkowe
#docelowo osobne pliki
#powinny wykonywać się szybko
#Jednostką metoda
#
