import os
import sys

from flask import Flask, Response

from api.help import help_message
from dependency_injection_container import Container, inventory_repository_selector
from lib.app_logging import AppLogging
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

    container.config.from_dict(app_config.asdict())
    container.wire(modules=[setup_database, sys.modules[__name__]])

    arguments = container.arguments()

    AppLogging.init(arguments.logging_level)

    http_utils = container.http_utils()
    inventory = container.inventory_handler()
    message = container.message_handler()
    behaviors = container.behaviors_handler()
    index = container.index_handler()

    debug_mode = arguments.debug_mode

    if debug_mode is not None and debug_mode == 'On':
        os.environ["FLASK_ENV"] = "development"

    port = int(app_config.get_app_port())
    AppLogging.info("Listening on port: " + str(port))
    AppLogging.info(index.get_message())

    if inventory_repository_selector() == 'database':
        setup_database.execute()

    app.run(use_debugger=True, use_reloader=False,
            threaded=True, host='0.0.0.0', port=port)
