from random import shuffle
from time import sleep
from pygame import mixer

from kivy.app import App
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.config import Config

from db.entidades import easy_questions
from db.repositorios import users_repositorio

import configparser

Builder.load_file('main.kv')

try:
    import crypt # Unix
except:
    import pcrypt as crypt  # Windows

config = configparser.ConfigParser()
config.read('config.ini')

Config.set('graphics', 'fullscreen', config['DISPLAY']['fullscreen'])
Config.set('graphics', 'width', config['DISPLAY']['width'])
Config.set('graphics', 'height', config['DISPLAY']['height'])
Config.set('kivy', 'window_icon', 'img/logo.png')

record = 0


class Telas(ScreenManager):
    pass


class Welcome(Screen):
    mixer.init()
    mixer.music.load('sound/kalimba.mp3')
    mixer.music.play(-1)

    def on_pre_enter(self, *args):
        self.add_widget(Teste())


class Teste(BoxLayout):
    def __init__(self, **kwargs):
        self.pos_hint = {'y': .25}
        super().__init__(**kwargs)
        textos = BoxLayout(orientation='vertical', size_hint=(.8, .55))

        welcome = Label(text='\nWelcome', color=(0, 0, 0, 1), halign='center', font_name='fonts/DEPLETED_URANIUM.ttf',
                        font_size=60)
        to = Label(text='\nTo', color=(0, 0, 0, 1), halign='right', font_size=60, font_name='fonts/DEPLETED_URANIUM.ttf')
        in4play = Label(text='\nIN4PLAY', color=(0, 0, 0, 1), font_size=60, font_name='fonts/DEPLETED_URANIUM.ttf')
        conexao = Label(text='\nClick anywhere on the screen', color=(0, 0, 0, 1), font_name='fonts/LittleBird.ttf',
                        font_size=20)
        logo = Image(source='img/logo.png')

        textos.add_widget(logo)
        textos.add_widget(welcome)
        textos.add_widget(to)
        textos.add_widget(in4play)
        textos.add_widget(conexao)

        self.add_widget(textos)

        animText = Animation(color=get_color_from_hex('#A90D0D'), duration=0.5) + Animation(
            color=get_color_from_hex('#600CCF'), duration=0.5)
        animText.repeat = True
        animText.start(welcome)

        animText = Animation(color=get_color_from_hex('#0B77CA'), duration=0.5) + Animation(
            color=get_color_from_hex('#0DA927'), duration=0.5)
        animText.repeat = True
        animText.start(to)

        animText = Animation(color=(0, 0, 0, 1)) + Animation(color=get_color_from_hex('#FFD700'))
        animText.repeat = True

        animText.start(in4play)


class Menu2(Screen):

    def signOut(self):
        popup = SignOut()
        popup.title = 'About:'
        popup.open()

    def close(self):
        popup = Close()
        popup.title = 'Quit?'
        popup.open()

    def leaderboards(self):
        popup = Leaderboards()
        popup.title = 'leaderboards'.upper()
        popup.open()


