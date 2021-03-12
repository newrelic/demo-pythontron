class Repository(object):
  def __init__(
      self,
      available_behaviors=None,
      behavior_factory_func=None,
      app_id=""
  ):
    self.available_behaviors = available_behaviors if available_behaviors is not None else Repository.get_available_behaviors()
    self.behavior_factory_func = behavior_factory_func
    self.app_id = app_id
    self.behaviors_header_key = "X-DEMO"

  @staticmethod
  def get_available_behaviors():
    return ["THROW", "COMPUTE", "MALLOC", "INVALID-QUERY"]

  def get_by_request(self, headers, step):
    behaviors = map(lambda name: self.find_behaviors(
        name, headers, step), self.available_behaviors)
    behaviors = filter(lambda b: b is not None, behaviors)
    return behaviors

  def find_behaviors(self, name, headers, step):
    key = "{}-{}-{}".format(self.behaviors_header_key, name, step).upper()
    key_with_app_id = "{}-{}".format(key, self.app_id).upper()

    behavior = self.lookup_and_create(key, name, headers)
    targeted_behavior = self.lookup_and_create(key_with_app_id, name, headers)
    if targeted_behavior is not None:
      behavior = targeted_behavior

    return behavior

  def lookup_and_create(self, key, name, headers):
    value = headers.get(key, None)
    if value is None:
      return None

    # .lower().replace() is sanitizing the name so it can match a keyword argument
    # example: INVALID-QUERY -> invalid_query
    return self.behavior_factory_func(name.lower().replace('-', '_'), value=value)
