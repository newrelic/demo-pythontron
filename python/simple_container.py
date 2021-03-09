import json
import os

from api.behaviors_handler import BehaviorsHandler
from api.index_handler import IndexHandler
from api.inventory_handler import InventoryHandler
from api.message_handler import MessageHandler
from lib.app_config import AppConfig
from lib.behaviors.repository import Repository
from lib.cli_parser import CliParser
from lib.http_utils import HttpUtils
from lib.validate.configuration import Configuration
from repository.database_connection_info import DatabaseConnectionInfo
from repository.database_inventory_repository import \
    DatabaseInventoryRepository
from repository.file_inventory_repository import FileInventoryRepository
from repository.mysql_connector import MySqlConnector


def get_flask_headers():
    from flask.globals import request
    return request.headers

def get_config_file_path():
    container = SimpleContainer()
    
    # look at environment variable first for lambda deployment. if doesn't exist, use argument -- for ec2 instance deployment.
    config_file_path = os.environ.get('config_file', '')
    print(f"value of config file: {config_file_path}")
    
    if config_file_path == '':
        config_file_path = container.arguments()['config_file']
    
    print(f"new value of config file: {config_file_path}")
    
    Configuration(config_file_path).validate_config()
    
    return config_file_path


def inventory_repository_selector():
    container = SimpleContainer()
    app_config = container.app_config()

    database_options = app_config.get_app_config_value('database')
    option_values = [database_options.get(i, '') for i in [
        'user', 'password', 'host', 'port', 'database']]

    # false if there exists an option with no value, true if all options have values
    use_database = not('' in option_values)

    selection = "database" if use_database else "file"

    print(f"Using inventory repository type: {selection}")

    return selection


def get_inventory_data():
    with open('data/inventory.json') as f:
        return json.load(f)


class SimpleContainer():
    arguments = CliParser.parse_args()

    inventory_data = get_inventory_data()

    config_file_path = get_config_file_path()

    app_config = AppConfig(
        config_file=config_file_path
    )

    config = app_config.asdict()

    database_connection_info = DatabaseConnectionInfo(
        user = config['user'],
        password = config['password'],
        host = config['host'],
        port = config['port'],
        database = config['database']
    )

    database_connector = MySqlConnector(
        connection_info=database_connection_info
    )

    database_inventory_repository = DatabaseInventoryRepository(
        database_connector=database_connector
    )

    file_inventory_repository = FileInventoryRepository()

    inventory_repositories = {
        'file': file_inventory_repository,
        'database': database_inventory_repository
    }
    inventory_repository = inventory_repositories[inventory_repository_selector()]

    http_utils = HttpUtils(
        func_get_headers=lambda: get_flask_headers() or dict()
    )

    behavior_repository = Repository(
        app_id=app_config.get_app_id()
    )

    inventory_handler = InventoryHandler(
        app_config=app_config, 
        datastore=inventory_repository, 
        http_utils=http_utils, 
        behavior_repository=behavior_repository
    )

    message_handler = MessageHandler(
        app_config=app_config,
        http_utils=http_utils,
        behavior_repository=behavior_repository
    )

    behaviors_handler = BehaviorsHandler(
        app_config=app_config,
        behavior_repository=behavior_repository
    )

    index_handler = IndexHandler(
        app_config=app_config,
        behavior_repository=behavior_repository
    )
