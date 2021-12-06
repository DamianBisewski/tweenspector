from App_variables import features
from ProgramFeature import ProgramFeature


class FeatureStrategy:
    def __init__(self, option):
        self.program_feature = ProgramFeature()

        if option == features[0]:
            self.feature = UserWordConnection(self)
        elif option == features[1]:
            self.feature = RelatedPeopleConnection(self)
        elif option == features[2]:
            self.feature = UserSimilarAccounts(self)

    def set_text_listbox_label(self):
        raise NotImplementedError('Please implement this method')

    def set_listbox(self):
        raise NotImplementedError('Please implement this method')

    def set_graph_item(self):
        raise NotImplementedError('Please implement this method')

    def get_graph_edges(self, person, precision):
        raise NotImplementedError('Please implement this method')

    def get_vertices_dictionary(self, person):
        raise NotImplementedError('Please implement this method')

    def get_graph_title(self):
        raise NotImplementedError('Please implement this method')

    def is_item_in_list(self, person):
        raise NotImplementedError('Please implement this method')


class UserWordConnection(FeatureStrategy):
    def set_text_listbox_label(self):
        return 'Lista osób'

    def set_listbox(self):
        return self.program_feature.user_topic_dict.keys()

    def set_graph_item(self):
        return 'Wybrana osoba'

    def get_graph_edges(self, person, precision):
        return self.program_feature.words_to_words(person, precision)

    def get_vertices_dictionary(self, person):
        return self.program_feature.get_topic_dictionary(person)

    def get_graph_title(self):
        return 'Sieć powiązań słów użytwkonika'

    def is_item_in_list(self, person):
        available_people_list = self.program_feature.user_topic_dict.keys()
        if person in available_people_list:
            return True
        return False


class RelatedPeopleConnection(FeatureStrategy):
    def set_text_listbox_label(self):
        return 'Lista tematów'

    def set_listbox(self):
        return self.program_feature.user_topic_dict.values()

    def set_graph_item(self):
        return 'Słowo kluczowe'


class UserSimilarAccounts(FeatureStrategy):
    def set_text_listbox_label(self):
        return 'Lista tematów'

    def set_listbox(self):
        return self.program_feature.user_topic_dict.values()

    def set_graph_item(self):
        return 'Słowo kluczowe'
