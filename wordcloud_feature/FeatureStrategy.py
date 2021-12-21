from TweetsData import TweetsData


class FeatureStrategy:
    def __init__(self, option, username, tweets_count):
        self.program_feature = TweetsData(username, tweets_count)
        self.username = username
        self.tweets_count = tweets_count

        if option == "Najczęstsze słowa":
            self.feature = UserWordConnection(self, username, tweets_count)
        elif option == "Powiązane konta":
            self.feature = RelatedPeopleConnection(self, username, tweets_count)
        elif option == "Konta podobne":
            self.feature = UserSimilarAccounts(self, username, tweets_count)

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
        self.program_feature.generate_another_one()

    def set_graph_label(self):
        return "Sieć powiązanych użytkowników z " + str(self.username) + ", ostatnie " +\
               str(self.tweets_count) + " twetty"


class UserSimilarAccounts(FeatureStrategy):
    def generate_image(self):
        print("user similarity accounts image there")

    def set_graph_label(self):
        return "Konta podobne użytkownika " + str(self.username) + ", ostatnie " +\
               str(self.tweets_count) + " twetty"
