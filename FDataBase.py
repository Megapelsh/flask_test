import sqlite3
import math
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getmenu(self):
        try:
            self.__cur.execute('SELECT * FROM mainmenu')
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('DB read error'+str(e))
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

    def showPostList(self):
        try:
            self.__cur.execute('SELECT id, title FROM posts ORDER BY time DESC ')
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('DB read error'+str(e))
        return []

    def getPost(self, post_id):
        sql = '''SELECT title, text, time FROM posts WHERE id = 1'''
        try:
            self.__cur.execute(f'SELECT title, text, time FROM posts WHERE id = {post_id} LIMIT 1')
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('DB read error'+str(e))
        return []
