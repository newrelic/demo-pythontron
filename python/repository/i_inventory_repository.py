from abc import ABC, abstractmethod


class IInventoryRepository(ABC):
    @abstractmethod
    def get_records(self):
        raise NotImplementedError()

    @abstractmethod
    def get_record_by_id(self, id):
        raise NotImplementedError()

    @staticmethod
    def _find_by_key(self, dict, key_name, key_value):
        for item in dict:
            if item[key_name] == key_value:
                return item
