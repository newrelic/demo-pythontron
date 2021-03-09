import json

from dependency_injector import containers, providers
from flask.globals import request

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
from repository.mysql_connection import MySqlConnection


def inventory_repository_selector():
    container = Container()
    app_config = container.app_config()

    database_options = app_config.get_app_config_value('database')
    option_values = [database_options.get(i, None) for i in [
        'username', 'password', 'host', 'port', 'database']]

    # false if there exists an option with no value, true if all options have values
    use_database = not(None in option_values)

    selection = "database" if use_database else "file"

    print(f"Using inventory repository type: {selection}")

    return selection


def get_inventory_data():
    with open('data/inventory.json') as f:
        return json.load(f)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    arguments = providers.Object(
        CliParser.parse_args()
    )

    inventory_data = providers.Object(
        get_inventory_data()
    )

    config_file = arguments().config_file
    Configuration(config_file).validate_config()

    app_config = providers.Singleton(
        AppConfig,
        config_file=config_file)

    database_connection_info = providers.Factory(
        DatabaseConnectionInfo,
        user=config.database.user,
        password=config.database.password,
        host=config.database.host,
        port=config.database.port,
        database=config.database.database
    )

    database_connection = providers.Factory(
        MySqlConnection,
        connection_info=database_connection_info
    )

    database_inventory_repository = providers.Singleton(
        DatabaseInventoryRepository,
        database_connection=database_connection
    )

    file_inventory_repository = providers.Singleton(
        FileInventoryRepository
    )

    inventory_repository = providers.Selector(
        inventory_repository_selector,
        file=file_inventory_repository,
        database=database_inventory_repository
    )

    http_utils = providers.Singleton(
        HttpUtils,
        func_get_headers=lambda: request.headers or dict()
    )

    behavior_repository = providers.Singleton(
        Repository,
        app_id=app_config.provided.get_app_id.call()
    )
    
    inventory_handler = providers.Singleton(
        InventoryHandler,
        app_config=app_config,
        datastore=inventory_repository,
        https_utils=http_utils,
        behavior_repository=behavior_repository
    )
    
    message_handler = providers.Singleton(
        MessageHandler,
        app_config=app_config,
        http_utils=http_utils,
        behavior_repository=behavior_repository
    )
    
    behaviors_handler = providers.Singleton(
        BehaviorsHandler,
        app_config=app_config,
        behavior_repository=behavior_repository
    )
    
    index_handler = providers.Singleton(
        IndexHandler,
        app_config=app_config,
        behavior_repository=behavior_repository
    )
