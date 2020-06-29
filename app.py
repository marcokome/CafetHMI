from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Pipe
from threading import Thread
import sys, random, math, json, time, requests, subprocess

class laclef_window(QtWidgets.QMainWindow):
    clicked = QtCore.pyqtSignal()
    scanned = QtCore.pyqtSignal(int)

    def __init__(self):

        super(laclef_window, self).__init__()
        self.rpi = False # Set to True if run this code on your RPI
        self.test = True # Set to False if you are going to use it for real

        self.default_width = 800
        self.default_height = 480

        self.waiting_for_confirmation = False
        self.on_error_page = False

        self.uid = ''
        self.uid_test = '2a3b7710'

        f = open('items.json', 'r')

        self.items = json.load(f)

        f.close()

        self.default_font = 'Kreon'

        self.user_name = "Default D."
        self.user_solde = 50.0
        self.snack_id = 1

        self.setupUi(self)
        self.setupHome(self)
        self.setupErrorPage(self)
        self.setupChoices(self)
        self.setupDetails(self)
        self.setupConfirmation(self)

        self.showHome()
        #self.showChoices()

    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(self.default_width, self.default_height)
        font = QtGui.QFont()
        font.setFamily(self.default_font)
        font.setPointSize(34)
        Frame.setFont(font)

    def setupHome(self, Frame):
        self.frame_homepage = QtWidgets.QFrame(Frame)
        self.frame_homepage.setGeometry(QtCore.QRect(0, 0, self.default_width, self.default_height))
        self.frame_homepage.setObjectName("frame_homepage")
        self.frame_homepage.setAutoFillBackground(True)
        self.frame_homepage.setStyleSheet("background: rgba(255, 255, 255, 255);")
        self.homepage_label = QtWidgets.QLabel(self.frame_homepage)
        self.homepage_label.setGeometry(QtCore.QRect(20, 140, 481, 197))
        font = QtGui.QFont()
        font.setFamily(self.default_font)
        font.setPointSize(34)
        self.homepage_label.setFont(font)
        self.homepage_label.setAlignment(QtCore.Qt.AlignCenter)
        self.homepage_label.setObjectName("homepage_label")
        self.homepage_label.setText("Badgez ici \n SVP")

        self.widget_home = QtWidgets.QLabel(self.frame_homepage)
        self.widget_home.setGeometry(QtCore.QRect(550, 130, 220, 220))
        self.widget_home.setObjectName("widget_home")

        pic = QtGui.QMovie('imgs/home.gif')
        self.widget_home.setMovie(pic)
        pic.start()

        self.frame_homepage.hide()

    def showHome(self):
        self.frame_homepage.show()

        Thread(target=self.checkForBadge).start()

    def hideHome(self):
        self.frame_homepage.hide()

    def setupErrorPage(self, Frame):
        self.frame_errorpage = QtWidgets.QFrame(Frame)
        self.frame_errorpage.setGeometry(QtCore.QRect(0, 0, self.default_width, self.default_height))
        self.frame_errorpage.setObjectName("frame_errorpage")
        self.frame_errorpage.setAutoFillBackground(True)
        self.frame_errorpage.setStyleSheet("background: rgba(255, 255, 255, 255);")
        self.errorpage_label_up = QtWidgets.QLabel(self.frame_errorpage)
        self.errorpage_label_up.setGeometry(QtCore.QRect(40, 140, 481, 51))
        self.errorpage_label_up.setAlignment(QtCore.Qt.AlignCenter)
        self.errorpage_label_down = QtWidgets.QLabel(self.frame_errorpage)
        self.errorpage_label_down.setGeometry(QtCore.QRect(40, 280, 481, 61))
        self.errorpage_label_down.setAlignment(QtCore.Qt.AlignCenter)
        self.errorpage_label_number = QtWidgets.QLabel(self.frame_errorpage)
        self.errorpage_label_number.setGeometry(QtCore.QRect(40, 180, 481, 91))
        self.errorpage_label_number.setAlignment(QtCore.Qt.AlignCenter)
        self.errorpage_label_alert = QtWidgets.QLabel(self.frame_errorpage)
        self.errorpage_label_alert.setGeometry(QtCore.QRect(0, 410, self.default_width, 20))
        self.errorpage_label_alert.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont()
        font1.setFamily(self.default_font)
        font1.setPointSize(11)
        font2 = QtGui.QFont()
        font2.setFamily(self.default_font)
        font2.setPointSize(34)
        font3 = QtGui.QFont()
        font3.setFamily(self.default_font)
        font3.setPointSize(10)
        self.errorpage_label_up.setFont(font1)
        self.errorpage_label_down.setFont(font1)
        self.errorpage_label_number.setFont(font2)
        self.errorpage_label_alert.setFont(font3)

        self.widget_error = QtWidgets.QLabel(self.frame_errorpage)
        self.widget_error.setGeometry(QtCore.QRect(550, 130, 220, 220))
        self.widget_error.setObjectName("widget_error")

        pic = QtGui.QMovie('imgs/error.gif')
        self.widget_error.setMovie(pic)
        pic.start()

        self.frame_errorpage.hide()

    def showErrorPage(self, nbr):
        self.errorpage_label_up.setText("Ton badge n'est pas reconnu")
        self.errorpage_label_number.setText(f"{nbr}")
        self.errorpage_label_down.setText("Envoie le code ci-dessus à \n baptiste.gaultier@imt-atlantique.fr \n Il saura quoi faire")
        self.errorpage_label_alert.setText("Touchez l'écran pour revenir à l'acceuil")

        self.on_error_page = True
        self.frame_errorpage.show()

    def showErrorNetwork(self):
        self.errorpage_label_up.setText("Réseau indisponible !")
        self.errorpage_label_number.setText("")
        self.errorpage_label_down.setText("Contactez \n baptiste.gaultier@imt-atlantique.fr \n Il saura quoi faire")
        self.errorpage_label_alert.setText("Touchez l'écran pour revenir à l'acceuil")

        self.on_error_page = True
        self.frame_errorpage.show()

    def hideErrorPage(self):
        self.frame_errorpage.hide()

    def setupChoices(self, Frame):
        self.frame_choices = QtWidgets.QFrame(Frame)
        self.frame_choices.setGeometry(QtCore.QRect(0, 0, self.default_width, self.default_height))
        self.frame_choices.setObjectName("frame_choices")
        self.frame_choices.setTabletTracking(True)

        self.layoutWidget = QtWidgets.QWidget(self.frame_choices)
        self.layoutWidget.setGeometry(QtCore.QRect(3, 111, 801, 291))
        self.layoutWidget.setObjectName("layoutWidget")

        self.frame_choices.setStyleSheet("background: rgba(252, 254, 252, 255);")

        self.Layout_choices = QtWidgets.QVBoxLayout(self.frame_choices)
        self.Layout_choices.setSpacing(10)
        self.Layout_choices.setObjectName("Layout_choices")
        self.choices_label = QtWidgets.QLabel(self.frame_choices)
        font = QtGui.QFont()
        font.setFamily(self.default_font)
        font.setPointSize(17)
        self.choices_label.setFont(font)
        self.choices_label.setLineWidth(1)
        self.choices_label.setGeometry(QtCore.QRect(0, 20, 800, 81))
        self.choices_label.setAlignment(QtCore.Qt.AlignCenter)
        self.choices_label.setObjectName("label")

        self.gridLayoutWidget = QtWidgets.QWidget(self.frame_choices)
        self.gridLayoutWidget.hide()
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 120, 800, 400))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)

        self.widget_choices = QtWidgets.QLabel(self.frame_choices)
        self.widget_choices.setGeometry(QtCore.QRect(0, 0, 101, 101))
        self.widget_choices.setObjectName("widget_home")

        pic = QtGui.QMovie('imgs/hey.gif')
        self.widget_choices.setMovie(pic)
        pic.start()

        j = 0
        k = 0
        self.buttons = {}
        layout_pos = [(30, 130), (280, 130), (530, 130),
                        (30, 270), (280, 270), (530, 270)]
        # Create buttons
        for i in range(6):
            b = QtWidgets.QPushButton(self.frame_choices)
            b.setMinimumSize(QtCore.QSize(0, 125))
            b.setObjectName(str(i))
            b.setText("bouton{}".format(i))
            f = QtGui.QFont()
            f.setFamily(self.default_font)
            f.setPointSize(11)
            b.setFont(f)
            b.setStyleSheet("border-radius: 5px; border:2px solid black; background: white;")
            b.setStyleSheet("background: solid grey;")
            self.buttons['button{}'.format(i)] = b
            self.buttons['button{}'.format(i)].setGeometry(QtCore.QRect(layout_pos[i][0], layout_pos[i][1], 231, 125))

            k = k + 1 if k < 2 else 0
            j = 1 if i > 1 else 0

        self.choices_button_back = QtWidgets.QPushButton(self.frame_choices)
        self.choices_button_back.setGeometry(QtCore.QRect(270, 430, 271, 25))
        self.choices_button_back.setFlat(True)
        f = QtGui.QFont()
        f.setFamily(self.default_font)
        f.setPointSize(11)
        self.choices_button_back.setFont(f)


        self.frame_choices.hide()

    def showChoices(self):
        #Set user name
        self.choices_label.setText("Salut {} ! \n On prend quoi aujourd\'hui ?".format(self.user_name))
        self.choices_button_back.setText("<-- Je ne prend rien finalement...")

        for i in range(6):
            self.buttons['button{}'.format(i)].setText(self.items[i]['desc'])
            self.buttons['button{}'.format(i)].setObjectName(self.items[i]['id'])

        self.buttons['button0'].clicked.connect(lambda: self.hideChoices(self.buttons['button0']))
        self.buttons['button1'].clicked.connect(lambda: self.hideChoices(self.buttons['button1']))
        self.buttons['button2'].clicked.connect(lambda: self.hideChoices(self.buttons['button2']))
        self.buttons['button3'].clicked.connect(lambda: self.hideChoices(self.buttons['button3']))
        self.buttons['button4'].clicked.connect(lambda: self.hideChoices(self.buttons['button4']))
        self.buttons['button5'].clicked.connect(lambda: self.hideChoices(self.buttons['button5']))

        self.choices_button_back.clicked.connect(self.backHome)

        self.frame_choices.show()


    def backHome(self):
        self.frame_choices.hide()
        self.showHome()

    def hideChoices(self, id):
        print('yep')
        self.frame_choices.hide()
        self.snack_id = id.objectName()
        self.showDetails(self, self.snack_id)

    def setupDetails(self, Frame):
        self.frame_details = QtWidgets.QFrame(Frame)
        self.frame_details.setGeometry(QtCore.QRect(0, 0, self.default_width, self.default_height))
        self.frame_details.setObjectName("frame_details")
        self.frame_details.setStyleSheet("background: rgb(252, 254, 252);")
        self.label_detail_price_calcul = QtWidgets.QLabel(self.frame_details)
        self.label_detail_price_calcul.setGeometry(QtCore.QRect(280, 230, 281, 41))
        self.label_detail_price_calcul.setAlignment(QtCore.Qt.AlignCenter)
        self.label_detail_price_calcul.setObjectName("label_detail_price_calcul")
        self.label_detail = QtWidgets.QLabel(self.frame_details)
        self.label_detail.setGeometry(QtCore.QRect(10, 130, 151, 221))
        self.label_detail.setAlignment(QtCore.Qt.AlignCenter)
        self.label_detail.setObjectName("label")
        font_2 = QtGui.QFont()
        font_2.setPointSize(11)
        font_2.setFamily(self.default_font)
        self.label_detail.setFont(font_2)

        self.button_validate = QtWidgets.QPushButton(self.frame_details)
        self.button_validate.setGeometry(QtCore.QRect(280, 300, 281, 57))
        self.button_validate.setObjectName("button_validate")
        self.button_validate.setFont(font_2)
        self.button_validate.setStyleSheet("border-radius: 5px; border:4px solid black;")
        self.label_detail_price = QtWidgets.QLabel(self.frame_details)
        self.label_detail_price.setGeometry(QtCore.QRect(280, 110, 281, 121))
        font = QtGui.QFont()
        font.setPointSize(70)
        font.setFamily(self.default_font)
        self.label_detail_price.setFont(font)
        self.label_detail_price.setTextFormat(QtCore.Qt.PlainText)
        self.label_detail_price.setAlignment(QtCore.Qt.AlignCenter)
        self.label_detail_price.setObjectName("label_detail_price")

        self.button_minus = QtWidgets.QPushButton(self.frame_details)
        self.button_minus.setGeometry(QtCore.QRect(170, 270, 89, 89))
        self.button_minus.setObjectName("button_minus")
        self.button_minus.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/moins.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_minus.setIcon(icon)
        self.button_minus.setIconSize(QtCore.QSize(30, 30))

        #self.button_minus.setFont(font_2)
        self.button_minus.setStyleSheet("border-radius: 44px; border:4px solid black;")

        self.button_back = QtWidgets.QPushButton(self.frame_details)
        self.button_back.setGeometry(QtCore.QRect(0, 20, 50, 50))
        self.button_back.setObjectName("button_back")
        self.button_back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_back.setIcon(icon)
        self.button_back.setFlat(True)
        self.button_back.setFont(font_2)

        self.button_plus = QtWidgets.QPushButton(self.frame_details)
        self.button_plus.setGeometry(QtCore.QRect(170, 130, 89, 89))
        self.button_plus.setObjectName("button_plus")
        self.button_plus.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_plus.setIcon(icon)
        self.button_plus.setIconSize(QtCore.QSize(30, 30))

        #self.button_plus.setFont(font_2)
        self.button_plus.setStyleSheet("border-radius: 44px; border:4px solid black;")

        self.label_detail_price_calcul.setFont(font_2)

        self.widget_details = QtWidgets.QLabel(self.frame_details)
        self.widget_details.setGeometry(QtCore.QRect(580, 130, 201, 201))
        self.widget_details.setObjectName("widget_details")

        pic = QtGui.QMovie('imgs/select.gif')
        self.widget_details.setMovie(pic)
        pic.start()

        self.button_plus.clicked.connect(lambda : self.addItem(1))
        self.button_minus.clicked.connect(lambda : self.removeItem(1))
        self.button_validate.clicked.connect(lambda : self.validate(1))
        self.button_back.clicked.connect(self.back)

        self.frame_details.hide()

    def showDetails(self, Frame, id):
        #Get item price and infos
        self.price = next((float(self.items[i]['price']) for i in range(6) if self.items[i]['id'] == id), 0)
        self.nbr = 1
        detail_name = next((self.items[i]['desc'] for i in range(6) if self.items[i]['id'] == id), 0)

        self.label_detail_price_calcul.setText("({}x{}€)".format(self.nbr, self.price))
        self.label_detail_price.setText("{}€".format(str(round(self.nbr*self.price,3))))
        self.label_detail.setText(detail_name)
        self.button_validate.setText("Valider")

        self.frame_details.show()

    def addItem(self, id):
        self.nbr = self.nbr + 1
        self.label_detail_price.setText("{}€".format(str(round(self.nbr*self.price,3))))
        self.label_detail_price_calcul.setText("({}x{}€)".format(self.nbr, self.price))

    def removeItem(self, id):
        self.nbr = self.nbr - 1 if self.nbr - 1 > 0 else 0
        self.label_detail_price.setText("{}€".format(str(round(self.nbr*self.price,3))))
        self.label_detail_price_calcul.setText("({}x{}€)".format(self.nbr, self.price))

    def validate(self, id):
        self.frame_details.hide()
        self.showConfirmation(self)

    def back(self):
        self.frame_details.hide()
        self.showChoices()


    def setupConfirmation(self, Frame):
        self.frame_confirmation = QtWidgets.QFrame(Frame)
        self.frame_confirmation.setGeometry(QtCore.QRect(0, 0, self.default_width, self.default_height))
        self.frame_confirmation.setObjectName("frame_confirmation")
        self.frame_confirmation.setStyleSheet("background: rgb(249, 252, 249);")

        self.label_solde = QtWidgets.QLabel(self.frame_confirmation)
        self.label_solde.setGeometry(QtCore.QRect(0, 280, 531, 111))
        self.label_solde.setAlignment(QtCore.Qt.AlignCenter)
        self.label_solde.setObjectName("label_solde")
        font2 = QtGui.QFont()
        font2.setFamily(self.default_font)
        font2.setPointSize(17)
        self.label_solde.setFont(font2)

        self.label_confirmation = QtWidgets.QLabel(self.frame_confirmation)
        self.label_confirmation.setGeometry(QtCore.QRect(0, 126, 531, 191))
        self.label_confirmation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_confirmation.setObjectName("label_confirmation")
        font = QtGui.QFont()
        font.setFamily(self.default_font)
        font.setPointSize(49)
        self.label_confirmation.setFont(font)


        self.label_alert = QtWidgets.QLabel(self.frame_confirmation)
        self.label_alert.setGeometry(QtCore.QRect(0, 400, self.default_width, 20))
        self.label_alert.setAlignment(QtCore.Qt.AlignCenter)
        self.label_alert.setObjectName("label_alert")
        font3 = QtGui.QFont()
        font3.setFamily(self.default_font)
        font3.setPointSize(10)
        self.label_alert.setFont(font3)

        self.widget_confirmation = QtWidgets.QLabel(self.frame_confirmation)
        self.widget_confirmation.setGeometry(QtCore.QRect(550, 130, 220, 220))
        self.widget_confirmation.setObjectName("widget_confirmation")

        pic = QtGui.QMovie('imgs/bisou.gif')
        self.widget_confirmation.setMovie(pic)
        pic.start()

        self.frame_confirmation.hide()

    def showConfirmation(self, Frame):
        #self.user_solde = self.pay(self.uid_test if self.test else self.uid, self.snack_id, self.nbr)
        self.label_confirmation.setText("Merci \n{} !".format(self.user_name))
        self.label_solde.setText("Un instant ...")
        self.label_alert.setText("Touchez l'écran pour revenir à l'acceuil")

        self.waiting_for_confirmation = True

        self.frame_confirmation.show()

        Thread(target=self.async_paiement, args=(self.uid_test if self.test else self.uid, self.snack_id, self.nbr)).start()

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            print(event.pos())
            print("blahblah")
            if self.waiting_for_confirmation:
                self.frame_confirmation.hide()
                self.showHome()
                self.waiting_for_confirmation = False
            elif self.on_error_page:
                self.hideErrorPage()
                self.showHome()
                self.on_error_page = False

    def async_paiement(self, uid, snack_id, qty):
        self.user_solde = self.pay(uid,snack_id,qty)
        self.label_solde.setText("Ton nouveau solde est de {}€".format(self.user_solde))

    def updateData(self):
        req = requests.get('http://api.laclef.cc/snacks')
        items = [(e['id'], e['description_fr_FR'], e['price']) for e in req.json()['response'] if e['visible'] == '1']

        f = open('items.json', 'w')
        f.write(json.dumps(items))
        f.close()

    def pay(self, uid, snack_id, qty):
        data = {"uid":uid,"service":1,"order":{"snack_{}".format(snack_id):qty}}
        req = requests.post('http://api.laclef.cc/swipes/2', data=json.dumps(data))
        print(req.json())
        return req.json()['balance']


    def getUserInfos(self, uid):
        try:
            req = requests.get('http://api.laclef.cc/tags/{}'.format(uid))
        except Exception as e:
            return (None,)

        print(req.json()['response'])
        if req.json()['response']['owner'] is None:
            return None
        else:
            name = "{} {}.".format(req.json()['response']['owner']['firstname'].capitalize(),req.json()['response']['owner']['lastname'][0].upper())
            balance = req.json()['response']['owner']['balance']
            return (name, balance)

    def checkForBadge(self):
        print("start the polling...")
        self.scan() if self.rpi else self.scan_test()

    def scan(self):
        while True:
            lines=subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null','w'))
            uid = next((line.decode().replace(' ','').split(':')[1] for line in lines.splitlines() if b'UID' in line), None)
            if uid != None:
                self.buzz()
                print('Uid: {} '.format(uid))
                #uid = uid[:7].replace('0','')
                #print(f'Uid (Legacy Code): {uid}')
                self.uid = uid
                user_infos = self.getUserInfos(self.uid_test if self.test else self.uid)

                if user_infos is None:
                    self.scanned.emit(2)
                elif len(user_infos) == 1:
                    self.scanned.emit(3)
                else:
                    self.user_name = user_infos[0]
                    self.user_solde = user_infos[1]
                    self.scanned.emit(1)

                break


    def buzz(self):
        import RPi.GPIO as GPIO
        from time import sleep

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        buzzer_pin = 23
        timeout = 0.001
        stop = 100
        count = 0

        GPIO.setup(buzzer_pin, GPIO.OUT)

        while True:
            GPIO.output(buzzer_pin, GPIO.HIGH)
            sleep(timeout)
            GPIO.output(buzzer_pin, GPIO.LOW)
            sleep(timeout)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            sleep(timeout)
            count += 1

            if count == stop:
                break

    def scan_test(self):
        while True:
            f = open('test.json', 'r')
            data = json.load(f)
            f.close()
            print(data['id'])
            # 0: nothing happend, 1: badge exists in db, 2: badge unknown
            if data['id'] == 1:
                user_infos = self.getUserInfos(self.uid_test)
                if user_infos is None:
                    self.scanned.emit(2)
                elif len(user_infos) == 1:
                    self.scanned.emit(3)
                else:
                    self.user_name = user_infos[0]
                    self.user_solde = user_infos[1]
                    self.scanned.emit(1)

                break
            else:
                print("Nope")

            time.sleep(3)

    def on_event_received(self, val):
        print(f"Scanné: {val}")
        if val == 1: # Badge known
            self.showChoices()
            self.hideHome()
        elif val == 2: # Badge unknown
            self.hideHome()
            self.showErrorPage(self.uid_test if self.test else self.uid)
        elif val == 3:
            self.hideHome()
            self.showErrorNetwork()
