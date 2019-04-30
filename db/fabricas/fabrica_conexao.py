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
            host='mysql.uhserver.com',
            db='in4play',
            user='xtudos',
            passwd='passwdjooj2019*'
        )
        return db
