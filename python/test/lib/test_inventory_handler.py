import unittest
import json

from mock import mock, patch
from unittest.mock import MagicMock
from api.inventory_handler import InventoryHandler
from lib.datastore import DataStore
from flask import request
from lib.app_logging import AppLogging
from lib.behaviors import repository, behavior

class InventoryTests(unittest.TestCase):

    def setUp(self):
        AppLogging.init('info')
        self.http_utils = mock.Mock()
        self.http_utils.query_service.return_value = "{}"
        self.http_utils.get_demo_http_headers.return_value = {}
        self.app_config = mock.Mock()
        self.result = mock.Mock()
        self.createResponseFunc = (lambda x,y,z: self.result)
        self.datastore = mock.Mock()
        self.all_inventory = [0,1,2,3,4,5,6,7,8,9]
        self.datastore.get_records.return_value = self.all_inventory
        self.inventory = InventoryHandler(self.app_config, self.datastore, self.http_utils, repository.Repository(["SOMETHING"]), self.createResponseFunc)

    def test_get_all_inventory_data(self):
        self.app_config.get_dependency_endpoint.return_value = None
        self.result.get_body = MagicMock(return_value=self.all_inventory)
        result = self.inventory.get_inventory()
        self.assertEqual(len(result.get_body()), 10)

    def test_get_single_inventory_data(self):
        self.app_config.get_dependency_endpoint.return_value = None
        self.result.get_body = MagicMock(return_value={'item':'Item_1'})
        result = self.inventory.get_inventory_item("1")
        self.assertIn('Item_1', json.dumps(result.get_body()))

    def test_incorrect_item_id(self):
        self.app_config.get_dependency_endpoint.return_value = None
        self.result.get_body = MagicMock(return_value=[])
        result = self.inventory.get_inventory_item("invalid_id")
        self.assertEqual(result.get_body(), [])

if __name__ == '__main__':
    unittest.main()