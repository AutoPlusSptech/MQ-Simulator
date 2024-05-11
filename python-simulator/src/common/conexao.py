import pymysql
import pymssql


class Conexao:
    
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = pymysql.connect(user=user, password=password, host=host, database=database)
        self.cursor = self.connection.cursor()
        
    def insert(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
        
    def getLastId(self):
        return self.cursor.lastrowid