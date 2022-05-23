from TweetsData import TweetsData


class FeatureStrategy:
    def __init__(self, user_name, search_words, date_from, date_to, tweets_count, option=0):
        self.program_feature = TweetsData(user_name, search_words, date_from, date_to, tweets_count)
        self.user_name = user_name
        self.tweets_count = tweets_count
        self.search_word = search_words
        self.Since = date_from
        self.Until = date_to
        self.option = option

    def generate_image(self):
        raise NotImplementedError('Please implement this method')


class UserWordConnection(FeatureStrategy):
    def generate_image(self):
        return self.program_feature.generate_word_cloud()


class RelatedPeopleConnection(FeatureStrategy):
    def generate_image(self):
        return self.program_feature.generate_interconnections_network(self.option)


class AccountsInfo(FeatureStrategy):
    def generate_image(self):
        return self.program_feature.generate_user_stats(self.option)
