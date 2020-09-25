import unittest
import json

from mock import mock, patch
from unittest.mock import MagicMock
from lib.http_utils import HttpUtils

class HttpUtilsTests(unittest.TestCase):

    def test_find_no_demo_http_headers(self):
        func_get_headers = lambda: ( {"Key": "Value"}.items() )

        self.http_util = HttpUtils(func_get_headers)
        headers = self.http_util.get_demo_http_headers()
        self.assertEqual(headers, {})

    def test_find_only_when_starts_with_x_demo_case_demo_http_headers(self):
        func_get_headers = lambda: ( {"NO-X-DEMO-TEST": "value"}.items() )

        self.http_util = HttpUtils(func_get_headers)
        headers = self.http_util.get_demo_http_headers()
        self.assertEqual(headers, {})

    def test_find_one_upper_case_demo_http_headers(self):
        func_get_headers = lambda: ( {"X-DEMO-TEST": "value"}.items() )

        self.http_util = HttpUtils(func_get_headers)
        headers = self.http_util.get_demo_http_headers()
        self.assertEqual(headers, {"X-DEMO-TEST": "value"})

    def test_find_one_lower_case_demo_http_headers(self):
        func_get_headers = lambda: ( {"x-demo-test": "value"}.items() )

        self.http_util = HttpUtils(func_get_headers)
        headers = self.http_util.get_demo_http_headers()
        self.assertEqual(headers, {"X-DEMO-TEST": "value"})

if __name__ == '__main__':
    unittest.main()