import MySQLdb as mysql
from datetime import datetime
import os


class MySQLConnection:

    def __init__(self, trello_conn):
        self.connection = None
        self.execution_time = datetime.now()
        self.trello_connection = trello_conn
        try:
            self.connection = mysql.connect(user=os.getenv('MYSQL_USER'), passwd=os.getenv('MYSQL_PASSWORD'),
                                            db=os.getenv('MYSQL_DATABASE'), host=os.getenv('MYSQL_HOST'))
        except:
            print('Não foi possível conectar ao banco')

    def get_db_lists(self):
        query = 'SELECT LIST_ID FROM LISTS ORDER BY LIST_POS DESC'
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            db_lists = cursor.fetchall()
            return db_lists
        except:
            print('ERRO')
            return 0

    def close(self):
        self.connection.close()
