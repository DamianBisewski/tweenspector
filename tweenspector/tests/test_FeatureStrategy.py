from TestUtils import add_parent_dir_to_sys_path

add_parent_dir_to_sys_path()  # Make sure Python sees files outside of test directory

import unittest
from unittest.mock import MagicMock
from tweenspector.FeatureStrategy import FeatureStrategy, UserWordConnection, RelatedPeopleConnection, AccountsInfo


class TestFeatureStrategy(unittest.TestCase):
    def test_can_create_FeatureStrategy(self):
        username = "TestUser"
        search_words = ""
        date_from = "04-10-2022"
        date_to = "03-11-2022"
        tweets_count = 100
        fs = FeatureStrategy(username, search_words, date_from, date_to, tweets_count)
        self.assertIsNotNone(fs)

    def test_base_class_generate_image_raises_error(self):
        mock_fs = MagicMock()
        with self.assertRaises(NotImplementedError):
            FeatureStrategy.generate_image(mock_fs)

    def test_UserWordConnection_generate_image(self):
        mock_gwc = MagicMock(return_value=True)
        mock_uwc = MagicMock(return_value=None)
        mock_uwc.program_feature.generate_word_cloud = mock_gwc
        self.assertTrue(UserWordConnection.generate_image(mock_uwc))
        mock_gwc.assert_called_once_with()

    def test_RelatedPeopleConnection_generate_image(self):
        mock_gin = MagicMock(return_value=True)
        mock_o = MagicMock(return_value=None)
        mock_rpc = MagicMock(return_value=None)
        mock_rpc.program_feature.generate_interconnections_network = mock_gin
        mock_rpc.option = mock_o
        self.assertTrue(RelatedPeopleConnection.generate_image(mock_rpc))
        mock_gin.assert_called_once_with(mock_o)

    def test_AccountsInfo_generate_image(self):
        mock_gus = MagicMock(return_value=True)
        mock_o = MagicMock(return_value=None)
        mock_ai = MagicMock(return_value=None)
        mock_ai.program_feature.generate_user_stats = mock_gus
        mock_ai.option = mock_o
        self.assertTrue(AccountsInfo.generate_image(mock_ai))
        mock_gus.assert_called_once_with(mock_o)
