from nltk.corpus import wordnet as wn


class ProgramFeature:
    def __init__(self):
        self.user_topic_dict = {'KK': [('cat', 5), ('animal', 4), ('bird', 7), ('tree', 6), ('plant', 4),
                                       ('dog', 21), ('car', 12), ('tiger', 8)],
                                'JB': [('hamster', 2), ('mouse', 1), ('pigeon', 3), ('carrot', 3),
                                       ('popcorn', 3)],
                                'AA': [('movie', 10), ('cinema', 8), ('cheese', 4), ('milk', 2), ('food', 4),
                                       ('river', 6), ('lake', 2)]}

    def words_to_words(self, person, precision):
        d = self.get_topic_dictionary(person)
        word_similarity_list = self.words_path_similarity_list(person)
        edges = []
        precision_max = self.set_precision_max(person)
        print(word_similarity_list)
        print(precision_max)
        print(precision / 100)
        precision = precision / 100 * precision_max
        print(precision)
        for item in word_similarity_list:
            if item[2] >= precision:
                edges.append([d[item[0]], d[item[1]]])
        return edges

    def set_precision_max(self, person):
        similarity_list = [value[2] for value in self.words_path_similarity_list(person)]
        return sorted(similarity_list)[::-1][1]

    # returns [(word1, word2, words path similarity), ...]
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

    # returns dictionary {topic: vertex} for graph vertices
    def get_topic_dictionary(self, person):
        person_topics = [topic[0] for topic in self.user_topic_dict[person]]
        d = {}
        for i in range(len(self.user_topic_dict[person])):
            d[person_topics[i]] = i
        return d
