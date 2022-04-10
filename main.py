import sys
import itertools
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from playerEntryScreen import Ui_MainWindow
from playActionScreen import Ui_PlayActionWindow
from timerScreen import Ui_MainWindow as TimerWindow
from database.database import database
from countdownTimer import countdownTimer
from udpClient import UdpClient
from udpClient import UdpClientThread

SOCKET_IP = "127.0.0.1"
SOCKET_PORT = 7501

# pyqt/python is stupid and will immediately gc all windows
# so hold a reference to all windows so it knows not to destroy them
main_window = None
#database = database()
#database.open()

class PlayerInfo:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.score = 0

class SplashWindow(QWidget):
    closed = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.setAttribute(Qt.WA_DeleteOnClose)

        # loading image
        self.pixmap = QPixmap("assets/logo.jpg")
        self.pixmap = self.pixmap.scaled(1000, 1000, Qt.KeepAspectRatio)

        # creating label
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)

        # adding image to label
        self.label.setPixmap(self.pixmap)

        self.layout = QGridLayout()

        # adding label to screen
        self.layout.addWidget(self.label, 0, 0)
        self.setStyleSheet("background-color: black;")

        self.setLayout(self.layout)
        self.show()
        
        QTimer.singleShot(3000, self.close_and_show_entry_screen)
    
    def close_and_show_entry_screen(self):
        self.close()
    
    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

class PlayerEntryWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

    def setupUIEvents(self):
        self.ui.startGame.clicked.connect(self.start_countdown_timer)

    def closeEvent(self, event):
        if main_window == self:
            sys.exit()
        else:
            event.accept()
    
    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_F5:
            self.start_countdown_timer()
    
    def get_list_players(self, idx):
        players = []
        for i in range(20):
            name = getattr(self.ui, f"player{i}FirstName_{idx}").toPlainText()
            id = getattr(self.ui, f"player{i}LastName_{idx}").toPlainText()

            if name.strip() == "" or id.strip() == "":
                continue

            player_info = PlayerInfo(name, int(id))
            players.append(player_info)
        
        return players

    def start_countdown_timer(self):
        red_team_players = self.get_list_players(1)
        blue_team_players = self.get_list_players(2)

        game_timer_input_text = self.ui.textEdit.toPlainText()
        
        if game_timer_input_text.isnumeric():
            game_timer_duration = int(game_timer_input_text)
        else:
            # todo: should have some kind of popup if this isn't valid
            game_timer_duration = 60

        show_timer_screen(game_timer_duration, red_team_players, blue_team_players)


class TimerScreen(QMainWindow):
    def __init__(self, game_duration, red_team_players, blue_team_players):
        QMainWindow.__init__(self)
        self.startingGameTimer = countdownTimer(3)
        self.game_duration = game_duration
        self.red_team_players = red_team_players
        self.blue_team_players = blue_team_players


    def endTimerButton(self):
        show_player_entry_screen()
        self.startingGameTimer.reset()
        self.close()


    def setupUIEvents(self):
        self.ui.pushButton.clicked.connect(self.endTimerButton)
        self.startingGameTimer.callback = self.updateTimer
        self.startingGameTimer.start()


    def closeEvent(self, event):
        if main_window == self:
            sys.exit()
        else:
            event.accept()


    def updateTimer(self, secondsLeft):
        if secondsLeft > 10:
            self.ui.textEdit.setPlainText(f"Time Remaining: {countdownTimer.toString(secondsLeft)}")
        elif secondsLeft > 0:
            self.ui.textEdit.setPlainText(f"WARNING!\nTime Remaining: {countdownTimer.toString(secondsLeft)}")
        else:
            show_play_action_screen(self.game_duration, self.red_team_players, self.blue_team_players)
            self.close()


class PlayActionScreen(QMainWindow):
    def __init__(self, timer_duration, red_team_players, blue_team_players):
        QMainWindow.__init__(self)
        self.startingGameTimer = countdownTimer(timer_duration)
        self.red_team_players = red_team_players
        self.blue_team_players = blue_team_players
        self.player_id_to_info = {}
        self.player_id_to_row = {}
        self.player_id_to_table_widget = {}
        self.udpClient = UdpClient(SOCKET_IP, SOCKET_PORT)
        self.udpClientThread = UdpClientThread(self.udpClient, self)
        self.udpClientThread.start()
        self.setupPlayerMap()
        
    def udpCallback(self, text):
        text_split = text.split(":")
        shooter_id = int(text_split[0])
        hit_id = int(text_split[1])

        shooter_player_info = self.player_id_to_info[shooter_id]
        shooter_player_info.score += 1

    def setupPlayerMap(self):
        all_players = self.red_team_players + self.blue_team_players
        for player in all_players:
            self.player_id_to_info[player.id] = player

    def setupUIEvents(self):
        self.startingGameTimer.callback = self.updateTimer
        self.startingGameTimer.start()

        self.refreshTable()
    
    def refreshTable(self):
        self.ui.team1.setRowCount(0)
        self.ui.team2.setRowCount(0)

        for player_info in self.red_team_players:
            self.addRow(self.ui.team1, player_info.name, player_info.id, player_info.score)

        for player_info in self.blue_team_players:
            self.addRow(self.ui.team2, player_info.name, player_info.id, player_info.score)

    def addRow(self, table_widget, player_name, player_id, player_score):
        numRows = table_widget.rowCount()
        table_widget.insertRow(numRows)
        
        table_widget.setItem(numRows, 0, QTableWidgetItem(player_name))
        table_widget.setItem(numRows, 1, QTableWidgetItem(str(player_score)))

        self.player_id_to_row[player_id] = numRows
        self.player_id_to_table_widget[player_id] = table_widget

    def closeEvent(self, event):
        self.udpClientThread.stopped = True
        self.udpClient.s.close()

        if main_window == self:
            sys.exit()
        else:
            event.accept()

    def updateTimer(self, secondsLeft):
        timer_text = f"Time Remaining: {countdownTimer.toString(secondsLeft)}"
        timer_text_color = "black"

        if secondsLeft <= 10:
            timer_text_color = "red"
        
        self.ui.timeRemaining.setStyleSheet(f"QPlainTextEdit {{color: {timer_text_color};}}")
        self.ui.timeRemaining.setPlainText(timer_text)

        self.refreshTable()
        
        if secondsLeft == 0:
            show_player_entry_screen()
            self.close()

def show_player_entry_screen():
    global main_window
    main_window = PlayerEntryWindow()
    main_window.ui = Ui_MainWindow()
    main_window.ui.setupUi(main_window)
    main_window.setupUIEvents()
    main_window.show()
    
    return main_window


def show_timer_screen(game_timer_duration, red_team_players, blue_team_players):
    global main_window

    main_window = TimerScreen(game_timer_duration, red_team_players, blue_team_players)
    main_window.ui = TimerWindow()
    main_window.ui.setupUi(main_window)
    main_window.setupUIEvents()
    main_window.show()

    return main_window


def show_play_action_screen(timer_duration, red_team_players, blue_team_players):
    global main_window

    # we're replacing the window, so it's fine if it gets gc'd
    main_window = PlayActionScreen(timer_duration, red_team_players, blue_team_players)
    main_window.ui = Ui_PlayActionWindow()
    main_window.ui.setupUi(main_window)
    main_window.setupUIEvents()
    main_window.show()
    
    return main_window

def show_splash_screen():
    splashWin = SplashWindow()
    splashWin.showMaximized()
    return splashWin

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    splash_screen = show_splash_screen()
    splash_screen.closed.connect(show_player_entry_screen)
    
    # don't close yet, we still need to open the main window
    app.exec_()

main()