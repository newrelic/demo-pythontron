import unittest

from repository.file_inventory_repository import FileInventoryRepository


class FileInventoryRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.file_inventory_repository = FileInventoryRepository()

    def tearDown(self):
        pass

    def test_get_all_data(self):
        result_array = self.file_inventory_repository.get_records()
        self.assertEqual(len(result_array), 10)
    
    def test_get_single_dependency_value(self):
        result = self.file_inventory_repository.get_record_by_id("1")
        self.assertIn('Item_1', result['item'])

    def test_incorrect_item_id(self):
        result_array = self.file_inventory_repository.get_record_by_id("invalid_id")
        self.assertEqual(len(result_array), 0)

if __name__ == '__main__':
    unittest.main()
