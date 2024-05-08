import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='SuaiYarik281_',
    db='librarymodel',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
