# Form implementation generated from reading ui file 'main_menu.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Menu_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 661)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(410, 280, 131, 41))
        self.startButton.setObjectName("startButton")
        self.optionsButton = QtWidgets.QPushButton(self.centralwidget)
        self.optionsButton.setGeometry(QtCore.QRect(410, 340, 131, 41))
        self.optionsButton.setObjectName("optionsButton")
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(410, 400, 131, 41))
        self.helpButton.setObjectName("helpButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 950, 19))
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
        self.startButton.setText(_translate("MainWindow", "START"))
        self.optionsButton.setText(_translate("MainWindow", "OPTIONS"))
        self.helpButton.setText(_translate("MainWindow", "HELP"))
