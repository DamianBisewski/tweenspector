from TestUtils import add_parent_dir_to_sys_path

add_parent_dir_to_sys_path()  # Make sure Python sees files outside of test directory

import unittest
from unittest.mock import MagicMock, patch
from tweenspector.MainApplication import MainApplication


class TestMainApplication(unittest.TestCase):
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
