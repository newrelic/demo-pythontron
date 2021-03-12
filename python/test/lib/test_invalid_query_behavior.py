import unittest

from mock import MagicMock, patch

from lib.behaviors.invalid_query import InvalidQuery


class InvalidQueryTests(unittest.TestCase):
    def setUp(self):
        self.database_inventory_repository = MagicMock()
        self.invalid_query_behavior = InvalidQuery(self.database_inventory_repository)
    
    @patch('lib.app_logging.AppLogging')
    def test_execute_calls_database_repository(self, _):
        self.invalid_query_behavior.execute()
        self.database_inventory_repository.run_invalid_query.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
