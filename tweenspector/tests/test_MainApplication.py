from TestUtils import add_parent_dir_to_sys_path

add_parent_dir_to_sys_path()  # Make sure Python sees files outside of test directory

import unittest
from unittest.mock import MagicMock, patch
import tweenspector.MainApplication as MApp
from tweenspector.MainApplication import MainApplication


class TestMainApplication(unittest.TestCase):
    @patch("tweenspector.MainApplication.print")
    def test_can_remove_widgets_from_list(self, mock_print):
        arg = [MagicMock(), MagicMock(), MagicMock()]
        MApp.remove_widgets(arg)
        for el in arg:
            el.destroy.assert_called_once_with()

    @patch("tweenspector.MainApplication.print")
    def test_can_remove_widgets_from_object(self, mock_print):
        arg = MagicMock()
        MApp.remove_widgets(arg)
        arg.destroy.assert_called_once_with()

    @patch("tweenspector.MainApplication.print")
    def test_remove_widgets_raises_no_exceptions_on_none(self, mock_print):
        MApp.remove_widgets(None)

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.ttk")
    @patch("tweenspector.MainApplication.DateEntry")
    @patch("tweenspector.MainApplication.Image")
    @patch("tweenspector.MainApplication.ImageTk")
    def test_can_create_MainApplication(self, mock_ImageTk, mock_Image, mock_DateEntry, mock_ttk, mock_tk, mock_print):
        mock_root = MagicMock()
        app = MainApplication(mock_root)
        self.assertIsNotNone(app)

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    def test_can_set_combobox_description(self, mock_tk, mock_print):
        test_features = {"Nie wybrano": "UWAGA: wybierz funkcjonalność",
                         "Najczęstsze słowa": "Zbiór najczęściej używanych słów dla danego użytkownika" + '\n' + "Twittera",
                         "Powiązane konta": "Graf powiązanych kont z danym użytkownikiem Twittera",
                         "Statystyki użytkownika": ""}

        for feature in test_features:
            with self.subTest(feature=feature):
                app = MagicMock()
                event = MagicMock()

                app.nav_cb[0].get = MagicMock(return_value=feature)

                MainApplication.set_combobox_description(app, event)

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    def test_can_propagate_params(self, mock_tk, mock_print):
        test_data = [("01.01.2022", "31.12.2022", "TestUser"),
                     ("13.07.2022", "14.07.2022", "TestUser"),
                     ("05.08.2022", "01.10.2022", "TestUser"),
                     ("25.11.2021", "04.03.2022", "TestUser"),
                     ("01.02.2018", "04.03.2020", "TestUser")]

        for date_from, date_to, username in test_data:
            with self.subTest(date_from=date_from, date_to=date_to, username=username):
                app = MagicMock()
                app.nav_e[0].get = MagicMock(return_value=username)

                dfg = MagicMock()
                dfg.get = MagicMock(return_value=date_from)
                dtg = MagicMock()
                dtg.get = MagicMock(return_value=date_to)
                app.date_e = [dfg, dtg]

                self.assertTrue(MainApplication.propagate_params(app))

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    def test_propagate_params_shows_error_when_username_is_none(self, mock_tk, mock_print):
        test_dates = [("13.07.2022", "14.07.2022", None),
                      ("13.07.2022", "14.07.2022", ""),
                      ("01.02.2018", "04.03.2020", None),
                      ("01.02.2018", "04.03.2020", "")]

        for date_from, date_to, username in test_dates:
            with self.subTest(date_from=date_from, date_to=date_to, username=username):
                app = MagicMock()
                app.nav_e[0].get = MagicMock(return_value=username)

                dfg = MagicMock()
                dfg.get = MagicMock(return_value=date_from)
                dtg = MagicMock()
                dtg.get = MagicMock(return_value=date_to)
                app.date_e = [dfg, dtg]

                self.assertFalse(MainApplication.propagate_params(app))

                mock_tk.messagebox.showerror.assert_called_once()
                mock_tk.messagebox.showerror.reset_mock()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    def test_propagate_params_shows_error_when_dates_are_mismatched(self, mock_tk, mock_print):
        test_dates = [("02.11.2022", "05.10.2022", "TestUsername"),
                      ("29.11.2022", "28.11.2022", "TestUsername"),
                      ("19.06.2022", "05.10.2021", "TestUsername"),
                      ("09.08.2020", "03.10.2018", "TestUsername")]

        for date_from, date_to, username in test_dates:
            with self.subTest(date_from=date_from, date_to=date_to, username=username):
                app = MagicMock()
                app.nav_e[0].get = MagicMock(return_value=username)

                dfg = MagicMock()
                dfg.get = MagicMock(return_value=date_from)
                dtg = MagicMock()
                dtg.get = MagicMock(return_value=date_to)
                app.date_e = [dfg, dtg]

                self.assertFalse(MainApplication.propagate_params(app))

                mock_tk.messagebox.showerror.assert_called_once()
                mock_tk.messagebox.showerror.reset_mock()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    def test_propagate_params_sets_search_words_to_none_if_empty(self, mock_tk, mock_print):
        test_data = [("13.07.2022", "14.07.2022", "TestUser"),
                     ("05.08.2022", "01.10.2022", "TestUser"),
                     ("01.02.2018", "04.03.2020", "TestUser")]

        for date_from, date_to, username in test_data:
            with self.subTest(date_from=date_from, date_to=date_to, username=username):
                app = MagicMock()

                ug = MagicMock()
                ug.get = MagicMock(return_value=username)
                swg = MagicMock()
                swg.get = MagicMock(return_value="")
                app.nav_e = [ug, swg]

                dfg = MagicMock()
                dfg.get = MagicMock(return_value=date_from)
                dtg = MagicMock()
                dtg.get = MagicMock(return_value=date_to)
                app.date_e = [dfg, dtg]

                self.assertTrue(MainApplication.propagate_params(app))
                self.assertIsNone(app.search_words)

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.plt")
    @patch("tweenspector.MainApplication.matplotlib")
    @patch("tweenspector.MainApplication.img")
    def test_can_search_result(self, mock_img, mock_matplotlib, mock_plt, mock_tk, mock_print):
        test_data = {"Najczęstsze słowa", "Powiązane konta", "Statystyki użytkownika"}

        for feature in test_data:
            with self.subTest(feature=feature):
                app = MagicMock()

                app.propagate_params = MagicMock(return_value=True)
                app.configure_feature_strategy = MagicMock()
                app.feature_strategy.generate_image = MagicMock(return_value=True)

                MainApplication.search_result(app, feature)

                app.propagate_params.assert_called_once_with()
                app.configure_feature_strategy.assert_called_once()
                app.feature_strategy.generate_image.assert_called_once_with()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.plt")
    @patch("tweenspector.MainApplication.matplotlib")
    @patch("tweenspector.MainApplication.img")
    def test_search_result_returns_if_cannot_propagate_params(self, mock_img, mock_matplotlib,
                                                              mock_plt, mock_tk, mock_print):
        test_data = {"Najczęstsze słowa", "Powiązane konta", "Statystyki użytkownika"}

        for feature in test_data:
            with self.subTest(feature=feature):
                app = MagicMock()

                app.propagate_params = MagicMock(return_value=False)
                app.configure_feature_strategy = MagicMock()
                app.feature_strategy.generate_image = MagicMock(return_value=True)

                MainApplication.search_result(app, feature)

                app.propagate_params.assert_called_once_with()
                app.configure_feature_strategy.assert_not_called()
                app.feature_strategy.generate_image.assert_not_called()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.plt")
    @patch("tweenspector.MainApplication.matplotlib")
    @patch("tweenspector.MainApplication.img")
    def test_search_result_shows_error_if_no_feature_selected(self, mock_img, mock_matplotlib,
                                                              mock_plt, mock_tk, mock_print):
        feature = "Nie wybrano"

        app = MagicMock()

        app.propagate_params = MagicMock(return_value=True)
        app.configure_feature_strategy = MagicMock()
        app.feature_strategy.generate_image = MagicMock(return_value=True)

        MainApplication.search_result(app, feature)

        app.propagate_params.assert_called_once_with()
        mock_tk.messagebox.showerror.assert_called_once()
        app.configure_feature_strategy.assert_not_called()
        app.feature_strategy.generate_image.assert_not_called()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.plt")
    @patch("tweenspector.MainApplication.matplotlib")
    @patch("tweenspector.MainApplication.img")
    def test_search_result_shows_error_if_cannot_generate_image(self, mock_img, mock_matplotlib,
                                                                mock_plt, mock_tk, mock_print):
        test_data = {"Najczęstsze słowa", "Powiązane konta", "Statystyki użytkownika"}

        for feature in test_data:
            with self.subTest(feature=feature):
                app = MagicMock()

                app.propagate_params = MagicMock(return_value=True)
                app.configure_feature_strategy = MagicMock()
                app.feature_strategy.generate_image = MagicMock(return_value=False)

                MainApplication.search_result(app, feature)

                app.propagate_params.assert_called_once_with()
                app.configure_feature_strategy.assert_called_once()
                app.feature_strategy.generate_image.assert_called_once_with()
                mock_tk.messagebox.showerror.assert_called_once()
                mock_tk.messagebox.showerror.reset_mock()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.AccountsInfo")
    @patch("tweenspector.MainApplication.RelatedPeopleConnection")
    @patch("tweenspector.MainApplication.UserWordConnection")
    def test_can_configure_feature_strategy(self, mock_UserWordConnection, mock_RelatedPeopleConnection,
                                            mock_AccountsInfo, mock_tk, mock_print):
        test_data = {("Najczęstsze słowa", mock_UserWordConnection),
                     ("Powiązane konta", mock_RelatedPeopleConnection),
                     ("Statystyki użytkownika", mock_AccountsInfo)}
        username = "TestUser"
        search_words = ""
        date_from = "05.08.2022"
        date_to = "01.10.2022"
        tweets_count = 100
        stats_option = 0
        community_detection_method = []

        for feature, featureConstructorMock in test_data:
            with self.subTest(feature=feature):
                app = MagicMock()

                self.assertTrue(
                    MainApplication.configure_feature_strategy(app, feature, username, search_words, date_from, date_to,
                                                               tweets_count, stats_option, community_detection_method))

                featureConstructorMock.assert_called_once()
                featureConstructorMock.reset_mock()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.save_tweets_df_to_csv")
    @patch("tweenspector.MainApplication.asksaveasfile")
    @patch("tweenspector.MainApplication.TweetsData")
    def test_can_save_csv(self, mock_TweetsData, mock_asksaveasfile,
                          mock_save_tweets_df_to_csv, mock_tk, mock_print):
        app = MagicMock()
        mock_file = MagicMock()
        td = MagicMock()
        mock_tweets = MagicMock()

        app.propagate_params.return_value = True
        mock_asksaveasfile.return_value = mock_file
        mock_TweetsData.return_value = td
        td.get_tweets = MagicMock(return_value=mock_tweets)

        MainApplication.save_csv(app)

        app.propagate_params.assert_called_once_with()
        mock_TweetsData.assert_called_once()
        td.get_tweets.assert_called_once()
        mock_asksaveasfile.assert_called_once()
        mock_save_tweets_df_to_csv.assert_called_once_with(mock_file.name, mock_tweets)

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.save_tweets_df_to_csv")
    @patch("tweenspector.MainApplication.asksaveasfile")
    @patch("tweenspector.MainApplication.TweetsData")
    def test_save_csv_returns_when_cannot_propagate_params(self, mock_TweetsData, mock_asksaveasfile,
                                                           mock_save_tweets_df_to_csv, mock_tk, mock_print):
        app = MagicMock()

        app.propagate_params.return_value = False

        MainApplication.save_csv(app)

        app.propagate_params.assert_called_once_with()
        mock_TweetsData.assert_not_called()
        mock_asksaveasfile.assert_not_called()
        mock_save_tweets_df_to_csv.assert_not_called()

    @patch("tweenspector.MainApplication.print")
    @patch("tweenspector.MainApplication.tk")
    @patch("tweenspector.MainApplication.save_tweets_df_to_csv")
    @patch("tweenspector.MainApplication.asksaveasfile")
    @patch("tweenspector.MainApplication.TweetsData")
    def test_save_csv_does_not_save_when_cannot_obtain_file_handle(self, mock_TweetsData, mock_asksaveasfile,
                                                                   mock_save_tweets_df_to_csv, mock_tk, mock_print):
        app = MagicMock()
        td = MagicMock()
        mock_tweets = MagicMock()

        app.propagate_params.return_value = True
        mock_asksaveasfile.return_value = None
        mock_TweetsData.return_value = td
        td.get_tweets = MagicMock(return_value=mock_tweets)

        MainApplication.save_csv(app)

        app.propagate_params.assert_called_once_with()
        mock_TweetsData.assert_called_once()
        td.get_tweets.assert_called_once()
        mock_asksaveasfile.assert_called_once()
        mock_save_tweets_df_to_csv.assert_not_called()
