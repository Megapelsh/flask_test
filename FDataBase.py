import sqlite3
import math
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getmenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('DB read error')
        return []

    def addPost(self, title, post):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES (NULL , ?, ?, ?)', (title, post, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Article add error in DB' + str(e))
            return False

        return True
