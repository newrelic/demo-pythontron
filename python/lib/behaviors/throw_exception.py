from . import behavior

class ThrowException(behavior.Behavior):
  def __init__(self):
    super().__init__("THROW")

  def execute(self):
    super().execute()
    reference = None
    reference.execute()
