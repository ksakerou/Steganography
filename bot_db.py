import sqlite3
import os

from config import *


def copyfile(file_path, file_name):
    i = 0
    while (str(i) + '_' + file_name) in os.listdir(secretpath):
        i = i + 1
    
    with open(file_path + file_name, 'rb') as fin:
        bin_file = fin.read()
    
    with open(secretpath + str(i) + '_' + file_name, 'wb') as fout:
        fout.write(bin_file)


class User:
    def __init__(self, user_id, status, picfile = '', srcfile = ''):
        self.id = user_id
        self.status = status
        self.pic = picfile
        self.src = srcfile


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread = False)
        self.cur = self.conn.cursor()

    def init_user(self, user_id, status):
        self.cur.execute('''INSERT INTO users (id, status) VALUES(?, ?)
                        ON CONFLICT (id)
                        DO UPDATE SET status = (?), picfile = NULL, srcfile = NULL WHERE id LIKE (?)''',
                        [user_id, status, status, user_id])
    
        return self.conn.commit()
    
    def get_by_id(self, user_id):
        try:
            res = self.cur.execute('SELECT * FROM users WHERE id == (?)', [user_id])
            res = res.fetchall()
            res = res[0]
            user = User(res[0], res[1], res[2], res[3])
            return user
    
        except IndexError:
            return None
    
    def del_by_id(self, user_id):
        user = self.get_by_id(user_id)
    
        if user != None:
            self.cur.execute('DELETE FROM users WHERE id == (?)', [user_id])
    
            if user.pic != None:
                copyfile(picpath, user.pic)
                os.remove(picpath + user.pic)
                pass
            if user.src != None:
                copyfile(srcpath, user.src)
                os.remove(srcpath + user.src)
    
        return self.conn.commit()
    
    def add_pic(self, user_id, picname):
        self.cur.execute('UPDATE users SET picfile = (?) WHERE id == (?)', [picname, user_id])
        return self.conn.commit()
    
    def add_src(self, user_id, srcname):
        self.cur.execute('UPDATE users SET srcfile = (?) WHERE id == (?)', [srcname, user_id])
        return self.conn.commit()
    
    def close(self):
        self.conn.close()