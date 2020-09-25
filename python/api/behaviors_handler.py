from lib.app_config import AppConfig
from lib.tron_response import TronResponse
from lib.app_logging import AppLogging
import json

class BehaviorsHandler(object):
  def __init__(self, app_config, behavior_repository):
    self.app_config = app_config
    self.behavior_repository = behavior_repository

  def list_behaviors(self):
    AppLogging.info("behaviors")

    behaviors = self.behavior_repository.get_available_behaviors()
    body = json.dumps(behaviors)
    tron_response = TronResponse(body)
    return tron_response
