from db.fabricas import fabrica_conexao


class Users_Repositorio:

    @staticmethod
    def add_user(user, passwd, word):
        try:
            fabrica = fabrica_conexao.FabricaConexao.conect()
        except:
            fabrica = fabrica_conexao.FabricaConexao.conectar()
        cursor = fabrica.cursor()
        try:
            cursor.execute("INSERT INTO users(nick, passwd, word) VALUES (?, ?, ?)", (user, passwd, word))
        except:
            cursor.execute("INSERT INTO users(nick, passwd, word) VALUES (%s, %s, %s)", (user, passwd, word))
        fabrica.commit()

    @staticmethod
    def set_record(id, record):
        try:
            fabrica = fabrica_conexao.FabricaConexao.conect()
        except:
            fabrica = fabrica_conexao.FabricaConexao.conectar()
        cursor = fabrica.cursor()
        try:
            cursor.execute("UPDATE users SET record = ? WHERE id = ?", (str(record), str(id)))
        except:
            cursor.execute("UPDATE users SET record = %s WHERE id = %s", (str(record), str(id)))
        fabrica.commit()

    @staticmethod
    def get_records(id):
        try:
            fabrica = fabrica_conexao.FabricaConexao.conect()
        except:
            fabrica = fabrica_conexao.FabricaConexao.conectar()

        cursor = fabrica.cursor()
        try:
            cursor.execute("SELECT record FROM users WHERE id = ?", (str(id),))
        except:
            cursor.execute("SELECT record FROM users WHERE id = %s", str(id))

        a = cursor.fetchall()
        for x in a:
            for y in x:
                return y

    @staticmethod
    def get_users():
        try:
            fabrica = fabrica_conexao.FabricaConexao.conect()
        except:
            fabrica = fabrica_conexao.FabricaConexao.conectar()

        cursor = fabrica.cursor()
        cursor.execute("SELECT * FROM users")

        return cursor.fetchall()

    @staticmethod
    def get_word(id):
        try:
            fabrica = fabrica_conexao.FabricaConexao.conect()
        except:
            fabrica = fabrica_conexao.FabricaConexao.conectar()

        cursor = fabrica.cursor()
        try:
            cursor.execute("SELECT word FROM users WHERE id = ?", (str(id),))
        except:
            cursor.execute("SELECT word FROM users WHERE id = %s", str(id))

        return cursor.fetchone()[0]


    @staticmethod
    def get_recordsAll():
        try:
            fabrica = fabrica_conexao.FabricaConexao.conect()
        except:
            fabrica = fabrica_conexao.FabricaConexao.conectar()

        cursor = fabrica.cursor()
        cursor.execute("SELECT nick,record FROM users")

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
        try:
            fabrica = fabrica_conexao.FabricaConexao.conect()
        except:
            fabrica = fabrica_conexao.FabricaConexao.conectar()

        cursor = fabrica.cursor()
        cursor.execute("SELECT * FROM users")

        a = cursor.fetchall()
        for x in a:
            if x[1].lower() == user.lower():
                return x[0]

    @staticmethod
    def get_status():
        try:
            fabrica_conexao.FabricaConexao.conect()
        except:
            return False

        return True
