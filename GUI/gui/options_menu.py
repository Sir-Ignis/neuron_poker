# Form implementation generated from reading ui file 'options_menu.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Options_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 762)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(120, 450, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.backButton.setFont(font)
        self.backButton.setStyleSheet("font: 13pt \"Arial\";")
        self.backButton.setObjectName("backButton")
        self.infoIcon = QtWidgets.QLabel(self.centralwidget)
        self.infoIcon.setGeometry(QtCore.QRect(120, 320, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.infoIcon.setFont(font)
        self.infoIcon.setStyleSheet("font: 13pt \"Arial\";")
        self.infoIcon.setText("")
        self.infoIcon.setPixmap(QtGui.QPixmap("../res/sprites/icons/ic_info.png"))
        self.infoIcon.setObjectName("infoIcon")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 320, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label.setFont(font)
        self.label.setStyleSheet("font: 13pt \"Arial\";")
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(350, 190, 291, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.randomRBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.randomRBtn.setFont(font)
        self.randomRBtn.setStyleSheet("font: 13pt \"Arial\";")
        self.randomRBtn.setObjectName("randomRBtn")
        self.horizontalLayout.addWidget(self.randomRBtn)
        self.equityRBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.equityRBtn.setFont(font)
        self.equityRBtn.setStyleSheet("font: 13pt \"Arial\";")
        self.equityRBtn.setObjectName("equityRBtn")
        self.horizontalLayout.addWidget(self.equityRBtn)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(350, 100, 291, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.shortRBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.shortRBtn.setFont(font)
        self.shortRBtn.setStyleSheet("font: 13pt \"Arial\";")
        self.shortRBtn.setObjectName("shortRBtn")
        self.horizontalLayout_3.addWidget(self.shortRBtn)
        self.longRBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.longRBtn.setFont(font)
        self.longRBtn.setStyleSheet("font: 13pt \"Arial\";")
        self.longRBtn.setObjectName("longRBtn")
        self.horizontalLayout_3.addWidget(self.longRBtn)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(120, 100, 231, 183))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.modelText = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.modelText.setFont(font)
        self.modelText.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"font: 13pt \"Arial\";\n"
"")
        self.modelText.setObjectName("modelText")
        self.verticalLayout.addWidget(self.modelText)
        self.runLenText = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.runLenText.setFont(font)
        self.runLenText.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"font: 13pt \"Arial\";")
        self.runLenText.setObjectName("runLenText")
        self.verticalLayout.addWidget(self.runLenText)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NLHUTH Poker Bot"))
        self.backButton.setText(_translate("MainWindow", "Back"))
        self.label.setText(_translate("MainWindow", "Hover over bold text for extra info"))
        self.randomRBtn.setText(_translate("MainWindow", "Random"))
        self.equityRBtn.setText(_translate("MainWindow", "Equity"))
        self.shortRBtn.setText(_translate("MainWindow", "Short"))
        self.longRBtn.setText(_translate("MainWindow", "Long"))
        self.modelText.setToolTip(_translate("MainWindow", "<html><head/><body><p style=\"color:white; font-family:\'Arial\';\">Bot model type: equity is more intelligent and random is less intelligent (see help for more info)</p></body></html>"))
        self.modelText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:696;\">Opponent Model:</span></p></body></html>"))
        self.runLenText.setToolTip(_translate("MainWindow", "<html><head/><body><p style=\"color:white; font-family:\'Arial\';\">Run length, short is 1000 steps and long is 10000 steps (see help for more info)</p></body></html>"))
        self.runLenText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:696;\">Run length</span><span style=\" font-family:\'Sans Serif\'; font-size:12pt;\">:</span></p></body></html>"))
