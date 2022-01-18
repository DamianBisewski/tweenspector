from TweetsData import TweetsData


def wordcloud_test1():
    td = TweetsData('wordcloud_test1', '', '', '', 100)
    td.test_mode_enable()
    td.generate_word_cloud()
    if td.wordcloud_test1_check():
        print("wordcloud_test1 - PASSED")
    else:
        print("wordcloud_test1 - FAILED")
    td.test_mode_disable()


def interconnection_network_test1():
    td = TweetsData('interconnection_network_test1.csv', '', '', '', 100)
    td.test_mode_enable()
    td.generate_interconnections_network()
    td.test_mode_disable()


def account_info_test1():
    td = TweetsData('szczepimysie', '', '', '', 100)
    td.test_mode_enable()
    td.generate_user_stats()
    if td.account_info_test1_check():
        print("account info test1 - PASSED")
    else:
        print("account info test1 - FAILED")
    td.test_mode_disable()


# wordcloud_test1()
# interconnection_network_test1()
account_info_test1()
