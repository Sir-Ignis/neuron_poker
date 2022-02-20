import sys
from GUI.HUTHP import Ui_MainWindow
from PyQt6 import QtWidgets, QtGui
from enum import Enum

file_path = "/home/daniel/Project/neuron_poker/GUI/action.txt"
path = "/home/daniel/Project/neuron_poker/GUI/resources/SBS - 2D Poker Pack/Top-Down/Cards/individual/"
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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableSprite.setPixmap(QtGui.QPixmap("/home/daniel/Project/neuron_poker/GUI/resources/table_top_empty.png"))
        self.ui.checkButton.clicked.connect(self.checkAction)
        self.ui.callButton.clicked.connect(self.callAction)
        self.ui.foldButton.clicked.connect(self.foldAction)

    def connectButtons(self):
        self.ui.checkButton.clicked.connect(self.checkAction)
        self.ui.callButton.clicked.connect(self.callAction)
        self.ui.foldButton.clicked.connect(self.foldAction)

    def renderTableCards(self, community_cards):
        self.ui.communityCard1.clear()
        self.ui.communityCard2.clear()
        self.ui.communityCard3.clear()
        self.ui.communityCard4.clear()
        self.ui.communityCard5.clear()

        for i in range(len(community_cards)):
            card = community_cards[i]
            if i == 0:
                self.ui.communityCard1.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 1:
                self.ui.communityCard2.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 2:
                self.ui.communityCard3.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 3:
                self.ui.communityCard4.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))
            elif i == 4:
                self.ui.communityCard5.setPixmap(QtGui.QPixmap(path+str(card)+'.png'))

    def renderHandCards(self, hand):
        self.ui.playerCard1.setPixmap(QtGui.QPixmap(path+hand[0]+'.png'))
        self.ui.playerCard2.setPixmap(QtGui.QPixmap(path+hand[1]+'.png'))

    def renderChipAmounts(self, playerChips, opponentChips):
        self.ui.playerChipsLabel.setText("Player Chips: $"+str(playerChips))
        self.ui.opponentChipsLabel.setText( "Opponent Chips: $"+str(opponentChips))

    def renderLastAction(self, last_action):
        if not(last_action == None):
            self.ui.opponentLastActionLabel.setText("Last Action: "+last_action.name)
        else:
            self.ui.opponentLastActionLabel.setText("")
    
    def renderActionButtons(self, legal_moves):
        raise_3bb = False
        raise_pot = False
        raise_2pot = False
        all_in = False

        legal_values = [e.value for e in legal_moves]

        if Action.CHECK.value in legal_values:
            self.ui.checkButton.show()
        else:
            self.ui.checkButton.hide()
        
        if Action.CALL.value in legal_values:
            self.ui.callButton.show()
        else:
            self.ui.callButton.hide()
        
        if Action.RAISE_3BB.value in legal_values:
            raise_3bb = True
        if Action.RAISE_POT.value in legal_values:
            raise_pot = True
        if Action.RAISE_2POT.value in legal_values:
            raise_2pot = True
        if Action.ALL_IN.value in legal_values:
            all_in = True

        if raise_3bb or raise_pot or raise_2pot or all_in:
            self.ui.raiseButton.show()
        else:
            self.ui.raiseButton.hide()

        return [raise_3bb, raise_pot, raise_2pot, all_in]


    def write_action_to_file(self, action):
        with open(file_path,'r+') as myfile:
            data = myfile.read()
            myfile.seek(0)
            myfile.write(action)
            myfile.truncate()

    def callAction(self):
        print('called callAction')
        self.write_action_to_file(str(Action.CALL.value))
        self.close()
    
    def checkAction(self):
        print('called checkAction')
        self.write_action_to_file(str(Action.CHECK.value))
        self.close()
    
    def foldAction(self):
        print('called foldAction')
        self.write_action_to_file(str(Action.FOLD.value))
        self.close()


"""
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
"""