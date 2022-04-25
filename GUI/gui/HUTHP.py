# Form implementation generated from reading ui file 'HUTHP.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1680, 1050)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.communityCardsLabel = QtWidgets.QLabel(self.centralwidget)
        self.communityCardsLabel.setGeometry(QtCore.QRect(710, 280, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.communityCardsLabel.setFont(font)
        self.communityCardsLabel.setStyleSheet("font: 14pt \"Georgia\";")
        self.communityCardsLabel.setObjectName("communityCardsLabel")
        self.communityCard1 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard1.setGeometry(QtCore.QRect(500, 370, 88, 124))
        self.communityCard1.setText("")
        self.communityCard1.setPixmap(QtGui.QPixmap("../res/sprites/cards/AD.png"))
        self.communityCard1.setObjectName("communityCard1")
        self.communityCard2 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard2.setGeometry(QtCore.QRect(630, 370, 88, 124))
        self.communityCard2.setText("")
        self.communityCard2.setPixmap(QtGui.QPixmap("../res/sprites/cards/KD.png"))
        self.communityCard2.setObjectName("communityCard2")
        self.communityCard3 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard3.setGeometry(QtCore.QRect(760, 370, 88, 124))
        self.communityCard3.setText("")
        self.communityCard3.setPixmap(QtGui.QPixmap("../res/sprites/cards/QD.png"))
        self.communityCard3.setObjectName("communityCard3")
        self.communityCard4 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard4.setGeometry(QtCore.QRect(890, 370, 88, 124))
        self.communityCard4.setText("")
        self.communityCard4.setPixmap(QtGui.QPixmap("../res/sprites/cards/JD.png"))
        self.communityCard4.setObjectName("communityCard4")
        self.communityCard5 = QtWidgets.QLabel(self.centralwidget)
        self.communityCard5.setGeometry(QtCore.QRect(1020, 370, 88, 124))
        self.communityCard5.setText("")
        self.communityCard5.setPixmap(QtGui.QPixmap("../res/sprites/cards/TD.png"))
        self.communityCard5.setObjectName("communityCard5")
        self.tableSprite = QtWidgets.QLabel(self.centralwidget)
        self.tableSprite.setGeometry(QtCore.QRect(5, 40, 1521, 771))
        self.tableSprite.setAutoFillBackground(False)
        self.tableSprite.setText("")
        self.tableSprite.setPixmap(QtGui.QPixmap("../res/sprites/table/poker_table_top.png"))
        self.tableSprite.setObjectName("tableSprite")
        self.playerCard1 = QtWidgets.QLabel(self.centralwidget)
        self.playerCard1.setGeometry(QtCore.QRect(700, 600, 88, 124))
        self.playerCard1.setText("")
        self.playerCard1.setPixmap(QtGui.QPixmap("../res/sprites/cards/AC.png"))
        self.playerCard1.setObjectName("playerCard1")
        self.playerCard2 = QtWidgets.QLabel(self.centralwidget)
        self.playerCard2.setGeometry(QtCore.QRect(800, 600, 88, 124))
        self.playerCard2.setText("")
        self.playerCard2.setPixmap(QtGui.QPixmap("../res/sprites/cards/2C.png"))
        self.playerCard2.setObjectName("playerCard2")
        self.playerChipsLabel = QtWidgets.QLabel(self.centralwidget)
        self.playerChipsLabel.setGeometry(QtCore.QRect(700, 560, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.playerChipsLabel.setFont(font)
        self.playerChipsLabel.setStyleSheet("font: 14pt \"Georgia\";")
        self.playerChipsLabel.setObjectName("playerChipsLabel")
        self.opponentChipsLabel = QtWidgets.QLabel(self.centralwidget)
        self.opponentChipsLabel.setGeometry(QtCore.QRect(700, 40, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        self.opponentChipsLabel.setFont(font)
        self.opponentChipsLabel.setStyleSheet("font: 12pt \"Georgia\";")
        self.opponentChipsLabel.setObjectName("opponentChipsLabel")
        self.opponentLastActionLabel = QtWidgets.QLabel(self.centralwidget)
        self.opponentLastActionLabel.setGeometry(QtCore.QRect(700, 20, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        self.opponentLastActionLabel.setFont(font)
        self.opponentLastActionLabel.setStyleSheet("font: 12pt \"Georgia\";")
        self.opponentLastActionLabel.setObjectName("opponentLastActionLabel")
        self.dealerButton = QtWidgets.QLabel(self.centralwidget)
        self.dealerButton.setGeometry(QtCore.QRect(630, 5, 69, 68))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dealerButton.setFont(font)
        self.dealerButton.setText("")
        self.dealerButton.setPixmap(QtGui.QPixmap("../res/sprites/chips/Dealer_Chip.png"))
        self.dealerButton.setObjectName("dealerButton")
        self.dealerLabel = QtWidgets.QLabel(self.centralwidget)
        self.dealerLabel.setGeometry(QtCore.QRect(637, 25, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.dealerLabel.setFont(font)
        self.dealerLabel.setStyleSheet("font: 10pt \"Georgia\";")
        self.dealerLabel.setObjectName("dealerLabel")
        self.potLabel = QtWidgets.QLabel(self.centralwidget)
        self.potLabel.setGeometry(QtCore.QRect(310, 400, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.potLabel.setFont(font)
        self.potLabel.setStyleSheet("font: 17pt \"Georgia\";")
        self.potLabel.setObjectName("potLabel")
        self.raisePotButton = QtWidgets.QPushButton(self.centralwidget)
        self.raisePotButton.setEnabled(True)
        self.raisePotButton.setGeometry(QtCore.QRect(510, 790, 130, 40))
        self.raisePotButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.raisePotButton.setObjectName("raisePotButton")
        self.raise3bbButton = QtWidgets.QPushButton(self.centralwidget)
        self.raise3bbButton.setGeometry(QtCore.QRect(670, 790, 130, 40))
        self.raise3bbButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.raise3bbButton.setObjectName("raise3bbButton")
        self.raise2PotButton = QtWidgets.QPushButton(self.centralwidget)
        self.raise2PotButton.setEnabled(True)
        self.raise2PotButton.setGeometry(QtCore.QRect(830, 790, 130, 40))
        self.raise2PotButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.raise2PotButton.setObjectName("raise2PotButton")
        self.allinButton = QtWidgets.QPushButton(self.centralwidget)
        self.allinButton.setGeometry(QtCore.QRect(990, 790, 130, 40))
        self.allinButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.allinButton.setObjectName("allinButton")
        self.callButton = QtWidgets.QPushButton(self.centralwidget)
        self.callButton.setGeometry(QtCore.QRect(510, 790, 130, 40))
        self.callButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.callButton.setObjectName("callButton")
        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setGeometry(QtCore.QRect(670, 790, 130, 40))
        self.checkButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.checkButton.setObjectName("checkButton")
        self.raiseButton = QtWidgets.QPushButton(self.centralwidget)
        self.raiseButton.setGeometry(QtCore.QRect(830, 790, 130, 40))
        self.raiseButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.raiseButton.setObjectName("raiseButton")
        self.foldButton = QtWidgets.QPushButton(self.centralwidget)
        self.foldButton.setGeometry(QtCore.QRect(990, 790, 130, 40))
        self.foldButton.setStyleSheet("font: 12pt \"Georgia\";")
        self.foldButton.setObjectName("foldButton")
        self.tableSprite.raise_()
        self.communityCard2.raise_()
        self.communityCard1.raise_()
        self.communityCard3.raise_()
        self.communityCard4.raise_()
        self.communityCard5.raise_()
        self.communityCardsLabel.raise_()
        self.playerCard1.raise_()
        self.playerCard2.raise_()
        self.playerChipsLabel.raise_()
        self.opponentChipsLabel.raise_()
        self.opponentLastActionLabel.raise_()
        self.dealerButton.raise_()
        self.dealerLabel.raise_()
        self.potLabel.raise_()
        self.raisePotButton.raise_()
        self.raise3bbButton.raise_()
        self.raise2PotButton.raise_()
        self.allinButton.raise_()
        self.callButton.raise_()
        self.checkButton.raise_()
        self.raiseButton.raise_()
        self.foldButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1680, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.communityCardsLabel.setText(_translate("MainWindow", "Community Cards"))
        self.playerChipsLabel.setText(_translate("MainWindow", "Your Chips: $500"))
        self.opponentChipsLabel.setText(_translate("MainWindow", "Opponent Chips: $500"))
        self.opponentLastActionLabel.setText(_translate("MainWindow", "Last Action: CHECK"))
        self.dealerLabel.setText(_translate("MainWindow", "Dealer"))
        self.potLabel.setText(_translate("MainWindow", "POT: $0"))
        self.raisePotButton.setText(_translate("MainWindow", "RAISE POT"))
        self.raise3bbButton.setText(_translate("MainWindow", "RAISE 3BB"))
        self.raise2PotButton.setText(_translate("MainWindow", "RAISE 2 POT"))
        self.allinButton.setText(_translate("MainWindow", "ALL IN"))
        self.callButton.setText(_translate("MainWindow", "CALL"))
        self.checkButton.setText(_translate("MainWindow", "CHECK"))
        self.raiseButton.setText(_translate("MainWindow", "RAISE"))
        self.foldButton.setText(_translate("MainWindow", "FOLD"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
