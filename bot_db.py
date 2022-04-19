import sqlite3
import os
from config import *

class User:
    def __init__(self, user_id, status, picfile = '', srcfile = ''):
        self.id = user_id
        self.status = status
        self.pic = picfile
        self.src = srcfile

#успешно своровано у хауди хо
class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread = False)
        self.cur = self.conn.cursor()
    def init_user(self, user_id, status):
        self.cur.execute("""INSERT INTO users (id, status) VALUES(?, ?)
                        ON CONFLICT (id)
                        DO UPDATE SET status = (?), picfile = NULL, srcfile = NULL WHERE id LIKE (?)""",
                        [user_id, status, status, user_id])
        return self.conn.commit()
    def get_by_id(self, user_id):
        try:
            res = self.cur.execute("""SELECT * FROM users WHERE id == (?)""", [user_id]).fetchall()[0]
            user = User(res[0], res[1], res[2], res[3])
            return user
        except IndexError:
            return None
    def del_by_id(self, user_id):
        user = self.get_by_id(user_id)
        self.cur.execute("""DELETE FROM users WHERE id == (?)""", [user_id])
        if user.pic != None:
            os.remove(picpath+user.pic)
        if user.src != None:
            os.remove(srcpath+user.src)
        return self.conn.commit()
    def add_pic(self, user_id, picname):
        self.cur.execute("""UPDATE users SET picfile = (?) WHERE id == (?)""", [picname, user_id])
        return self.conn.commit()
    def add_src(self, user_id, srcname):
        self.cur.execute("""UPDATE users SET srcfile = (?) WHERE id == (?)""", [srcname, user_id])
        return self.conn.commit()
    def close(self):
        self.conn.close()