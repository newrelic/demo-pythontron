from random import seed, random, randint
from math import sqrt, log, cos, pi, ceil
from multiprocessing import Process
import time
import json
from . import behavior
from ..app_logging import AppLogging
import uuid
import sys

MAX_KEY = "max"
MIN_KEY = "min"

class Malloc(behavior.Behavior):
  Allocated = []

  def __init__(self, value):
    super().__init__("MALLOC", value)

  def execute(self):
    super().execute()

    config = self.get_configuration(self.get_value())
    if config is None:
      return False

    # Randomly select a duration length within the range
    numberKb = self.sample(time.time(), config[MIN_KEY], config[MAX_KEY])
    AppLogging.info("Allocating {}KB".format(numberKb))
    self.allocateKB(numberKb)
    return True

  def allocateKB(self, numberKB):
    # 1KB is 64 guids (16 bytes)
    size = int(numberKB*64)
    data = []
    for _ in range(size):
      data.append(uuid.uuid4())
    Malloc.Allocated.append(data)
    return True

  def sample(self, seed_num, min_val, max_val):
    seed(seed_num)

    # Ensure there isn't a zero value
    r_1 = 1 - random()
    r_2 = 1 - random()

    # This is a Box Muller transform. Given 2 indepenent samples from a uniform distribution
    # this formula will generate a random variable that will follow a normal distribution.
    # Source: https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform
    box_muller = sqrt(-2.0 * log(r_1)) * cos(2.0 * pi + r_2)
    # Convert to a value between 0 and 1
    decimal_bm = box_muller / 10.0 + 0.5

    value = min_val + (decimal_bm * (max_val+1 - min_val))
    return int(value)

  def is_value_valid(self, value):
    if (
        value is None               or
        not isinstance(value, list) or
        len(value) < 2
    ):
      AppLogging.warning(
          "Could not get compute parameters for behavior, input expected is an array of 2 integers, got: {}"
          .format(self.get_value()))
      return False

    return True
      

  def is_range_valid(self, value):
    if (
        not isinstance(value[0], int) or
        not isinstance(value[1], int) or
        value[0] > value[1]
    ):
      AppLogging.warning(
          "Could not get valid compute parameters for behavior, min: {} max: {}"
          .format(value[0], value[1]))
      return False

    return True

  def parse_json(self, value):
    parsed_value = None
    try:
      parsed_value = json.loads(value)
    except json.decoder.JSONDecodeError:
      # The block below will catch this case
      AppLogging.warning(
          "Unable to parse configuration for behavior. details: {}"
          .format(value))
      return None

    return parsed_value

  def get_configuration(self, value):
    parsed_val = self.parse_json(value)
    if not self.is_value_valid(parsed_val):
      return None

    if not self.is_range_valid(parsed_val):
      return None

    config = {}
    config[MIN_KEY] = parsed_val[0]
    config[MAX_KEY] = parsed_val[1]

    return config 
