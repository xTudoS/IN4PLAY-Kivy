from db.fabricas import fabrica_conexao


class Users_Repositorio:

    @staticmethod
    def add_user(user, passwd, word):
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        cursor = fabrica.cursor()
        try:
            fabrica.begin()
            cursor.execute("INSERT INTO users(nick, passwd, word) VALUES (%s, %s, %s)", (user, passwd, word))
            fabrica.commit()
        except:
            fabrica.rollback()
        finally:
            fabrica.close()

    @staticmethod
    def add_record(record, id):
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        cursor = fabrica.cursor()
        try:
            fabrica.begin()
            cursor.execute("INSERT INTO users(record) VALUES (%s)", (id, record))
            fabrica.commit()
        except:
            fabrica.rollback()

        finally:
            fabrica.close()

    @staticmethod
    def set_record(id, record):
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        cursor = fabrica.cursor()
        try:
            fabrica.begin()
            cursor.execute("UPDATE users SET record = %s WHERE id = %s", (str(record), str(id)))
            fabrica.commit()
        except:
            fabrica.rollback()

        finally:
            fabrica.close()

    @staticmethod
    def get_records(id):
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        try:
            cursor = fabrica.cursor()
            cursor.execute(f"SELECT record FROM users WHERE id = {id}")

        finally:
            fabrica.close()
        a = cursor.fetchall()
        for x in a:
            for y in x:
                return y

    @staticmethod
    def get_users():
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        try:
            cursor = fabrica.cursor()
            cursor.execute("SELECT * FROM users")

        finally:
            fabrica.close()

        return cursor.fetchall()

    @staticmethod
    def get_word(id):
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        try:
            cursor = fabrica.cursor()
            cursor.execute(f"SELECT word FROM users WHERE id = {str(id)}")

        finally:
            fabrica.close()

        return cursor.fetchone()[0]

    @staticmethod
    def set_word(id, word):
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        try:
            cursor = fabrica.cursor()
            cursor.execute("UPDATE users SET word = %s WHERE nick = %s", (str(word), str(id)))

        finally:
            fabrica.close()

    @staticmethod
    def get_recordsAll():
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        try:
            cursor = fabrica.cursor()
            cursor.execute("SELECT nick,record FROM users")
        finally:
            fabrica.close()
        records = cursor.fetchall()
        records3 = []
        records2 = []

        for record in records:
            records3.append(record[1])
        records3.sort(reverse=True)
        records = list(records)
        while len(records2) < len(records):
            for record in records3:
                for nick in records:
                    if record == nick[1]:
                        if nick not in records2:
                            records2.append(nick)

        while len(records2) > 10:
            records2.pop(-1)
        return records2

    @staticmethod
    def get_id(user):
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        try:
            cursor = fabrica.cursor()
            cursor.execute("SELECT * FROM users")

        finally:
            fabrica.close()
        a = cursor.fetchall()
        for x in a:
            if x[1].lower() == user.lower():
                return x[0]
        #return cursor.fetchall()[0]
