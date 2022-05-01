import sys 
import time
import os
import ast 

from enum import Enum

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QProcess, QByteArray, pyqtSlot, QEventLoop, QTimer

from main_menu import Menu_MainWindow # menu UI
from help_menu import Help_MainWindow 
from options_menu import Options_MainWindow 
from HUTHP import Ui_MainWindow # main UI for game


PROJECT_PATH = '/Users/daniel/Documents/Poker Project/neuron_poker/neuron_poker' 
# replace with where your neuron_poker git is stored
RESOURCES_PATH = PROJECT_PATH+'/GUI/res/'
SPRITES_PATH = RESOURCES_PATH+'sprites/'
CARD_SPRITES_PATH = SPRITES_PATH+'cards/'
CHIP_SPRITES_PATH = SPRITES_PATH+'chips/'
TABLE_SPRITES_PATH = SPRITES_PATH+'table/'
ICONS_PATH = SPRITES_PATH+'icons/'

#these strings are used to parse log data from the process
#better method would use threads instead of processes see dissertation for reason
#why a process was chosen instead of running it as multiple processes
LOG_ACTION_STRING = 'Choose action with number: '
LOG_DEALER_POS_STRING = 'Dealer is at position'
LOG_GUI_INFO_STRING = 'GUI INFO: '
LOG_NEW_HAND_STRING = 'INFO - Starting new hand.'
LOG_OPP_CARDS_STRING = 'INFO - Opponent cards: '
LOG_WON_STRING0 = 'INFO - Player 0 won:' #you won
LOG_WON_STRING1 = 'INFO - Player 1 won: ' #bot won
LOG_TOTAL_WIN_STRING = 'INFO - Total winnings = '

PLAY_STEP_LENGTH = 1000 # used in process start command to determine selfplay step length
MODEL_TYPE_EQUITY = "EQUITY" # equity uses the model when the agent was trained agains the equity agent
MODEL_TYPE_RANDOM = "RANDOM" # random uses the model when the agent was trained against a random agent
MODEL_TYPE = MODEL_TYPE_EQUITY # used in process command to determine the selfplay model used

AGENT_CARDS_SHOWN = False #true when keras-rl's cards are shown on the table
WAIT_TIME = 10000 #time to display cards and win message for
IDLE_PERIOD = False#true when win message hasn't been cleared else false
COMMUNITY_CARDS = 0

os.chdir(PROJECT_PATH)

