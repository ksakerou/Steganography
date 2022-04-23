import sqlite3
from config import *

try:
    sqlite_connection = sqlite3.connect(dbname)
    sqlite_create_table_query = '''CREATE TABLE users (
                                    id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                    status TEXT NOT NULL,
                                    picfile TEXT UNIQUE,
                                    srcfile TEXT UNIQUE);'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    sqlite_connection.close()
except Exception as e:
    print(e)
