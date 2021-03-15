from . import behavior


class ThrowException(behavior.Behavior):
  def __init__(self, value = None):
    super().__init__("THROW", value)

  def execute(self):
    super().execute()
    reference = None
    reference.execute()
