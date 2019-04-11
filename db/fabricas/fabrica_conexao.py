import pymysql


class FabricaConexao:

    @staticmethod
    def conectar():
        db = pymysql.connect(
            user='xtudos',
            passwd='passwdjooj2019*',
            db='in4play',
            host='in4play.mysql.uhserver.com'
        )

        return db
