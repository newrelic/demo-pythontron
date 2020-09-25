from lib.string_utils import StringUtils

MAX_LENGTH_TRACE = 1000

class Trace(object):
    @staticmethod
    def getHeaderKey():
        return "X-DEMOTRON-TRACE"

    @staticmethod
    def should_trace(http_utils):
        if Trace.getHeaderKey() in http_utils.get_demo_http_headers():
            return True
        return False

    @staticmethod
    def getResponseTrace(response):
        if response is not None:
            if Trace.getHeaderKey() in response.headers:
                trace = response.headers.get(Trace.getHeaderKey())
                return trace

        return None
