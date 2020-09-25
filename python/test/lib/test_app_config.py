import unittest
import json

from mock import mock, mock_open, patch
from lib.app_config import AppConfig

class AppConfigTests(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('lib.validate.configuration.Configuration.validate_json')
        self.mock_object = self.patcher.start()
        self.mock_object.return_value = None

        self.arguments = mock.Mock()
        self.arguments.config_file = "filename"
        
        self.http_utils = mock.Mock()
        self.http_utils.get_request.text.return_value = ""

    def tearDown(self):
        pass

    @patch('builtins.open', mock.mock_open(read_data='{"id":"app1"}'))
    @mock.patch('requests.get', )
    def test_get_app_id(self, request_mock):
        app_config = AppConfig(self.arguments)
        result = app_config.get_app_id()
        self.assertEqual(result, 'app1')

    @patch('builtins.open', mock.mock_open(read_data='{"port":5000}'))
    def test_get_app_port(self):
        app_config = AppConfig(self.arguments)
        result = app_config.get_app_port()
        self.assertEqual(result, 5000)

    @patch('builtins.open', mock.mock_open(read_data='{}'))
    def test_get_app_port_no_value(self):
        app_config = AppConfig(self.arguments)
        with self.assertRaises(Exception):
            app_config.get_app_port()

    @patch('builtins.open', mock.mock_open(read_data='{"dependencies":[{"id":"app2","urls":["http://52.53.221.242:5001"]}]}'))
    def test_get_dependency(self):
        app_config = AppConfig(self.arguments)
        result = app_config.get_dependency_endpoint('app2')
        assert (len(result) > 0)

if __name__ == '__main__':
    unittest.main()            