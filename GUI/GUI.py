from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum
import sys
sys.path.insert(1,"/home/daniel/Project/neuron_poker/gym_env")
from env import Action

path = "/home/daniel/Project/neuron_poker/GUI/resources/SBS - 2D Poker Pack/Top-Down/Cards/individual/"
path2 = "/home/daniel/Project/neuron_poker/GUI/resources/"
file_path = "/home/daniel/Project/neuron_poker/GUI/action.txt"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1127, 817)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.communityCardsLabel = QtWidgets.QLabel(self.centralwidget)
        self.communityCardsLabel.setGeometry(QtCore.QRect(490, 190, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.communityCardsLabel.setFont(font)
        self.communityCardsLabel.setObjectName("communityCardsLabel")
        self.communityCard1 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard1.setGeometry(QtCore.QRect(270, 240, 88, 124))
        self.communityCard1.setText("")
        self.communityCard1.setPixmap(QtGui.QPixmap(path+"AD.png"))
        self.communityCard1.setObjectName("communityCard1")
        self.communityCard2 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard2.setGeometry(QtCore.QRect(403, 240, 88, 124))
        self.communityCard2.setText("")
        self.communityCard2.setPixmap(QtGui.QPixmap(path+"KD.png"))
        self.communityCard2.setObjectName("communityCard2")
        self.communityCard3 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard3.setGeometry(QtCore.QRect(538, 240, 88, 124))
        self.communityCard3.setText("")
        self.communityCard3.setPixmap(QtGui.QPixmap(path+"QD.png"))
        self.communityCard3.setObjectName("communityCard3")
        self.communityCard4 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard4.setGeometry(QtCore.QRect(671, 240, 88, 124))
        self.communityCard4.setText("")
        self.communityCard4.setPixmap(QtGui.QPixmap(path+"JD.png"))
        self.communityCard4.setObjectName("communityCard4")
        self.communityCard5 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard5.setGeometry(QtCore.QRect(804, 240, 88, 124))
        self.communityCard5.setText("")
        self.communityCard5.setPixmap(QtGui.QPixmap(path+"10D.png"))
        self.communityCard5.setObjectName("communityCard5")
        self.tableSprite = QtWidgets.QLabel(self.centralwidget)
        self.tableSprite.setGeometry(QtCore.QRect(110, 80, 901, 411))
        self.tableSprite.setAutoFillBackground(False)
        self.tableSprite.setText("")
        self.tableSprite.setPixmap(QtGui.QPixmap(path2+"table_top_empty.png"))
        self.tableSprite.setObjectName("tableSprite")
        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setGeometry(QtCore.QRect(275, 710, 111, 41))
        self.checkButton.setObjectName("checkButton")
        self.checkButton.clicked.connect(self.checkAction)
        self.raiseButton = QtWidgets.QPushButton(self.centralwidget)
        self.raiseButton.setGeometry(QtCore.QRect(565, 710, 111, 41))
        self.raiseButton.setObjectName("raiseButton")
        self.callButton = QtWidgets.QPushButton(self.centralwidget)
        self.callButton.setGeometry(QtCore.QRect(420, 710, 111, 41))
        self.callButton.setObjectName("callButton")
        self.callButton.clicked.connect(self.callAction)
        self.foldButton = QtWidgets.QPushButton(self.centralwidget)
        self.foldButton.setGeometry(QtCore.QRect(710, 710, 111, 41))
        self.foldButton.setObjectName("foldButton")
        self.foldButton.clicked.connect(self.foldAction)
        self.playerCard1 = QtWidgets.QLabel(self.centralwidget)
        self.playerCard1.setGeometry(QtCore.QRect(450, 550, 88, 124))
        self.playerCard1.setText("")
        self.playerCard1.setPixmap(QtGui.QPixmap(path+"AC.png"))
        self.playerCard1.setObjectName("playerCard1")
        self.playerCard2 = QtWidgets.QLabel(self.centralwidget)
        self.playerCard2.setGeometry(QtCore.QRect(560, 550, 88, 124))
        self.playerCard2.setText("")
        self.playerCard2.setPixmap(QtGui.QPixmap(path+"2C.png"))
        self.playerCard2.setObjectName("playerCard2")
        self.playerChipsLabel = QtWidgets.QLabel(self.centralwidget)
        self.playerChipsLabel.setGeometry(QtCore.QRect(450, 510, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.playerChipsLabel.setFont(font)
        self.playerChipsLabel.setObjectName("playerChipsLabel")
        self.opponentChipsLabel = QtWidgets.QLabel(self.centralwidget)
        self.opponentChipsLabel.setGeometry(QtCore.QRect(450, 40, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.opponentChipsLabel.setFont(font)
        self.opponentChipsLabel.setObjectName("opponentChipsLabel")
        self.opponentLastActionLabel = QtWidgets.QLabel(self.centralwidget)
        self.opponentLastActionLabel.setGeometry(QtCore.QRect(450, 20, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.opponentLastActionLabel.setFont(font)
        self.opponentLastActionLabel.setObjectName("opponentLastActionLabel")
        self.tableSprite.raise_()
        self.communityCard2.raise_()
        self.communityCard1.raise_()
        self.communityCard3.raise_()
        self.communityCard4.raise_()
        self.communityCard5.raise_()
        self.communityCardsLabel.raise_()
        self.checkButton.raise_()
        self.raiseButton.raise_()
        self.callButton.raise_()
        self.foldButton.raise_()
        self.playerCard1.raise_()
        self.playerCard2.raise_()
        self.playerChipsLabel.raise_()
        self.opponentChipsLabel.raise_()
        self.opponentLastActionLabel.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1127, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.communityCardsLabel.setText(_translate("MainWindow", "Community Cards"))
        self.checkButton.setText(_translate("MainWindow", "CHECK"))
        self.raiseButton.setText(_translate("MainWindow", "RAISE"))
        self.callButton.setText(_translate("MainWindow", "CALL"))
        self.foldButton.setText(_translate("MainWindow", "FOLD"))
        self.playerChipsLabel.setText(_translate("MainWindow", "Player Chips: $500"))
        self.opponentChipsLabel.setText(_translate("MainWindow", "Opponent Chips: $500"))
        self.opponentLastActionLabel.setText(_translate("MainWindow", "Last Action: CHECK"))

    def renderTableCards(self, community_cards):
        self.communityCard1.clear()
        self.communityCard2.clear()
        self.communityCard3.clear()
        self.communityCard4.clear()
        self.communityCard5.clear()

        for i in range(len(community_cards)):
            card = community_cards[i]
            if i == 0:
                self.communityCard1.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 1:
                self.communityCard2.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 2:
                self.communityCard3.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 3:
                self.communityCard4.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 4:
                self.communityCard5.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))

    def renderHandCards(self, hand):
        self.playerCard1.setPixmap(QtGui.QPixmap(path+hand[0]+'.png'))
        self.playerCard2.setPixmap(QtGui.QPixmap(path+hand[1]+'.png'))

    def renderChipAmounts(self, playerChips, opponentChips):
        self.playerChipsLabel.setText("Player Chips: $"+str(playerChips))
        self.opponentChipsLabel.setText( "Opponent Chips: $"+str(opponentChips))

    def renderLastAction(self, last_action):
        if not(last_action == None):
            self.opponentLastActionLabel.setText("Last Action: "+last_action.name)
        else:
            self.opponentLastActionLabel.setText("")
    
    def renderActionButtons(self, legal_moves):
        raise_3bb = False
        raise_pot = False
        raise_2pot = False
        all_in = False

        legal_values = [e.value for e in legal_moves]

        if Action.CHECK.value in legal_values:
            self.checkButton.show()
        else:
            self.checkButton.hide()
        
        if Action.CALL.value in legal_values:
            self.callButton.show()
        else:
            self.callButton.hide()
        
        if Action.RAISE_3BB.value in legal_values:
            raise_3bb = True
        if Action.RAISE_POT.value in legal_values:
            raise_pot = True
        if Action.RAISE_2POT.value in legal_values:
            raise_2pot = True
        if Action.ALL_IN.value in legal_values:
            all_in = True

        if raise_3bb or raise_pot or raise_2pot or all_in:
            self.raiseButton.show()
        else:
            self.raiseButton.hide()

        return [raise_3bb, raise_pot, raise_2pot, all_in]


    def write_action_to_file(self, action):
        with open(file_path,'r+') as myfile:
            data = myfile.read()
            myfile.seek(0)
            myfile.write(action)
            myfile.truncate()

    def callAction(self):
        self.write_action_to_file(str(Action.CALL.value))
    
    def checkAction(self):
        self.write_action_to_file(str(Action.FOLD.value))
        
    
    def foldAction(self):
        self.write_action_to_file(str(Action.FOLD.value))
