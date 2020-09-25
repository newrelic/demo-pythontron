import requests
import json

class HttpUtils(object):

    def __init__(self, func_get_headers):
        self.header_demotron_key_prefix = "X-DEMO"
        self.func_get_headers = func_get_headers

    def get_demo_http_headers(self):
        demo_headers = {}
        all_headers = self.func_get_headers()
        for key, header in all_headers:
            if key.upper().startswith(self.header_demotron_key_prefix):
                demo_headers[key.upper()] = header
        return demo_headers

    def query_service(self, url):
        headers = self.get_demo_http_headers()
        response = self.get_request(url, None, headers)
        return response

    def get_request(self, URL, PARAMS, HEADERS=None):
        httpResponse = requests.get(url = URL, params = PARAMS, headers=HEADERS)
        httpResponse.raise_for_status()
        return httpResponse

    def add_response_headers(self, response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Content-type', 'application/json')

        return response
