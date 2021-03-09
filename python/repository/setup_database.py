from __future__ import print_function

import mysql.connector
from dependency_injection_container import Container
from dependency_injector.wiring import Provide, inject
from mysql.connector import errorcode
from repository.database_connection_info import DatabaseConnectionInfo

from repository.i_database_connector import IDatabaseConnector


@inject
def execute(database_connector: IDatabaseConnector = Provide[Container.database_connector],
            database_connection_info: DatabaseConnectionInfo = Provide[Container.database_connection_info],
            inventory_data = Provide[Container.inventory_data]):

    DB_NAME = database_connection_info.database
    # remove this since we dont know if database exists yet.
    database_connection_info.database = None

    cnx = database_connector.connect(**database_connection_info.asdict())
    cursor = cnx.cursor()

    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
        print("Database already exists")
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
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

            print("Creating inventory table . . .")

            for table_name in TABLES:
                table_description = TABLES[table_name]
                try:
                    print("Creating table {}: ".format(table_name), end='')
                    cursor.execute(table_description)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print("OK")

            print("Inserting inventory data . . .")

            add_inventory_item = ("INSERT INTO inventory "
                                  "(item, price, sku) "
                                  "VALUES (%(item)s, %(price)s, %(sku)s)")

            for item in inventory_data:
                cursor.execute(add_inventory_item, item)
                cnx.commit()

            cursor.close()
            cnx.close()
        else:
            print(err)
            exit(1)
