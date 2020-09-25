import unittest
import json

from mock import mock, patch
from lib.string_utils import StringUtils

class StringUtilsTests(unittest.TestCase):

    def test_truncate_last_word(self):
        string = "abc 123 ffgg"
        deliminter = " "
        max_string_length = 10
        expected = "abc 123"
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)

    def test_truncate_exactly_enough(self):
        string = "12345 789"
        deliminter = " "
        max_string_length = 5
        expected = "12345"
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)

    def test_truncate_exactly_enough_with_out_delimiter(self):
        string = "12345 789"
        deliminter = " "
        max_string_length = 6
        expected = "12345"
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)

    def test_truncate_except_when_shorter_than_max(self):
        string = "12345 789"
        deliminter = " "
        max_string_length = 7
        expected = "12345"
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)

    def test_truncate_on_any_string_delimiter(self):
        string = "abczz123zzffgg"
        deliminter = "zz"
        max_string_length = 10
        expected = "abczz123"
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)

    def test_truncate_to_empy_when_max_too_small(self):
        string = "abcdefgh abcdefgh"
        deliminter = " "
        max_string_length = 2
        expected = ""
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)

    def test_truncate_to_empy_when_max_too_small(self):
        string = "abcdefgh abcdefgh"
        deliminter = " "
        max_string_length = 2
        expected = ""
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)

    def test_truncate_to_frist_when_max_too_small_becuase_of_delimiter(self):
        string = "abZZZZcdZZZZef"
        deliminter = "ZZZZ"
        max_string_length = 5
        expected = "ab"
        result = StringUtils.truncateString(string, deliminter, max_string_length)
        self.assertEqual(result, expected)
