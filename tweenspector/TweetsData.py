import twint
from wordcloud import WordCloud
import re
import igraph
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import matplotlib
import math
from App_variables import *
import spacy
import html

def save_tweets_df_to_csv(filename, tweets_df):   #zapis wczytanych tweetów do CSV
    tweets_df.to_csv(filename)


def load_tweets_df_from_csv(filename):    #wczytanie tweetów z CSV
    return pd.read_csv(filename)


class TweetsData:       #tworzymy obiekt klasy TweetsData, który ma wszystkie metody potrzebne do wczytania tweetów i prezentacji danych
    def __init__(self, user_name, search_words, date_from, date_to, num_of_tweets=500):
        self.user_name = user_name                #nazwa użytkownika, liczba tweetów, daty od/do, a także poszukiwane słowa
        self.num_of_tweets = num_of_tweets
        self.num_of_tweets_read = 0
        self.Since = date_from
        self.Until = date_to
        self.search_words = search_words

    def get_tweets(self, user_name, search_words, date_from, date_to, num_of_tweets):   #wczytanie tweetów
        try:                        #w przeciwnym razie konfigurujemy Twinta
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
            if twint.output.panda.Tweets_df.empty:    #jeśli nie znaleziono tweetów to informujemy o tym
                print("No tweets from user: ", user_name)
                return twint.output.panda.Tweets_df
            else:                                     #zwracamy pustą lub pełną ramke danych
                return twint.output.panda.Tweets_df
        except ValueError:                     #obsługujemy potencjalne wyjątki
            print("Get tweets - Blad wartosci, user:", user_name)
            return pd.DataFrame()
        except Exception as exc:
            print("Get tweets - Cos poszlo nie tak, user: {user}, wyjatek: {excType} {excMsg}"
                  .format(user=user_name, excType=type(exc).__name__, excMsg=str(exc)))
            return pd.DataFrame()

    def generate_word_cloud(self):
        worldcloud = self.create_word_cloud()
        return worldcloud is not None

    def create_word_cloud(self): #tutaj tworzymy mapę słów
        tweets = self.get_tweets(self.user_name, self.search_words, self.Since, self.Until, self.num_of_tweets)
        if tweets.empty:                   #wczytujemy tweety, jeśli brak tweetów to wychodzimy
            return None
        try:
            lemmatizer_enabled = True      #włączamy lematyzer
            preprocessed_tweets_text = ''              #tu tekst tweetów po przetworzeniu
            original_tweets_text = ''
            nlp = spacy.load("pl_core_news_lg")
            for tweet in tweets.iterrows():           #tutaj kolejno szukamy wspominków o innych kontach by dodać je do słów nieznaczących
                text = tweet[1]['tweet']
                # w pierwszym kroku odflitrowujemy wszystkie linki http/https
                lst = re.findall('http://\S+|https://\S+', text)
                for i in lst:
                    text = text.replace(i, '')
                # w kolejnym usuwamy wszystkie odwoloania do @nazwa
                lst = re.findall(r"(@\w+)", text)
                for i in lst:
                    text = text.replace(i, '')
                if lemmatizer_enabled:               #tutaj lematyzacja słów
                    stopwords = nlp.Defaults.stop_words
                    stopwords.add("RT")
#                    original_tweets_text = tweets.tweet.values
                    tweets_text_from_lemmatizer = nlp(str(text))    #kolejno lematyzujemy wszystkie słowa
