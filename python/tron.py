import json
import sys
import os

from flask import Flask, request, jsonify, Blueprint, Response
from flask import g

from multiprocessing import Value

from lib.cli_parser import CliParser
from lib.app_config import AppConfig
from lib.datastore import DataStore
from lib.http_utils import HttpUtils
from lib.app_logging import AppLogging
from lib.validate.configuration import Configuration
from lib.behaviors import repository
from api.inventory_handler import InventoryHandler
from api.message_handler import MessageHandler
from api.help import help_message
from api.index_handler import IndexHandler
from api.behaviors_handler import BehaviorsHandler

app = Flask(__name__)

@app.route("/")
def index():
    return get_flask_response(index.index_message())

@app.route("/api")
def index_api():
    return get_flask_response(index.index_message())

@app.route("/api/help")
def help():
    return get_flask_response(help_message())

@app.route("/api/behaviors")
def behaviors():
    return get_flask_response(behaviors.list_behaviors())

@app.route("/api/validateMessage")
def validateMessage():
    return get_flask_response(message.validate())

@app.route("/api/inventory")
def inventory_list():
    return get_flask_response(inventory.get_inventory())

@app.route("/api/inventory/<string:item_id>")
def inventory_item(item_id):
    return get_flask_response(inventory.get_inventory_item(item_id))

@app.after_request
def add_headers(response):
    return http_utils.add_response_headers(response)

def get_flask_response(tron_response):
    response = Response(tron_response.get_body(), status=tron_response.get_status_code(), mimetype='application/json')
    for k,v in tron_response.get_headers().items():
        response.headers[k] = v
    return response

if __name__ == "__main__":
    arguments = CliParser.parse_args()
    Configuration(arguments.config_file).validate_config()
    app_config = AppConfig(arguments.config_file)

    func_get_headers = lambda: (request.headers or dict())
    http_utils = HttpUtils(func_get_headers)

    AppLogging.init(arguments.logging_level)

    behavior_repository = repository.Repository(app_id=app_config.get_app_id())

    datastore = DataStore()
    inventory = InventoryHandler(app_config, datastore, http_utils, behavior_repository)
    message = MessageHandler(app_config, http_utils, behavior_repository)
    behaviors = BehaviorsHandler(app_config, behavior_repository)
    index = IndexHandler(app_config, behavior_repository)

    debug_mode = arguments.debug_mode

    if debug_mode is not None and debug_mode == 'On':
        os.environ["FLASK_ENV"] = "development"

    port=int(app_config.get_app_port())
    AppLogging.info("Listening on port: " + str(port))
    AppLogging.info(index.get_message())

    app.run(use_debugger=True, use_reloader=False, threaded=True, host='0.0.0.0', port=port)

