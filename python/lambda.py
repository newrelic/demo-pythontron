from api.help import help_message
from lib.app_logging import AppLogging
from lib.tron_response import TronResponse
from simple_container import SimpleContainer


def get_lambda_reponse(tron_response):
    return {
       'headers': tron_response.get_headers(),
       'statusCode': tron_response.get_status_code(),
       'body': tron_response.get_body()
    }

def lambda_handler(event, context):
    AppLogging.init('info')
    
    container = SimpleContainer()

    endpoint = (event['resource'] or "").lower()
    if endpoint == "/":
        index = container.index_handler
        resp =  index.index_message()
    elif endpoint == "/validatemessage":
        message = container.message_handler
        resp =  message.validate()
    elif endpoint == "/help":
        resp = help_message()
    elif endpoint == "/inventory":
        inventory = container.inventory_handler
        resp = inventory.get_inventory()
    elif endpoint == "/inventory/{id+}":
        inventory = container.inventory_handler
        item_id = event['pathParameters']['id']
        resp = inventory.get_inventory_item(item_id)
    else:
        body = "Unsupported endpoint: " + endpoint
        resp = TronResponse(body, dict(), 404)

    return get_lambda_reponse(resp)