#                    preprocessed_tweets_text = ''
                    for t in tweets_text_from_lemmatizer:     #do tekstu do przetworzenia dodajemy tylko słowa znaczące
                        if t.lemma_ not in stopwords:
                            strtoken = html.unescape(t.lemma_)
                            preprocessed_tweets_text = preprocessed_tweets_text + ' ' + strtoken
                else:
                    preprocessed_tweets_text = tweets.tweet.values    #gdyby lematyzer był wyłączony to w tekście wszystkie słowa
            #tu rysujemy mapę słów
            wordcloud = WordCloud(
                background_color='black',
                colormap='Pastel1',
                width=1000,
                height=500,
                stopwords=stopwords,
                regexp=r"\w[\w'\&\-]*\w")
            wordcloud_img = wordcloud.generate(str(preprocessed_tweets_text))
            wordcloud_img.to_file("images/file.png")    #mapę słów można zapisać
            return wordcloud, preprocessed_tweets_text
        except ValueError:                  #obsługa wyjątków
            print("Generate word cloud - Blad wartosci")
            return None
        except Exception as exc:
            print("Generate word cloud - Cos poszlo nie tak: {excType} {excMsg}"
                  .format(excType=type(exc).__name__, excMsg=str(exc)))
            return None

    def generate_interconnections_network(self, option):
        interconnections_network = self.create_interconnections_network(option)
        return interconnections_network is not None

    def create_interconnections_network(self, option): #tu utworzenie grafu powiązań
        tweets = self.get_tweets(self.user_name, self.search_words, self.Since, self.Until, self.num_of_tweets)
        if tweets.empty:
            return None
        try:
            def get_friends():               #szukamy wszystkich wspominków danego konta o innych by mieć wierzchołki grafu
                rtsmts = set()
                rtsmts.add(self.user_name.lower())
                for r in tweets.iterrows():
                    text = r[1]['tweet']
                    mts = set(re.findall(r"@(\w+)", text))
                    for mt in mts:
                        mt = mt.lower()
                        rtsmts.add(mt)
                return rtsmts
            g = igraph.Graph(directed=True)   #tworzymy graf
            rtsmts = get_friends()
            for rtmt in rtsmts:
                g.add_vertex(rtmt)          #tu dodajemy wierzchołki
            relations = dict()
            for someone in rtsmts:
                relations[someone] = dict()    #kolejno zliczamy interakcje użytkowników grafu ze sobą
                friend_tweets = self.get_tweets(someone, self.search_words, self.Since, self.Until, self.num_of_tweets)
                if friend_tweets.empty:       # w razie braku tweetów danego użytkownika informujemy o tym i idziemy dalej
                    print("Generate interconnections network - Brak konta, user:", someone)
                    continue
                for r in friend_tweets.iterrows():      #zliczanie odbywa się tutaj, interakcja to wspomnienie jednego użytkownika o drugim
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
                for key, value in temp.items():       #tutaj dodajemy krawędzie do grafu, grubość krawędzi zależy od liczby interakcji między dwoma kontami
                    g.add_edge(someone, key)
            x = 1000 * math.log(len(rtsmts))               #tu ustawiamy rozdzielczość
            y = 600 * math.log(len(rtsmts))
            visual_style = {                      #tu ustawiamy jak graf ma wyglądać
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
            if option == "Optimal Modularity":              #tutaj jest obsługa wyboru metody grupowania kont
                comm = g.community_optimal_modularity()
            elif option == "Spinglass":
                comm = g.community_spinglass()
            elif option == "Label Propagation":
                comm = g.community_label_propagation()
            elif option == "Infomap":
                comm = g.community_infomap()
            else:
                return None
            igraph.plot(comm, "images/file.png", **visual_style, mark_groups=True)    #graf można zapisać do pliku
            return g
        except ValueError:
            print("Generate interconnections network - Blad wartosci")     #obsługa wyjątków
            return None
        except Exception as exc:
            print("Generate interconnections network - Cos poszlo nie tak: {excType} {excMsg}"
                  .format(excType=type(exc).__name__, excMsg=str(exc)))
            return None

    def generate_user_stats(self, option):
        user_stats = self.create_user_stats(option)
        return user_stats is not None
    
    def create_user_stats(self, option): #tu obliczmy statystyki konta
        def generate_account_info(df):
            date1 = pd.to_datetime(df.iloc[0].date)
            date2 = pd.to_datetime(df.iloc[int(self.num_of_tweets_read) - 1].date)
            usersdict = dict()
            for tweet in df.tweet:           #zliczamy wspominki o innych kontach
                mts = set(re.findall(r"@(\w+)", tweet))
                for mt in mts:
                    mt = mt.lower()
                    if mt in usersdict:
                        usersdict[mt] = usersdict[mt] + 1
                    else:
                        usersdict[mt] = 1
            hourdict = dict()           #zliczamy tweety wg godzin napisania
            for hour in df.hour:
                if hour in hourdict:
                    hourdict[hour] = hourdict[hour] + 1
                else:
                    hourdict[hour] = 1
            account_stats = {             #tutaj przechowujemy wszystkie statystyki
                'avglikes': round(sum(df[df.retweet == False].nlikes) / len(df[df.retweet == False].nlikes)),   #średnia, maksimum, minimum i mediana liczby polubień i udostępnień
                'maxlikes': max(df[df.retweet == False].nlikes),
                'minlikes': min(df[df.retweet == False].nlikes),
                'medianlikes': statistics.median(df[df.retweet == False].nlikes),
                'avgretweets': round(sum(df[df.retweet == False].nretweets) /
                                     len(df[df.retweet == False].nretweets)),
                'maxretweets': max(df[df.retweet == False].nretweets),
                'minretweets': min(df[df.retweet == False].nretweets),
                'medianretweets': statistics.median(df[df.retweet == False].nretweets),
                'interval': (date1 - date2) / (int(self.num_of_tweets_read) - 1),       #średni odstęp między tweetami
                'places': set(),                    #miejsca, z których pisano
                'hashtagdict': dict(),              #hasztagi, których użyto
                'usersdict': dict(sorted(usersdict.items(), key=lambda x: x[1])),    #uzytkownicy, o których wspomniano
                'hourdict': dict(sorted(hourdict.items(), key=lambda x: x[1]))}     #i godziny napisania

            for place in df.place:               #tu miejsca, z których pisano są zliczane
                if place != '':
                    account_stats['places'].add(place)

            # for hashtags loaded from tweeter twint provides them as list of strings
            for hashtags in df.hashtags:
                for hashtag in hashtags:
                    if hashtag:
                        if hashtag in account_stats['hashtagdict']:
                            account_stats['hashtagdict'][hashtag] = account_stats['hashtagdict'][hashtag] + 1
                        else:
                            account_stats['hashtagdict'][hashtag] = 1
            return account_stats

        data_frame = self.get_tweets(self.user_name, self.search_words, self.Since, self.Until, self.num_of_tweets)   #by mieć statystyki potrzebujemy tweetów
        if data_frame.empty:
            return None
        account_stats = generate_account_info(data_frame)

        def generate_statistics_chart():              #wyświetlenie wykresu popularności (liczby polubień i udostępnień)
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

        def generate_tweets_hour_chart():           #wyświetlenie wykresu godzin, o których pisano wg UTC+1
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

        def generate_hashtag_chart():              #wyświetlenie najczęściej użytych hasztagów
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
        else:
            return None
        return account_stats

