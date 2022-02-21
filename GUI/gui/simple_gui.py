import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

os.chdir("/home/daniel/Project/neuron_poker")

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._textedit = QtWidgets.QTextEdit(readOnly=True)
        self._lineedit = QtWidgets.QLineEdit()
        self._pushbutton = QtWidgets.QPushButton("Send")
        self._pushbutton.clicked.connect(self.on_clicked)

        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self._textedit, 0, 0, 1, 2)
        lay.addWidget(self._lineedit, 1, 0)
        lay.addWidget(self._pushbutton, 1, 1)

        self._process = QtCore.QProcess(self)
        self._process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self._process.readyRead.connect(self.on_readReady)

        self._process.start("python", ['-u','main.py','selfplay','dqn_play_human','-c','--steps=1000','--render'])

    def on_readReady(self):
        cursor = self._textedit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(str(self._process.readAll(), "utf-8"))
        self._textedit.ensureCursorVisible()

    def on_clicked(self):
        text = self._lineedit.text() + "\n"
        self._process.write(text.encode())


if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"


    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec())