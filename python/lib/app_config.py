import json
import sys
import random
import functools
import time

class AppConfig(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.file = None
        self.process_start_time = time.time()

    def get_app_config_value(self, key):
        if self.file is None:
            self.file = self._parse_json_file()

        if key in self.file:
            return self.file[key]
        return None

    def get_dependency_endpoint(self, endpoint):
        dependency_endpoints = []

        for dependency in self.get_app_config_value('dependencies'):
            if dependency is not None:
                urls = dependency['urls']
                for url in urls:
                    if url is not None:
                        dependency_endpoint = url.strip() + endpoint
                        dependency_endpoints.append(dependency_endpoint)

        return dependency_endpoints

    def get_app_id(self):
        app_id = self.get_app_config_value('id')
        if app_id is None:
            app_id = "No Api ID defined"
        return app_id

    def get_app_port(self):
        app_port = self.get_app_config_value('port')
        if app_port is None:
           raise Exception('No Api port defined')
        return app_port

    def get_delay_start_ms(self):
        delay_start_ms = self.get_app_config_value('delayStartMs')
        if delay_start_ms is None:
           return 0
        return delay_start_ms

    def get_process_start_time(self):
        return self.process_start_time

    def _parse_json_file(self):
        file_path = self.config_file
        if file_path is not None:
            with open(file_path) as json_file:
              data = json.load(json_file)
              return data
        else:
            raise Exception('No configuration file defined')

    def _pick_one_random(self, elements):
      if elements == None:
        return None

      if len(elements) == 0:
        return None
      return random.choice(elements)
