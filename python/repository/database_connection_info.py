from dataclasses import asdict, dataclass


@dataclass
class DatabaseConnectionInfo():
    """This class encapsulates connection information for connecting to a database.

    Attributes:
        user (str): name of user to connect with.
        password (str): password of the user.
        host (str): address of the host to connect to.
        database (str): name of the database to connect to.

    """

    user: str
    password: str
    host: str
    port: str
    database: str

    def asdict(self):
        # remove options that aren't set, assuming they arent used so dont supply them
        return {key: value for key, value in asdict(self).items() if value != None}
