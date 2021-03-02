from lib.app_logging import AppLogging

import json

import os

def response(body, status_code = 200):
    return {
        'body': body,
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }

def unauth_resp():
    AppLogging.info("Authorization header not present.")
    return response('Unauthorized', 401)

def lambda_handler(event, context):
    AppLogging.init('info')
    auth_header_key = 'Authorization'
    auth_string = "Bearer ABC123"
    headers = event['headers'] or dict()
    endpoint = (event['resource'] or "").lower()

    AppLogging.info(endpoint)
    if endpoint == "/cancellations":
        if (not auth_header_key in headers) or (headers[auth_header_key] != auth_string):
            return unauth_resp()
        else:
            return response(json.dumps({ 'a': 15, 'b': 78 }))
    elif endpoint == "/end-test":
        if (not auth_header_key in headers) or (headers[auth_header_key] != auth_string):
            return unauth_resp()
        else:
            return response('Test ended')
    else:
        return response('Unsupport endpoint: ' + endpoint, 404)
