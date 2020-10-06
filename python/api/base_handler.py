import time
import math

class BaseHandler(object):
  def __init__(self, app_config):
    self.app_config = app_config

  def ensure_app_is_started(self):
    delay_start_ms = self.app_config.get_delay_start_ms()
    process_start_time = self.app_config.get_process_start_time()
    current_process_time_ms = math.floor((time.time() - process_start_time)*1000)
    if delay_start_ms > current_process_time_ms:
      message = "The application is not yet ready to accept traffic"
      raise Exception(message)
    return True
