""" Creates the DB Schema for the music database """
import sqlite3
from sqlite3 import Error
from sqlite3 import OperationalError


def create_connection(db_file):
    """ Creates connection to SQLite db """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as connection_error:
        print connection_error
    return None


def build_db_from_sql(db_conn, filename):
    """ Reads SQL from a file, and runs the commands
    on the sql db connection.  Throws an exception if any
    of the sql statements are invalid. """
    with open(filename) as s_file:
        sql = s_file.read()
        sql_statements = sql.split(";")

    for statement in sql_statements:
        try:
            db_conn.execute(statement)
        except OperationalError, msg:
            print "Command skipped: ", msg


if __name__ == "__main__":

    DB_CONNECTION = create_connection("hw13.db")
    if DB_CONNECTION:
        build_db_from_sql(DB_CONNECTION, "school.sql")
