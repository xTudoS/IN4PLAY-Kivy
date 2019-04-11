from db.fabricas import fabrica_conexao
from random import shuffle, choice

fabrica = fabrica_conexao.FabricaConexao.conectar()
cursor = fabrica.cursor()

cursor.execute("SELECT * FROM easy_questions")

questions = list(cursor.fetchall())


cursor.execute("SELECT answer FROM easy_answers")

#answer = cursor.fetchall()


def questions1(id):
    cursor.execute("SELECT question FROM easy_questions WHERE id = %s", str(id))

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
    cursor.execute("SELECT answer FROM easy_answers WHERE id = %s", str(id_question))

    return cursor.fetchall()


def get_ans():
    globals()['aleatorio']
    l = []
    for x in aleatorio:
        l.append(answers(x))

    return l

