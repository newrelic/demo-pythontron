import os
import sys

from flask import Flask, Response, request

from api.behaviors_handler import BehaviorsHandler
from api.help import help_message
from api.index_handler import IndexHandler
from api.inventory_handler import InventoryHandler
from api.message_handler import MessageHandler
from dependency_injection_container import Container
from lib.app_logging import AppLogging
from lib.behaviors import repository
from lib.http_utils import HttpUtils
from repository import setup_database

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_exception(e):
    message = "{}".format(e)
    AppLogging.error(message)
    return message, 500


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
    response = Response(tron_response.get_body(
    ), status=tron_response.get_status_code(), mimetype='application/json')
    for k, v in tron_response.get_headers().items():
        response.headers[k] = v
    return response


if __name__ == "__main__":
    container = Container()
    app_config = container.app_config()

    print(app_config.asdict())
    container.config.from_dict(app_config.asdict())
    container.wire(modules=[setup_database, sys.modules[__name__]])

    arguments = container.arguments()

    # arguments = CliParser.parse_args()
    # Configuration(arguments.config_file).validate_config()
    # app_config = AppConfig(arguments.config_file)

    def func_get_headers(): return (request.headers or dict())
    http_utils = HttpUtils(func_get_headers)

    AppLogging.init(arguments.logging_level)

    behavior_repository = repository.Repository(app_id=app_config.get_app_id())

    #datastore = DataStore()
    datastore = container.inventory_repository()

    inventory = InventoryHandler(
        app_config, datastore, http_utils, behavior_repository)
    message = MessageHandler(app_config, http_utils, behavior_repository)
    behaviors = BehaviorsHandler(app_config, behavior_repository)
    index = IndexHandler(app_config, behavior_repository)

    debug_mode = arguments.debug_mode

    if debug_mode is not None and debug_mode == 'On':
        os.environ["FLASK_ENV"] = "development"

    port = int(app_config.get_app_port())
    AppLogging.info("Listening on port: " + str(port))
    AppLogging.info(index.get_message())

    if app_config.get_app_config_value('database').get('database', None) != None:
        # only setup database if value exists
        setup_database.execute()

    app.run(use_debugger=True, use_reloader=False,
            threaded=True, host='0.0.0.0', port=port)
