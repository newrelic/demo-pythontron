import unittest

from mock import MagicMock

Container = None


class DependencyInjectionContainerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Container
        
        import repository.helpers
        import lib.cli_parser
        import lib.validate.configuration

        lib.validate.configuration.Configuration = MagicMock()
        lib.cli_parser.CliParser = MagicMock()
        repository.helpers.inventory_repository_selector = lambda: 'database'

        from dependency_injection_container import Container
    
    def setUp(self):
        self.app_config = MagicMock()
        self.app_config.get_app_id = lambda: "fake_app_id"
        self.container = Container()
        self.container.app_config.override(self.app_config)

    def test_container_resolves_index_handler(self):
        index_handler = self.container.index_handler()
        assert index_handler != None

    def test_container_resolves_behaviors_handler(self):
        behaviors_handler = self.container.behaviors_handler()
        assert behaviors_handler != None

    def test_container_resolves_message_handler(self):
        message_handler = self.container.message_handler()
        assert message_handler != None

    def test_container_resolves_inventory_handler(self):
        inventory_handler = self.container.inventory_handler()
        assert inventory_handler != None

if __name__ == '__main__':
    unittest.main()
