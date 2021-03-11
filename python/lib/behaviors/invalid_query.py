from repository.database_inventory_repository import \
    DatabaseInventoryRepository

from . import behavior


class InvalidQuery(behavior.Behavior):
    def __init__(self, inventory_repository: DatabaseInventoryRepository):
        super().__init__("INVALID-QUERY")
        self.__inventory_repository = inventory_repository


    def execute(self):
        super.execute()
        self.__inventory_repository.run_invalid_query()
