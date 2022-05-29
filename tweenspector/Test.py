from TweetsData import TweetsData


def wordcloud_test1():
    td = TweetsData('wordcloud_test', '', '', '', 100)
    td.test_mode_enable()
    td.generate_word_cloud()
    if td.wordcloud_test1_check():
        print("wordcloud_test1 - PASSED")
    else:
        print("wordcloud_test1 - FAILED")
    td.test_mode_disable()


def interconnection_network_test1(option):
    td = TweetsData('szczepimysie', '', '', '', 100)
    td.test_mode_enable()
    td.generate_interconnections_network(option)
    if td.interconnection_network_test1_check():
        print("interconnection_network_test1 - PASSED")
    else:
        print("interconnection_network_test1 - FAILED")
    td.test_mode_disable()

def account_info_test1():
    td = TweetsData('donaldtusk', '', '', '', 100)
    td.test_mode_enable()
    td.generate_user_stats(1)
    if td.account_info_test1_check():
        print("account info test1 - PASSED")
    else:
        print("account info test1 - FAILED")
    td.test_mode_disable()

wordcloud_test1()
interconnection_network_test1("Label Propagation")
account_info_test1()
