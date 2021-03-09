from dependency_injector import containers, providers
from flask.globals import request

from api.behaviors_handler import BehaviorsHandler
from api.index_handler import IndexHandler
from api.inventory_handler import InventoryHandler
from api.message_handler import MessageHandler
from data.inventory import get_inventory_data
from lib.app_config import AppConfig
from lib.behaviors.repository import Repository
from lib.cli_parser import CliParser
from lib.http_utils import HttpUtils
from lib.validate.configuration import Configuration
from repository.database_connection_info import DatabaseConnectionInfo
from repository.database_inventory_repository import \
    DatabaseInventoryRepository
from repository.file_inventory_repository import FileInventoryRepository
from repository.helpers import inventory_repository_selector
from repository.mysql_connector import MySqlConnector
from repository.setup_database_action import SetupDatabaseAction


class Container(containers.DeclarativeContainer):
    """
    A class whose responsibility is instantiating, and resolving dependencies.
    """
    
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
        config_file=config_file
    )

    database_connection_info = providers.Factory(
        DatabaseConnectionInfo,
        user=config.database.user,
        password=config.database.password,
        host=config.database.host,
        port=config.database.port,
        database=config.database.name
    )

    database_connector = providers.Factory(
        MySqlConnector,
        connection_info=database_connection_info
    )

    database_inventory_repository = providers.Singleton(
        DatabaseInventoryRepository,
        database_connector=database_connector
    )
    
    setup_database_action = providers.Factory(
        SetupDatabaseAction,
        database_connector=database_connector,
        database_connection_info=database_connection_info,
        inventory_data=inventory_data
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
        http_utils=http_utils,
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
