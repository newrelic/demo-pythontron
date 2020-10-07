import unittest
import json
import time

from mock import mock, patch
from unittest.mock import MagicMock
from api.message_handler import MessageHandler
from lib.app_logging import AppLogging
from lib.behaviors import repository

class MessageTests(unittest.TestCase):

    def setUp(self):
        AppLogging.init('info')
        self.http_utils = mock.Mock()
        self.http_utils.get_demo_http_headers.return_value = {}
        self.app_config = mock.Mock()
        self.app_config.get_delay_start_ms.return_value = 0
        self.app_config.get_process_start_time.return_value = time.time()
        self.result = mock.Mock()
        self.createResponseFunc = (lambda x,y,z: self.result)
        self.message = MessageHandler(self.app_config, self.http_utils, repository.Repository(["SOMETHING"]), self.createResponseFunc)

    def test_validate_message(self):
        self.app_config.get_dependency_endpoint.return_value = None
        data = '{"result": true}'
        self.result.get_body = MagicMock(return_value=data)
        
        result = self.message.validate()
        self.assertEqual(data, result.get_body())

if __name__ == '__main__':
    unittest.main()