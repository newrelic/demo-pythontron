from ..app_logging import AppLogging

class Behavior(object):
  def __init__(self, name, value = None):
    self.name = name
    self.value = value

  def get_name(self):
    return self.name

  def get_value(self):
    return self.value

  def execute(self):
    AppLogging.info("Executing behavior {}".format(self.get_name()))
    return True
