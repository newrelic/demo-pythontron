import json
import os

from api.help import help_message
from api.index_handler import IndexHandler
from api.inventory_handler import InventoryHandler
from api.message_handler import MessageHandler
from lib.app_config import AppConfig
from lib.app_logging import AppLogging
from lib.behaviors.repository import Repository
from lib.http_utils import HttpUtils
from lib.tron_response import TronResponse
from lib.validate.configuration import Configuration
from repository.database_connection_info import DatabaseConnectionInfo
from repository.database_inventory_repository import \
    DatabaseInventoryRepository
from repository.file_inventory_repository import FileInventoryRepository
from repository.mysql_connector import MySqlConnector
from repository.setup_database_action import SetupDatabaseAction


def get_config_file_path(arguments):
    # look at environment variable first for lambda deployment. if doesn't exist, use argument -- for ec2 instance deployment.
    config_file_path = os.environ.get('config_file', '')
    print(f"value of config file: {config_file_path}")

    if config_file_path == '':
        config_file_path = arguments.config_file

    print(f"new value of config file: {config_file_path}")

    Configuration(config_file_path).validate_config()

    return config_file_path


def inventory_repository_selector(app_config):
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


def get_lambda_reponse(tron_response):
    return {
       'headers': tron_response.get_headers(),
       'statusCode': tron_response.get_status_code(),
       'body': tron_response.get_body()
    }

def lambda_handler(event, context):
    AppLogging.init('info')

    app_config = AppConfig(
        config_file=os.environ['config_file']
    )

    config = app_config.asdict()

    database_connection_info_func = lambda: DatabaseConnectionInfo(
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host'],
        port=config['database']['port'],
        database=config['database']['database']
    )

    database_connector = MySqlConnector(
        connection_info=database_connection_info_func()
    )

    database_inventory_repository = DatabaseInventoryRepository(
        database_connector=database_connector
    )

    file_inventory_repository = FileInventoryRepository()

    inventory_repositories = {
        'file': file_inventory_repository,
        'database': database_inventory_repository
    }
    inventory_repository = inventory_repositories[inventory_repository_selector(app_config)]

    http_utils = HttpUtils(
        func_get_headers=lambda: (event['headers'] or dict()).items()
    )

    behavior_repository = Repository(
        app_id=app_config.get_app_id()
    )
    
    AppLogging.init('info')
    
    if(inventory_repository_selector(app_config) == 'database'):
        setup_database = SetupDatabaseAction(database_connector, database_connection_info_func(), get_inventory_data())
        setup_database.execute()

    endpoint = (event['resource'] or "").lower()
    if endpoint == "/":
        index = IndexHandler(app_config, behavior_repository)
        resp =  index.index_message()
    elif endpoint == "/validatemessage":
        message = MessageHandler(app_config, http_utils, behavior_repository)
        resp =  message.validate()
    elif endpoint == "/help":
        resp = help_message()
    elif endpoint == "/inventory":
        inventory = InventoryHandler(app_config, inventory_repository, http_utils, behavior_repository)
        resp = inventory.get_inventory()
    elif endpoint == "/inventory/{id+}":
        inventory = InventoryHandler(app_config, inventory_repository, http_utils, behavior_repository)
        item_id = event['pathParameters']['id']
        resp = inventory.get_inventory_item(item_id)
    else:
        body = "Unsupported endpoint: " + endpoint
        resp = TronResponse(body, dict(), 404)

    return get_lambda_reponse(resp)
