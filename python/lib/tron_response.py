import json

from lib.trace import Trace

class TronResponse(object):

    def __init__(self, body="", headers=None, status_code=200):
        self.body = body
        self.status_code = status_code
        if headers is not None:
            self.headers = headers
        else:
            self.headers = dict()

    @staticmethod
    def createResponse(data, app_config, http_utils):
        body = json.dumps(data)
        tron_response = TronResponse(body)
        app_id = app_config.get_app_id()
        tron_response.trace(http_utils, app_id)
        return tron_response

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def add_header(self, key, value):
        if key in self.headers:
            self.headers[key] = self.headers[key] +"," +value
        else:
            self.headers[key] = value

    def get_headers(self):
        return self.headers

    def set_status_code(self, status_code):
        self.status_code = status_code

    def get_status_code(self):
        return self.status_code

    def trace(self, http_utils, app_id):
        if Trace.should_trace(http_utils):
            self.add_header(Trace.getHeaderKey(), app_id)
        return None

    def append_trace(self,  http_utils, downstream_response):
        if Trace.should_trace(http_utils):
            trace = Trace.getResponseTrace(downstream_response)
            self.add_header(Trace.getHeaderKey(), trace)
