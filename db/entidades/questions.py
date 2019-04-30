from db.fabricas import fabrica_conexao
from random import shuffle, choice

erro = 0

try:
    fabrica = fabrica_conexao.FabricaConexao.conectar()
    cursor = fabrica.cursor()
    cursor.execute("SELECT * FROM questions")
except:
    erro = 1

if erro:
    fabrica = fabrica_conexao.FabricaConexao.conect()
    cursor = fabrica.cursor()
    cursor.execute("SELECT * FROM questions")
    
    
questions = list(cursor.fetchall())


cursor.execute("SELECT answer FROM answers")


def questions1(id):
    erro = 0

    try:
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        cursor = fabrica.cursor()
        cursor.execute("SELECT question FROM questions WHERE id = ?", (str(id),))
    except:
        erro = 1

    if erro:
        fabrica = fabrica_conexao.FabricaConexao.conect()
        cursor = fabrica.cursor()
        cursor.execute("SELECT question FROM questions WHERE id = %s", (str(id),))

    return cursor.fetchone()


def aleatorio2():
    global questions
    shuffle(questions)
    q = []
    for x in questions:
        q.append(x[0])
    while len(q) > 12:
        q.remove(choice(q))
    return q


aleatorio = aleatorio2()
nQ = len(aleatorio)


def answers(id_question):
    erro = 0

    try:
        fabrica = fabrica_conexao.FabricaConexao.conectar()
        cursor = fabrica.cursor()
        cursor.execute("SELECT answer FROM answers WHERE id = ?", (str(id_question),))
    except:
        erro = 1

    if erro:
        fabrica = fabrica_conexao.FabricaConexao.conect()
        cursor = fabrica.cursor()
        cursor.execute("SELECT answer FROM answers WHERE id = %s", (str(id_question),))
    
    return cursor.fetchall()


def get_ans():
    globals()['aleatorio']
    l = []
    for x in aleatorio:
        l.append(answers(x))

    return l


fabrica.close()
