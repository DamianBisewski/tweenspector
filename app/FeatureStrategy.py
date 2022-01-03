from TweetsData import TweetsData


class FeatureStrategy:
    def __init__(self, option, username, search_words, date_from, date_to, tweets_count):
        self.program_feature = TweetsData(username, search_words, date_from, date_to, tweets_count)
        self.username = username
        self.tweets_count = tweets_count
        self.search_word = search_words
        self.Since = date_from
        self.Until = date_to

        if option == "Najczęstsze słowa":
            self.feature = UserWordConnection(self, username, search_words, date_from, date_to, tweets_count)
        elif option == "Powiązane konta":
            self.feature = RelatedPeopleConnection(self, username, search_words, date_from, date_to, tweets_count)
        elif option == "Informacja o koncie":
            self.feature = AccountsInfo(self, username, search_words, date_from, date_to, tweets_count)

    def generate_image(self):
        raise NotImplementedError('Please implement this method')

    def set_graph_label(self):
        raise NotImplementedError('Please implement this method')


class UserWordConnection(FeatureStrategy):
    def generate_image(self):
        self.program_feature.generate_word_cloud()

    def set_graph_label(self):
        return "Najczęściej używane słowa użytkownika " + str(self.username) + ", ostatnie " +\
               str(self.tweets_count) + " twetty"


class RelatedPeopleConnection(FeatureStrategy):
    def generate_image(self):
        self.program_feature.generate_interconnections_network()

    def set_graph_label(self):
        return "Sieć powiązanych użytkowników z " + str(self.username) + ", ostatnie " +\
               str(self.tweets_count) + " twetty"


class AccountsInfo(FeatureStrategy):
    def generate_image(self):
        self.program_feature.generate_user_stats()

    def set_graph_label(self):
        return "Informacja o koncie użytkownika " + str(self.username) + ", na podstawie ostatnich " +\
               str(self.tweets_count) + " twettów"
