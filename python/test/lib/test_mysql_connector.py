import unittest
from unittest.mock import patch

from repository.database_connection_info import DatabaseConnectionInfo
from repository.mysql_connector import MySqlConnector


class MySqlConnectorTests(unittest.TestCase):

    def setUp(self):
        self.connection_info = DatabaseConnectionInfo('fake_username', 'fake_password', 'fake_host', 'fake_port', 'fake_database')
        self.mysql_connector = MySqlConnector(self.connection_info)

    @patch('repository.mysql_connector.mysql.connector')
    def test_connect_uses_options(self, mock_connector):
        options = {
            'option1': 'fake_value_1',
            'option2': 'fake_value_2'
        }
        self.mysql_connector.connect(**options)
        mock_connector.connect.assert_called_once_with(**options)
    
    @patch('repository.mysql_connector.mysql.connector')
    def test_connect_uses_default(self, mock_connector):
        self.mysql_connector.connect()
        mock_connector.connect.assert_called_once_with(**self.connection_info.asdict())

if __name__ == '__main__':
    unittest.main()
