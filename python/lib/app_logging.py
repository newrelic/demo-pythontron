import sys
import datetime
import logging

class AppLogging(object):
  _logger = None

  @staticmethod
  def init(logging_level):
    levels = {
      'critical': logging.CRITICAL,
      'error': logging.ERROR,
      'warn': logging.WARNING,
      'warning': logging.WARNING,
      'info': logging.INFO,
      'debug': logging.DEBUG
    }
    level = levels.get(logging_level.lower())
    if level is None:
      level = logging.INFO
    AppLogging._logger = logging.getLogger()
    AppLogging._logger.setLevel(level)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s  %(message)s')
    # create console handler with a higher log level
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    AppLogging._logger.addHandler(consoleHandler)

  @staticmethod
  def trace(message):
    AppLogging._logger.debug(message)

  @staticmethod
  def info(message):
    AppLogging._logger.info(message)

  @staticmethod
  def warning(message):
    AppLogging._logger.warning(message)

  @staticmethod
  def error(message):
    AppLogging._logger.error(message)
