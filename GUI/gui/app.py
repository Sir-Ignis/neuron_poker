import sys 
import time
import os
import ast 

from enum import Enum

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QProcess, QByteArray, pyqtSlot

from menu import Menu_MainWindow
from HUTHP import Ui_MainWindow


PROJECT_PATH = '/home/daniel/Project/neuron_poker/' # replace with where your neuron_poker git is stored
RESOURCES_PATH = PROJECT_PATH+'/GUI/res/'
SPRITES_PATH = RESOURCES_PATH+'sprites/'
CARD_SPRITES_PATH = SPRITES_PATH+'cards/'
CHIP_SPRITES_PATH = SPRITES_PATH+'chips/'
TABLE_SPRITES_PATH = SPRITES_PATH+'table/'

LOG_ACTION_STRING = 'Choose action with number: '
LOG_DEALER_POS_STRING = 'Dealer is at position'
LOG_GUI_INFO_STRING = 'GUI INFO: '
LOG_NEW_HAND_STRING = 'INFO - Starting new hand.'

os.chdir(PROJECT_PATH)

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
        self.ui.startButton.clicked.connect(self.start_main)
        self.data = []
        self.raise_btns = []

    def closeEvent(self, event):
        if not(self.p == None):
            print('Terminating process due to window close...')
            self.p.terminate()
            self.p.waitForFinished()
            self.p = None
        event.accept()

    def start_main(self):
        self.setup_main_ui()
        self.start_process()

    def start_process(self):
        if self.p is None:
            print("Starting neuron_poker")
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.finished.connect(self.process_finished)  # Clean up once
            self.p.start("python", ['-u','main.py','selfplay','dqn_play_human','-c','--steps=1000','--render'])

    def setup_main_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.renderSprites()
        self.toggle_buttons(False)
        self.connect_buttons()

    def connect_buttons(self):
        self.ui.callButton.clicked.connect(self.callAction)
        self.ui.checkButton.clicked.connect(self.checkAction)
        self.ui.raiseButton.clicked.connect(self.raiseAction)
        self.ui.foldButton.clicked.connect(self.foldAction)

        self.ui.raise3bbButton.clicked.connect(self.raise3bbAction)
        self.ui.raise2PotButton.clicked.connect(self.raise2PotAction)
        self.ui.raisePotButton.clicked.connect(self.raisePotAction)
        self.ui.allinButton.clicked.connect(self.allinAction)

    def toggle_buttons(self, enable=False):
        self.ui.callButton.setEnabled(enable)
        self.ui.checkButton.setEnabled(enable)
        self.ui.foldButton.setEnabled(enable)
        self.ui.raiseButton.setEnabled(enable)

    def hide_buttons(self):
        self.ui.checkButton.hide()
        self.ui.callButton.hide()
        self.ui.raiseButton.hide()
        self.ui.foldButton.hide()

    def hide_raise_buttons(self):
        self.ui.raise3bbButton.hide()
        self.ui.raise3bbButton.lower()
        self.ui.raise2PotButton.hide()
        self.ui.raise2PotButton.lower()
        self.ui.raisePotButton.hide()
        self.ui.raisePotButton.lower()
        self.ui.allinButton.hide()
        self.ui.allinButton.lower()

    def parseData(self, data):
        info = data
        idx = data.indexOf(LOG_ACTION_STRING.encode("utf8"))
        info.truncate(idx)
        
        info_str = str(info, "utf8")
        info_str = info_str.replace(LOG_GUI_INFO_STRING,'')
        info_dict = dict()
        try:
            info_dict = ast.literal_eval(info_str)
        except Exception as e:
            print(e)

        if 'legal_moves' in info_dict:
            self.raise_btns = self.renderActionButtons(info_dict['legal_moves'])
            self.render_table(info_dict)
        else:
            print('legal moves key not in info_dict!')
            print('Likely cause: you spammed the buttons...')
            self.close()

    def renderDealerButton(self, data):
        info = data
        tmp = str(data,'utf8')
        idx = data.indexOf(LOG_DEALER_POS_STRING.encode("utf8"))
        info = info.sliced(idx)
        dealer_str = str(info, "utf8")
        dealer_str = dealer_str.split('\n')[0][-1]
        dealer_pos = int(dealer_str)

        player_btn_label_coords = (310, 550)
        player_btn_coords = (305, 580)
        p = (player_btn_label_coords, player_btn_coords)

        agent_btn_label_coords = (332, 20)
        agent_btn_coords = (330, 40)
        a = (agent_btn_label_coords, agent_btn_coords)

        # player is dealer
        if dealer_pos == 0:
            self.ui.dealerLabel.move(p[0][0], p[0][1])
            self.ui.dealerButton.move(p[1][0], p[1][1])
        else:
            self.ui.dealerLabel.move(a[0][0], a[0][1])
            self.ui.dealerButton.move(a[1][0], a[1][1])

    def handle_stdout(self):
        """ updates gui based on info read from process, i.e. info read from the terminal"""
        print('called stdout')
        self.toggle_buttons(False)

        data = self.p.readAllStandardOutput()
        data_ = QByteArray(data)

        if(data.contains(LOG_ACTION_STRING.encode("utf8"))):
            self.toggle_buttons(True)
        if data_.contains(LOG_GUI_INFO_STRING.encode("utf8")):
            self.parseData(data_)
        if data_.contains(LOG_NEW_HAND_STRING.encode("utf8")):
            self.clear_table()
        if data_.contains(LOG_DEALER_POS_STRING.encode("utf8")):
            self.renderDealerButton(data_)
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
        s = str(Action.CALL.value) + "\n"
        self.p.write(s.encode())
        
    @pyqtSlot()
    def checkAction(self):
        s = str(Action.CHECK.value) + "\n"
        self.p.write(s.encode("utf8"))
        
    @pyqtSlot()
    def foldAction(self):
        s = str(Action.FOLD.value) + "\n"
        self.p.write(s.encode("utf8"))

    @pyqtSlot()
    def raiseAction(self):
        self.render_raise_btns()
        self.hide_buttons()

    @pyqtSlot()
    def raise3bbAction(self):
        s = str(Action.RAISE_3BB.value) + "\n"
        self.p.write(s.encode("utf8"))
        self.hide_raise_buttons()
    
    @pyqtSlot()
    def raisePotAction(self):
        s = str(Action.RAISE_POT.value) + "\n"
        self.p.write(s.encode("utf8"))
        self.hide_raise_buttons()

    @pyqtSlot()
    def raise2PotAction(self):
        s = str(Action.RAISE_2POT.value) + "\n"
        self.p.write(s.encode("utf8"))
        self.hide_raise_buttons()

    @pyqtSlot()
    def allinAction(self):
        s = str(Action.ALL_IN.value) + "\n"
        self.p.write(s.encode("utf8"))
        self.hide_raise_buttons()

    def renderActionButtons(self, legal_action_values):
        raise_3bb = False
        raise_pot = False
        raise_2pot = False
        all_in = False

        legal_values = legal_action_values

        if Action.FOLD.value in legal_values:
            self.ui.foldButton.show()
            self.ui.foldButton.raise_()
        else:
            self.ui.foldButton.hide()
        if Action.CHECK.value in legal_values:
            self.ui.checkButton.show()
            self.ui.checkButton.raise_()
        else:
            self.ui.checkButton.hide()
        
        if Action.CALL.value in legal_values:
            self.ui.callButton.show()
            self.ui.callButton.raise_()
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
            self.ui.checkButton.raise_()
        else:
            self.ui.raiseButton.hide()

        self.hide_raise_buttons()
        return [raise_3bb, raise_pot, raise_2pot, all_in]

    def render_raise_btns(self):
        if self.raise_btns[0]:
            self.ui.raise3bbButton.show()
        else:
            self.ui.raise3bbButton.hide()
        if self.raise_btns[1]:
            self.ui.raisePotButton.show()
        else:
            self.ui.raisePotButton.hide()
        if self.raise_btns[2]:
            self.ui.raise2PotButton.show()
        else:
            self.ui.raise2PotButton.hide()
        if self.raise_btns[3]:
            self.ui.allinButton.show()
        else:
            self.ui.allinButton.hide()
        
    def renderSprites(self):
        table_top_path = TABLE_SPRITES_PATH+"table_top_empty.png"
        dealer_btn_path = CHIP_SPRITES_PATH+"Dealer_Chip.png"
        self.ui.tableSprite.setPixmap(QtGui.QPixmap(table_top_path))
        self.ui.dealerButton.setPixmap(QtGui.QPixmap(dealer_btn_path))

    def render_table(self, info_dict): 
        sprite_path = CARD_SPRITES_PATH
        d = info_dict

        self.ui.potLabel.setText("Pot: $"+str(d['pot']))
        self.ui.opponentLastActionLabel.setText("Last Action: "+self.action_val_to_string(d['last_action']))
        self.ui.opponentChipsLabel.setText("Opponent Chips: $"+ str(d['opponent_stack']))
        table_cards = d['table_cards']
        for i in range(len(table_cards)):
            if i == 0:
                self.ui.communityCard1.setPixmap(QtGui.QPixmap(sprite_path+table_cards[0]+'.png'))
            if i == 1:
                self.ui.communityCard2.setPixmap(QtGui.QPixmap(sprite_path+table_cards[1]+'.png'))
            if i == 2:
                self.ui.communityCard3.setPixmap(QtGui.QPixmap(sprite_path+table_cards[2]+'.png'))
            if i == 3:
                self.ui.communityCard4.setPixmap(QtGui.QPixmap(sprite_path+table_cards[3]+'.png'))
            if i == 4:
                self.ui.communityCard5.setPixmap(QtGui.QPixmap(sprite_path+table_cards[4]+'.png'))
        self.ui.playerChipsLabel.setText("Player Chips: $"+str(d['player_stack']))
        player_cards = d['player_cards']
        self.ui.playerCard1.setPixmap(QtGui.QPixmap(sprite_path+player_cards[0]+'.png'))
        self.ui.playerCard2.setPixmap(QtGui.QPixmap(sprite_path+player_cards[1]+'.png'))


    def action_val_to_string(self, action_value):
        return Action(action_value).name.replace('_',' ')

    def clear_table(self):
        self.ui.communityCard1.setPixmap(QtGui.QPixmap())
        self.ui.communityCard2.setPixmap(QtGui.QPixmap())
        self.ui.communityCard3.setPixmap(QtGui.QPixmap())
        self.ui.communityCard4.setPixmap(QtGui.QPixmap())
        self.ui.communityCard5.setPixmap(QtGui.QPixmap())

        self.ui.playerCard1.setPixmap(QtGui.QPixmap())
        self.ui.playerCard2.setPixmap(QtGui.QPixmap())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
