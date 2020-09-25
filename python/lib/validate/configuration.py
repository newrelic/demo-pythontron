import json
import sys

from jsonschema import Draft6Validator, ValidationError, validate
from lib.validate import schema
from lib.app_logging import AppLogging

class Configuration(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def validate_config(self):
        errors = self.validate_json()
        if errors is not None and len(errors) > 0:
            config_file_path = self.config_file
            AppLogging.error('****Configuration file ' + config_file_path +' is not valid*****')
            for error in errors:
                AppLogging.error('  ' +error)
            raise SystemExit

    def validate_json(self):
        config_file_path = self.config_file
        s = schema.get_schema()
        errors = None
        if config_file_path is not None:
            with open(config_file_path) as json_file:
                try:
                    instance = json.load(json_file)
                except:
                    return ['file is not a JSON file']
                v = Draft6Validator(s)
                validation_errors = sorted(v.iter_errors(instance), key=str)
                errors = self._parse_errors(validation_errors)
                return errors
        else:
            AppLogging.error('No configuration file defined')
            raise Exception('No configuration file defined')

    def _parse_errors(self, errors):
        error_messages = []
        for error in errors:
            error_messages.append(error.message)
        return error_messages
