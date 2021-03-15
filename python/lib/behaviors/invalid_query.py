from repository.database_inventory_repository import \
    DatabaseInventoryRepository

from . import behavior


class InvalidQuery(behavior.Behavior):
    def __init__(self, database_inventory_repository: DatabaseInventoryRepository, value=None):
        super().__init__("INVALID-QUERY", value)
        self.__database_inventory_repository = database_inventory_repository

    def execute(self):
        super().execute()
        self.__database_inventory_repository.run_invalid_query()
