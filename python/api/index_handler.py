from lib.app_config import AppConfig
from lib.tron_response import TronResponse
from lib.app_logging import AppLogging

class IndexHandler(object):
  def __init__(self, app_config, behavior_repository):
    self.app_config = app_config
    self.behavior_repository = behavior_repository

  def index_message(self):
    AppLogging.info("index")

    body = self.get_message()
    tron_response = TronResponse(body)
    return tron_response

  def get_message(self):
    app_id = self.app_config.get_app_id()
    message = "Pythontron (" +app_id +") is up and running!"
    return message
