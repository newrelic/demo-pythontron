from __future__ import print_function

from repository.i_database_connector import IDatabaseConnector
from repository.i_inventory_repository import IInventoryRepository


class DatabaseInventoryRepository(IInventoryRepository):    
    def __init__(self, database_connector: IDatabaseConnector) -> None:
        self.__database_connector = database_connector

    def get_records(self):
        # dictionary=True is to return output as a dictionary, rather than multi dimensional array
        with self.__database_connector.connect().cursor(dictionary=True) as cursor:
            query = ("SELECT * FROM inventory")
            cursor.execute(query)
            return [i for i in cursor]

    def get_record_by_id(self, id):
        with self.__database_connector.connect().cursor(dictionary=True) as cursor:
            query = ("SELECT * FROM inventory "
                     "WHERE id = %s")
            cursor.execute(query, (id,))
            items = [i for i in cursor]
            return items[0] if len(items) == 1 else None
        
    def run_invalid_query(self):
        with self.__database_connector.connect() as cursor:
            query = ("SELECT * FROM inventry")
            cursor.execute(query)
            return [i for i in cursor]