class Leaderboards(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        records = users_repositorio.Users_Repositorio.get_recordsAll()
        for record in records:
            self.ids.lider.add_widget(L2(texto=record))


class L2(BoxLayout):

    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        for record in texto:
            self.add_widget(Button(text=str(record)))


class Close(Popup):
    pass


class Credits(Popup):
    pass


class CronoWidget(Label):
    # Código copiado e adaptado de https://cadernodelaboratorio.com.br/2015/07/29/associando-eventos-a-botoes-no-kivy/
    cronoValue = NumericProperty()
    cronoValueText = StringProperty()
    habilitaContagem = BooleanProperty(False)

    def update(self, *args):
        self.cronoValueText = str(round(self.cronoValue))
        if self.habilitaContagem:
            self.cronoValue -= 0.1
            if self.cronoValue <= 0:
                self.ids.time.focus = True

    def zerar(self):
        if not self.habilitaContagem:
            self.cronoValue = 30

    def iniciar(self):
        self.cronoValue = 30
        self.habilitaContagem = True

    def parar(self):
        self.habilitaContagem = False


class Perguntas(Screen):
    qts = easy_questions.nQ
    id_q = 1
    fimGame = 1
    bonus = 1

    def on_pre_enter(self):
        self.idq = easy_questions.aleatorio2()
        self.addQuestion()

    def addQuestion(self):
        if self.id_q > self.qts:
            self.id_q = 1
            if self.fimGame > self.qts:
                self.bonus = 1
                self.ids.fimGame.focus = True
                self.manager.current = 'fim'

            self.fimGame = 1
            self.manager.transition.direction = 'down'
            sleep(0.3)
        else:
            self.cronos = CronoWidget()
            self.cronos.iniciar()
            Clock.schedule_interval(self.cronos.update, 0.1)

            self.ids.box.add_widget(self.cronos)
            self.ids.box.add_widget(Pergunta(tQ=self.idq[self.id_q - 1]))
            answers = list(easy_questions.answers(self.idq[self.id_q - 1]))
            self.id_q += 1
            self.fimGame += 1
            perguntas = []
            for x in answers:
                for y in x:
                    perguntas.append(y)
                    break
            correct = perguntas[0]
            while len(perguntas) > 4:
                perguntas.pop(-1)

            shuffle(perguntas)
            for pergunta in perguntas:
                if pergunta == correct:
                    self.ids.box.add_widget(AlternativaCorrect(text=str(pergunta), correct=True))
                else:
                    self.ids.box.add_widget(Alternativa(text=str(pergunta)))
            del perguntas

    def removeAll(self, remove=False, parar=False, correct=False):

        if remove:
            self.cronos.parar()
            self.cronos.zerar()
            self.ids.box.clear_widgets()
            if correct:
                globals()['record'] += (2000 * self.bonus)
                self.bonus += 1
            else:
                globals()['record'] -= 500
                self.bonus = 1
        globals()['record'] -= (60 * self.cronos.cronoValue)
        if parar:
            self.id_q = self.qts + 1

        self.addQuestion()


class Alternativa(BoxLayout):
    correct = ''
    qts = easy_questions.questions

    def __init__(self, text='', correct=False, **kwargs):
        super().__init__(**kwargs)
        self.ids.alternativa.text = text

        if correct:
            self.correct = text

    def corrects(self, text):

        if text == self.correct:
            return True
        else:
            return False


class AlternativaCorrect(BoxLayout):
    correct = ''
    qts = easy_questions.questions

    def __init__(self, text='', correct=False, **kwargs):
        super().__init__(**kwargs)
        self.ids.alternativa.text = text

        if correct:
            self.correct = text

    def corrects(self, text):
        if text == self.correct:
            return True
        else:
            return False


class Pergunta(BoxLayout):

    def __init__(self, tQ, **kwargs):
        super().__init__(**kwargs)
        self.qts = easy_questions.questions1(tQ)[0]
        self.addPergunta()

    def addPergunta(self):
        question = self.qts
        question = self.quebraLinha(question)
        self.ids.label.text = question
        # self.i.pop(0)

    def quebraLinha(self, word):
        word2 = word.split(' ')
        if len(word) > 10:
            w = ''
            for x, y in enumerate(word2):
                w += y
                w += '\n' if x != 0 and x % 7 == 0 else ' '
            return w
        return word


class SignOut(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.logoff.text = '''The game is based around answering questions about IT (Information Technology) and testing
your knowledge about it. You need a high level of knowledge to answer everything right. The
game has a leaderboard so you can compare your highscore to the score done by others players
or yourself. If the answer is right, the button will turn green, if it’s wrong it will turn red. Also be
careful, if you answer anything wrong you lose points. You need to create an account with a
nickname and password to play.'''


class Finish(Screen):
    def on_pre_enter(self, *args):
        r = globals()['record']
        id_user = globals()['id_user']
        records = users_repositorio.Users_Repositorio.get_records(str(id_user))
        if records < r:
            users_repositorio.Users_Repositorio.set_record(id_user, r)
        self.ids.finish.text = f'Congratulations!\n\nYou have reached\n\nthe end of this round!\n\nFinal Score\n{r}'
        globals()['record'] = 0


class User(Screen):
    mudar_nick = 1
    mudar_pass = 1

    def nickMudar(self):
        global mudar_nick
        if self.mudar_nick == 1:
            self.mudar_nick = 0
            return 'Nickname'
        elif self.mudar_nick == 0:
            self.mudar_nick = None
            self.ids.nick.text = ''

    def passMudar(self):
        if self.mudar_pass == 1:
            self.mudar_pass = 0
            return 'Password'
        elif self.mudar_pass == 0:
            self.ids.passwd.password = True
            self.ids.passwd.text = ''
            self.mudar_pass = None

    def errorSingUp(self):
        popup = ErrorSignUp()
        popup.title = 'ERROR SIGN UP:'
        popup.open()

    def errorLogIn(self):
        popup = ErrorLogIn()
        popup.title = 'ERROR LOG IN:'
        popup.open()

    def remover_espacos(self, word):
        a = ''
        for x in word:
            if x.isalnum():
                a += x
        return a

    def signup(self):
        usrs = users_repositorio.Users_Repositorio.get_users()
        nickname = self.remover_espacos(self.ids.nick.text)
        password = self.remover_espacos(self.ids.passwd.text)
        if nickname.lower() == 'nickname' or password.lower() == 'password':
            self.errorSingUp()
            return None
        if (4 <= len(password) <= 8) and (0 < len(nickname) <= 255):
            for x in usrs:
                if nickname.lower() == x[1].lower():
                    self.errorSingUp()
                    return None
        else:
            self.errorSingUp()
            return None

        salt = crypt.mksalt(crypt.METHOD_SHA512)
        password = crypt.crypt(password, salt)
        users_repositorio.Users_Repositorio.add_user(nickname, password, salt)
        self.ids.passwd.text = ''
        globals()['id_user'] = users_repositorio.Users_Repositorio.get_id(nickname)
        self.manager.current = 'menu'
        self.manager.transition.direction = 'left'

    def login(self):
        usrs = users_repositorio.Users_Repositorio.get_users()
        nickname = self.ids.nick.text
        password = self.remover_espacos(self.ids.passwd.text)
        nickname = self.remover_espacos(nickname)
        for x in usrs:
            if nickname.lower() == x[1].lower():
                salt = users_repositorio.Users_Repositorio.get_word(x[0])
                password = crypt.crypt(password, salt)
                if password == x[2]:
                    self.ids.passwd.text = ''
                    self.manager.current = 'menu'
                    globals()['id_user'] = x[0]
                    self.manager.transition.direction = 'left'
                else:
                    self.errorLogIn()
                return None

        else:
            self.errorLogIn()


class ErrorSignUp(Popup):
    pass


class ErrorLogIn(Popup):
    pass


class TimeOut(Screen):

    def on_pre_enter(self, *args):
        record = globals()['record']
        id_user = globals()['id_user']
        if users_repositorio.Users_Repositorio.get_records(id_user) < record:
            users_repositorio.Users_Repositorio.set_record(id_user, record)
        self.ids.timeOut.text = f'Oh no!\n\nYour time is over!\n\nTry to be faster next time!\n\nFinal Score\n{record}'
        globals()['record'] = 0


class Menu(App):

    def build(self):
        self.title = 'IN4PLAY'
        self.icon = 'img/logo.png'
        self.root = Telas()
        return self.root


Menu().run()
