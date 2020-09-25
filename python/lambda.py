from api.index_handler import IndexHandler
from api.help import help_message
from api.message_handler import MessageHandler
from lib.datastore import DataStore
from api.inventory_handler import InventoryHandler
from lib.app_config import AppConfig
from lib.validate.configuration import Configuration
from lib.http_utils import HttpUtils
from lib.tron_response import TronResponse
from lib.app_logging import AppLogging
from lib.behaviors import repository

import os

def get_lambda_reponse(tron_response):
    return {
       'headers': tron_response.get_headers(),
       'statusCode': tron_response.get_status_code(),
       'body': tron_response.get_body()
    }

def lambda_handler(event, context):
    AppLogging.init('info')
    config_file = os.environ['config_file']
    Configuration(config_file).validate_config()
    app_config = AppConfig(config_file)

    func_get_headers = lambda: (event['headers'] or dict()).items()
    http_utils = HttpUtils(func_get_headers)
    behavior_repository = repository.Repository(app_id=app_config.get_app_id())

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
        inventory = InventoryHandler(app_config, DataStore(), http_utils, behavior_repository)
        resp = inventory.get_inventory()
    elif endpoint == "/inventory/{id+}":
        inventory = InventoryHandler(app_config, DataStore(), http_utils, behavior_repository)
        item_id = event['pathParameters']['id']
        resp = inventory.get_inventory_item(item_id)
    else:
        body = "Unsupported endpoint: " + endpoint
        resp = TronResponse(body, dict(), 404)

    return get_lambda_reponse(resp)
