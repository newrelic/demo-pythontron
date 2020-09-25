import json


class DataStore(object):
    
    def get_records(self):
        file_path = "data/inventory.json"
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data

    def get_record_by_id(self, key):
        data = self.get_records()
        item = self._find_by_key(data, "id", key)
        if item is not None:
            return item
        else:
            return {}
    
    @classmethod
    def _find_by_key(obj, json_object, key_name, key_value):
        for item in json_object:
            if item[key_name] == key_value:
                return item