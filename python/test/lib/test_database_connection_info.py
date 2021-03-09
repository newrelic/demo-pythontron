import unittest

from repository.database_connection_info import DatabaseConnectionInfo


class DatabaseConnectionInfoTests(unittest.TestCase):
    def setUp(self):
        self.connection_info = {
            'user': 'fake_user',
            'password': 'fake_password',
            'host': 'fake_host',
            'port': 'fake_port',
            'database': 'fake_database'
        }
        
    def get_database_connection_info(self):
        return DatabaseConnectionInfo(
            user=self.connection_info.get('user', None),
            password=self.connection_info.get('password', None),
            host=self.connection_info.get('host', None),
            port=self.connection_info.get('port', None),
            database=self.connection_info.get('database', None)
        )
    
    def test_asdict_returns_all_fields(self):
        expected = self.connection_info
        actual = self.get_database_connection_info().asdict()
        self.assertDictEqual(actual, expected)

    def test_asdict_only_returns_fields_with_values(self):
        del self.connection_info['user']
        del self.connection_info['database']
        expected = self.connection_info
        actual = self.get_database_connection_info().asdict()
        self.assertDictEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