class Action(Enum):
    NONE = -1
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
        # setup main_menu ui
        self.home()
        self.showMaximized()
        self.tmp_data = QByteArray() #to hold data when idling to correctly render cards
        self.tmp_log_action_string_shown = False

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
            steps = f"--steps={PLAY_STEP_LENGTH}"
            model = MODEL_TYPE.lower()
            if (not(MODEL_TYPE == MODEL_TYPE_RANDOM)): 
                model = "--name=dqn1"
            else:
                model = f"--name={model}"
            print(model)
            self.p.start("python", ['-u','main.py','selfplay','dqn_play_human',model,'-c',steps,'--render'])

    def setup_main_ui(self):
        self.showFullScreen()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("NLHUTH Poker Bot")
        self.renderSprites()
        self.toggle_buttons(False)
        self.connect_buttons()

    def setup_help(self):
        self.ui = Help_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.ui.backButton.clicked.connect(self.home)

    def setup_options(self):
        self.ui = Options_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.ui.infoIcon.setPixmap(QtGui.QPixmap(ICONS_PATH+'ic_info_orange.png'))
        self.ui.backButton.clicked.connect(self.home)
        self.ui.randomRBtn.toggled.connect(lambda:self.change_model_type(self.ui.randomRBtn))
        self.ui.equityRBtn.toggled.connect(lambda:self.change_model_type(self.ui.equityRBtn))
        self.ui.shortRBtn.toggled.connect(lambda:self.change_num_runs(self.ui.shortRBtn))
        self.ui.longRBtn.toggled.connect(lambda:self.change_num_runs(self.ui.longRBtn))

    def home(self):
        self.p = None
        self.ui = Menu_MainWindow()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.start_main) # start poker bot
        self.ui.helpButton.clicked.connect(self.setup_help)
        self.ui.optionsButton.clicked.connect(self.setup_options)
        self.ui.pokerMenuSprite.setPixmap(QtGui.QPixmap(ICONS_PATH+'title_screen_poker_art.png'))
        self.data = []
        self.raise_btns = []
        self.log_actions = 0 # when log action string shown this is incremented


    """ changes the number of runs that the poker bot is started with depending on
        which radio button was selected in the options menu, default is short - 1000 step run - 
        and long being 10000 steps """
    def change_num_runs(self,b):
        global PLAY_STEP_LENGTH
        if b.isChecked():
            if b.text() == "Short":
                PLAY_STEP_LENGTH = 1000
            elif b.text() == "Long":
                PLAY_STEP_LENGTH = 10000
            print(f"Changed episode length to {PLAY_STEP_LENGTH}")


    """ changes the model type depending on the selected radio button
        see load function in keras agent to see how loading is done """
    def change_model_type(self,b):
        global MODEL_TYPE
        if b.isChecked():
            if b.text() == "Random" and b.isChecked():
                MODEL_TYPE = MODEL_TYPE_RANDOM
            elif b.text() == "Equity" and b.isChecked():
                MODEL_TYPE = MODEL_TYPE_EQUITY
            print(f"Changed model type to {MODEL_TYPE}")

    def connect_buttons(self):
        self.ui.callButton.clicked.connect(self.callAction)
        self.ui.checkButton.clicked.connect(self.checkAction)
        self.ui.raiseButton.clicked.connect(self.raiseAction)
        self.ui.foldButton.clicked.connect(self.foldAction)

        self.ui.raise3bbButton.clicked.connect(self.raise3bbAction)
        self.ui.raise2PotButton.clicked.connect(self.raise2PotAction)
        self.ui.raisePotButton.clicked.connect(self.raisePotAction)
        self.ui.allinButton.clicked.connect(self.allinAction)

    def toggle_buttons(self, enable=True):
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

    def parseData(self, data, action_string_shown):
        """ likely cause of crashing in this function, perhaps using threads
            instead of running the main program as a process would prevent random
            crashes? """ 
        info = data

        if action_string_shown:
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

        """
        TODO: 
        should modify this to make it so its not using coordinates
        probable solution: change layout to include multiple containers
        """

        player_btn_label_coords = (912, 640)
        player_btn_coords = (900, 620)
        p = (player_btn_label_coords, player_btn_coords)

        agent_btn_label_coords = (642, 25)
        agent_btn_coords = (630, 5)
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
        data = self.p.readAllStandardOutput()
        data_ = QByteArray(data)

        log_action_string_shown = False
        if(data.contains(LOG_ACTION_STRING.encode("utf8"))):
            log_action_string_shown = True
            if not IDLE_PERIOD:
                self.toggle_buttons(True)
        if data_.contains(LOG_GUI_INFO_STRING.encode("utf8")):
            if not IDLE_PERIOD:
                self.parseData(data_,log_action_string_shown)
            else:
                self.tmp_data = QByteArray(data)
                self.tmp_log_action_string_shown = log_action_string_shown
        if data_.contains(LOG_OPP_CARDS_STRING.encode("utf8")):
            self.show_agent_cards(data_)
        if data_.contains(LOG_WON_STRING0.encode("utf8")) or \
           data_.contains(LOG_WON_STRING1.encode("utf8")):
               self.display_won_msg(data_)
        if not IDLE_PERIOD and data_.contains(LOG_NEW_HAND_STRING.encode("utf8")):
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
        """ renders the appropriate action buttons depending on the actions in
        legal_Action_values """
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
        table_top_path = TABLE_SPRITES_PATH+"poker_table_top.png"
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
        global COMMUNITY_CARDS
        COMMUNITY_CARDS = len(table_cards)
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

    def clear_community_cards(self):
        self.ui.communityCard1.setPixmap(QtGui.QPixmap())
        self.ui.communityCard2.setPixmap(QtGui.QPixmap())
        self.ui.communityCard3.setPixmap(QtGui.QPixmap())
        self.ui.communityCard4.setPixmap(QtGui.QPixmap())
        self.ui.communityCard5.setPixmap(QtGui.QPixmap())

    def clear_table(self):
        self.clear_community_cards()

        self.ui.playerCard1.setPixmap(QtGui.QPixmap())
        self.ui.playerCard2.setPixmap(QtGui.QPixmap())

    """ shows keras-rl's hand (2 cards) """
    def show_agent_cards(self, info):
        info_str = str(info, "utf8")
        info_str = info_str.replace(LOG_OPP_CARDS_STRING,'')
        hand = []
        try:
            hand = ast.literal_eval(info_str)
        except Exception as e:
            print(e)
        else:
            print("hand: "+str(hand))
            card1 = QtGui.QPixmap(CARD_SPRITES_PATH+hand[0]+'.png')
            card2 = QtGui.QPixmap(CARD_SPRITES_PATH+hand[1]+'.png')
            self.ui.oppHandCard1.setPixmap(card1)
            self.ui.oppHandCard2.setPixmap(card2)
            if not card1.isNull() and not(card2.isNull()):
                self.idle_period()
                QTimer.singleShot(WAIT_TIME, self.clear_agent_cards)
        
    def clear_agent_cards(self):
        self.ui.oppHandCard1.setPixmap(QtGui.QPixmap())
        self.ui.oppHandCard2.setPixmap(QtGui.QPixmap())
    
    def idle_period(self):
        #disable the buttons until win message is cleared
        #prevents someone from spamming the buttons before concluding who run the round
        global IDLE_PERIOD
        IDLE_PERIOD = True
        self.toggle_buttons(False)
    

    def display_won_msg(self, info):
        info_str = str(info, "utf8")
        if info.contains(LOG_WON_STRING1.encode("utf8")):
            
           if COMMUNITY_CARDS == 0: 
               self.ui.winnerLabel.setText('Bot won because you folded')
               self.idle_period()
           else:
               info_str = info_str.replace(LOG_WON_STRING1,'')
               info_str = info_str.replace(LOG_TOTAL_WIN_STRING,'Bot won: $')
               self.ui.winnerLabel.setText('Bot won with: '+info_str)
        else:
           if COMMUNITY_CARDS == 0: 
               self.ui.winnerLabel.setText('You won because the bot folded')
               self.idle_period()
           else:
               info_str = info_str.replace(LOG_WON_STRING0,'')
               info_str = info_str.replace(LOG_TOTAL_WIN_STRING,'You won: $')
               self.ui.winnerLabel.setText('You won with: '+info_str)
    
        QTimer.singleShot(WAIT_TIME, self.clear_won_msg)

    def clear_won_msg(self):
        self.ui.winnerLabel.clear()
        global IDLE_PERIOD
        global COMMUNITY_CARDS
        IDLE_PERIOD = False
        COMMUNITY_CARDS = 0
        self.clear_community_cards()
        self.toggle_buttons(True)
        #see parseData
        data = self.tmp_data
        log_action_string_shown = self.tmp_log_action_string_shown
        self.parseData(data,log_action_string_shown)
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
