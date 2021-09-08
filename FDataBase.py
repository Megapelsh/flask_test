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
