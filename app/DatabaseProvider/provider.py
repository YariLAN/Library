import pymysql.cursors

from settings import users

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='SuaiYarik281_',
    db='librarymodel',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


class ProviderDb:
    connection = None

    def __init__(self):
        pass

    def set_connection(self, role: str):
        self.connection = pymysql.connect(
            host='localhost',
            user=users[role]['name'],
            password=users[role]['password'],
            db='librarymodel',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
