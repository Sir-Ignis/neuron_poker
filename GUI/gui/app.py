import sys 
import time
import os

from enum import Enum

from PyQt6 import QtWidgets
from PyQt6.QtCore import QProcess, pyqtSlot

from menu import Menu_MainWindow
from HUTHP import Ui_MainWindow

os.chdir("/home/daniel/Project/neuron_poker")

class Action(Enum):
    """Allowed actions"""

    FOLD = 0
    CHECK = 1
    CALL = 2
    RAISE_3BB = 3
    RAISE_HALF_POT = 3
    RAISE_POT = 4
    RAISE_2POT = 5
    ALL_IN = 6
    SMALL_BLIND = 7
    BIG_BLIND = 8

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.p = None

        self.ui = Menu_MainWindow()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.start_process)

    def start_process(self):
        if self.p is None:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.connect_buttons()
            print("Starting neuron_poker")
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.finished.connect(self.process_finished)  # Clean up once
            self.p.start("python", ['-u','main.py','selfplay','dqn_play_human','-c','--steps=1000','--render'])
    
    def connect_buttons(self):
        self.ui.callButton.clicked.connect(self.callAction)
        self.ui.checkButton.clicked.connect(self.checkAction)
        self.ui.foldButton.clicked.connect(self.foldAction)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)

    def process_finished(self):
        print("Process finished.")
        self.p = None

    @pyqtSlot()
    def callAction(self):
        print('called callAction')
        self.p.write(str(Action.CALL.value).encode())
        self.p.waitForBytesWritten(-1)
        print('written!')


        
    @pyqtSlot()
    def checkAction(self):
        print('called checkAction')
        self.p.write(str(Action.CHECK.value).encode("utf8"))
        

    @pyqtSlot()
    def foldAction(self):
        print('called foldAction')
        self.p.write(str(Action.FOLD.value).encode("utf8"))

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
