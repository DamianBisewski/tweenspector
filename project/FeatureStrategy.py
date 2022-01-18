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
        elif option == "Statystyki użytkownika":
            self.feature = AccountsInfo(self, username, search_words, date_from, date_to, tweets_count)

    def generate_image(self):
        raise NotImplementedError('Please implement this method')

    def get_tweets(self, text_input, search_words, date_from, date_to, tweets_count):
        raise NotImplementedError('Please implement this method')


class UserWordConnection(FeatureStrategy):
    def generate_image(self, option=0):
        self.program_feature.generate_word_cloud()

    def get_tweets(self, text_input, search_words, date_from, date_to, tweets_count):
        return self.program_feature.get_tweets(text_input, search_words, date_from, date_to, tweets_count)


class RelatedPeopleConnection(FeatureStrategy):
    def generate_image(self, option=0):
        self.program_feature.generate_interconnections_network()

    def get_tweets(self, text_input, search_words, date_from, date_to, tweets_count):
        return self.program_feature.get_tweets(text_input, search_words, date_from, date_to, tweets_count)


class AccountsInfo(FeatureStrategy):
    def generate_image(self, option=0):
        self.program_feature.generate_user_stats(option)

    def get_tweets(self, text_input, search_words, date_from, date_to, tweets_count):
        return self.program_feature.get_tweets(text_input, search_words, date_from, date_to, tweets_count)
