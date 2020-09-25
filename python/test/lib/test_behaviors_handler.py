import unittest
import json

from mock import mock, patch
from unittest.mock import MagicMock
from api.behaviors_handler import BehaviorsHandler
from lib.app_logging import AppLogging
from lib.behaviors import repository

class BehaviorAPITtests(unittest.TestCase):

    def setUp(self):
        AppLogging.init('info')
        self.app_config = mock.Mock()
        self.result = mock.Mock()
        self.behaviors = BehaviorsHandler(self.app_config, repository.Repository(["SOMETHING"]))

    def test_validate_message(self):
        self.app_config.get_dependency_endpoint.return_value = None
        repository.Repository.get_available_behaviors = mock.Mock()
        repository.Repository.get_available_behaviors.return_value = ["SOMETHING"]
        
        data = '["SOMETHING"]'
        self.result.get_body = MagicMock(return_value=data)

        result = self.behaviors.list_behaviors()
        self.assertEqual(data, result.get_body())

if __name__ == '__main__':
    unittest.main()