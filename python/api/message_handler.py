import json
from lib.app_logging import AppLogging
from lib.behavior_actions import handle_behaviors_pre, handle_behaviors_post
from lib.tron_response import TronResponse
from .base_handler import BaseHandler

class MessageHandler(object):
    def __init__(self, app_config, http_utils, behavior_repository, createResponseFunc = None):
        self.http_utils = http_utils
        self.app_config = app_config
        self.behavior_repository = behavior_repository
        self.createResponseFunc = createResponseFunc
        if createResponseFunc is None:
            self.createResponseFunc = (lambda x,y,z: TronResponse.createResponse(x,y,z))

    def validate(self):
        BaseHandler(self.app_config).ensure_app_is_started()
        AppLogging.info("validate_message")
        handle_behaviors_pre(self.behavior_repository, self.http_utils.get_demo_http_headers())

        data = { "result" : True }
        tron_response = self.createResponseFunc(data, self.app_config, self.http_utils)

        urls = self.app_config.get_dependency_endpoint('/api/validateMessage')
        if urls is not None:
            for url in urls:
                if url is not None:
                    downstream_response = self.http_utils.query_service(url)
                    tron_response.append_trace(self.http_utils, downstream_response)

        handle_behaviors_post(self.behavior_repository, self.http_utils.get_demo_http_headers())
        
        return tron_response
