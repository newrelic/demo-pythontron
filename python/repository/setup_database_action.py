import mysql.connector
from lib.app_logging import AppLogging
from mysql.connector import errorcode

from repository.database_connection_info import DatabaseConnectionInfo
from repository.i_database_connector import IDatabaseConnector


class SetupDatabaseAction():
    def __init__(self, database_connector: IDatabaseConnector,
                 database_connection_info: DatabaseConnectionInfo,
                 inventory_data) -> None:
        self.__database_connector = database_connector
        self.__database_connection_info = database_connection_info
        self.__inventory_data = inventory_data
    
    def execute(self):
        DB_NAME = self.__database_connection_info.database
        # remove this since we dont know if database exists yet.
        self.__database_connection_info.database = None

        cnx = self.__database_connector.connect(**self.__database_connection_info.asdict())
        cursor = cnx.cursor()

        def create_database(cursor):
            try:
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            except mysql.connector.Error as err:
                AppLogging.error("Failed creating database: {}".format(err))
                exit(1)

        try:
            cursor.execute("USE {}".format(DB_NAME))
            AppLogging.info("Database already exists")
        except mysql.connector.Error as err:
            AppLogging.info("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                AppLogging.info("Database {} created successfully.".format(DB_NAME))
                cnx.database = DB_NAME

                TABLES = {}
                TABLES['inventory'] = (
                    "CREATE TABLE `inventory` ("
                    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
                    "  `item` varchar(14) NOT NULL,"
                    "  `sku` varchar(80) NOT NULL,"
                    "  `price` varchar(14) NOT NULL,"
                    "  PRIMARY KEY (`id`)"
                    ") ENGINE=InnoDB")

                AppLogging.info("Creating inventory table . . .")

                for table_name in TABLES:
                    table_description = TABLES[table_name]
                    try:
                        AppLogging.info("Creating table {}: ".format(table_name))
                        cursor.execute(table_description)
                    except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                            AppLogging.error("table already exists.")
                        else:
                            AppLogging.error(err.msg)
                    else:
                        AppLogging.info("OK")

                AppLogging.info("Inserting inventory data . . .")

                add_inventory_item = ("INSERT INTO inventory "
                                    "(item, price, sku) "
                                    "VALUES (%(item)s, %(price)s, %(sku)s)")

                for item in self.__inventory_data:
                    cursor.execute(add_inventory_item, item)
                    cnx.commit()

                cursor.close()
                cnx.close()
            else:
                AppLogging.error(err)
                exit(1)
