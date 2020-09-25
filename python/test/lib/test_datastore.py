import unittest
import json

from mock import mock, patch
from lib.datastore import DataStore
from flask import Flask

class DataStoreTests(unittest.TestCase):

    def setUp(self):
        self.datastore = DataStore()

    def tearDown(self):
        pass

    def test_get_all_data(self):
        result_array = self.datastore.get_records()
        self.assertEqual(len(result_array), 10)
    
    def test_get_single_dependency_value(self):
        result = self.datastore.get_record_by_id("1")
        self.assertIn('Item_1', result['item'])

    def test_incorrect_item_id(self):
        result_array = self.datastore.get_record_by_id("invalid_id")
        self.assertEqual(len(result_array), 0)

if __name__ == '__main__':
    unittest.main()