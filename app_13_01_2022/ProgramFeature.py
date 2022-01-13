from nltk.corpus import wordnet as wn
from Data import get_data_dictionary


class ProgramFeature:
    def __init__(self, username, tweets_count):
        # self.user_topic_dict = {'AA': [('movie', 10), ('cinema', 8), ('cheese', 4), ('milk', 2), ('food', 4),
        #                                ('river', 6), ('lake', 2)]}
        self.user_topic_dict = {username: get_data_dictionary(username, tweets_count)}

    def words_to_words(self, person, precision):
        word_similarity_list = self.words_path_similarity_list(person)
        # print("word_similarity_list: ", word_similarity_list)
        path_similarity_min, path_similarity_max = self.set_precision_min_max(person)
        scale = path_similarity_min + ((path_similarity_max - path_similarity_min) * precision / 100)
        # print("scale: ", scale)
        user_word_list = self.user_word_list(person)
        user_word_name_list = [word[0] for word in user_word_list]
        edges = []
        for item in word_similarity_list:
            if item[2] >= scale:
                edges.append([user_word_name_list.index(item[0]), user_word_name_list.index(item[1])])
        return edges

    def set_precision_min_max(self, person):
        similarity_list = sorted([value[2] for value in self.words_path_similarity_list(person)])
        return similarity_list[0], similarity_list[-1]

    def words_path_similarity_list(self, person):
        words = [item[0] for item in self.user_topic_dict[person]]
        test_input = []
        for i in range(len(words)):
            for j in range(len(words)):
                if i < j:
                    word_meaning1 = wn.synsets(words[i], pos=wn.NOUN)[0]
                    word_meaning2 = wn.synsets(words[j], pos=wn.NOUN)[0]
                    test_input.append((words[i], words[j], round(word_meaning1.path_similarity(word_meaning2), 3)))
        return test_input

    def provided_data(self, text_input):
        test_input = []
        for person in set(self.user_topic_dict.keys()):
            topic_list = self.user_topic_dict.get(person)
            for topic in topic_list:
                word_meaning1 = wn.synsets(topic, pos=wn.NOUN)[0]
                word_meaning2 = wn.synsets(text_input, pos=wn.NOUN)[0]
                test_input.append((topic, person, round(word_meaning1.path_similarity(word_meaning2), 2)))
        return test_input

    def user_word_list(self, person):
        return self.user_topic_dict[person]
