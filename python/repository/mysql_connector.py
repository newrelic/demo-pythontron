import mysql.connector
from lib.app_logging import AppLogging
from mysql.connector import errorcode

from repository.database_connection_info import DatabaseConnectionInfo
from repository.i_database_connector import IDatabaseConnector


class MySqlConnector(IDatabaseConnector):
    def __init__(self, connection_info: DatabaseConnectionInfo) -> None:
        self.__connectin_info = connection_info
        self.__connection = None

    def connect(self, **kwargs):
        try:
            if self.__connection == None:
                # if options are provided, dont use default options
                connect_options = kwargs if len(
                    kwargs) > 0 else self.__connectin_info.asdict()

                self.__connection = mysql.connector.connect(
                    **connect_options)

            return self.__connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                AppLogging.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                AppLogging.error("Database does not exist")
            else:
                AppLogging.error(err)
