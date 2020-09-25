import json
from lib.tron_response import TronResponse
from lib.app_logging import AppLogging

def help_message():
    AppLogging.info("help")

    body = '''
        API Usage:
        - GET    /api/validateMessage\n
        - GET    /api/inventory\n
        - GET    /api/inventory/<id>\n
    '''
    tron_response = TronResponse(body)

    return tron_response