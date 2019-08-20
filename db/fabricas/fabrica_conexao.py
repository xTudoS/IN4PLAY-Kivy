import pymysql
import sqlite3


class FabricaConexao:

    @staticmethod
    def conectar():
        db = sqlite3.connect('in4play.db')

        return db

    @staticmethod
    def conect():
        db = pymysql.connect(
            host='host',
            db='db',
            user='user',
            passwd='password'
        )
        return db
