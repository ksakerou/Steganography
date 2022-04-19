#import sqlite3
from bot_db import User, Database

db = Database("SPECTR.db")
"""
user = User(12663, 1)

db.init_user(user)

user.status = 2

db.init_user(user)
"""

user = db.get_user_by_id(654)
print(user.id, user.status, user.pic, user.src)

#db.del_user_by_id(12663)
"""
try:

    sqlite_connection = sqlite3.connect('SPECTR.db')
    sqlite_create_table_query = '''CREATE TABLE users (
                                id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                status INTEGER NOT NULL,
                                picfile TEXT UNIQUE,
                                srcfile TEXT UNIQUE);'''


    cursor = sqlite_connection.cursor()

    cursor.execute(sqlite_create_table_query)


    sqlite_connection.commit()
    sqlite_connection.close()
    print("F")
except Exception as e:
    print(e)
"""

