from configparser import ConfigParser

FILENAME = 'db_config.ini'
SECTION = 'DATABASE'


def config(filename=FILENAME, section=SECTION):
    parser = ConfigParser()
    parser.read(filename)

    host = parser.get(section, 'host')
    database = parser.get(section, 'database')
    user = parser.get(section, 'user')
    password = parser.get(section, 'password')
    port = parser.get(section, 'port')

    return {
        'user': user,
        'password': password,
        'database': database,
        'host': host,
        'port': port,
    }
