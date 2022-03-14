import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from playerEntryScreen import Ui_MainWindow
from playActionScreen import Ui_PlayActionWindow
from timerScreen import Ui_MainWindow as TimerWindow
from database.database import database
from countdownTimer import countdownTimer


# pyqt/python is stupid and will immediately gc all windows
# so hold a reference to all windows so it knows not to destroy them
main_window = None
#database = database()
#database.open()
startingGameTimer = countdownTimer(None, lambda * args: None)

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

        # setting timer
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
        self.ui.startGame.clicked.connect(show_timer_screen)

    def closeEvent(self, event):
        # close here instead of after splash
        # sys.exit()
        event.accept()
    
    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_F5:
            show_timer_screen()

class PlayActionScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
    def setupUIEvents(self):
       pass

    def closeEvent(self, event):
        # close here instead of after splash
        sys.exit()
        event.accept()

class TimerScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        
    def setupUIEvents(self):
        self.ui.pushButton.clicked.connect(show_player_entry_screen)

    def closeEvent(self, event):
        # close here instead of after splash
        # sys.exit()
        event.accept()

    def warningTimer(self, secondsLeft):
        if(secondsLeft <= 10):
            self.ui.textEdit.setPlainText("WARNING!\n" + countdownTimer.toString(secondsLeft))
            if secondsLeft == 0:
                show_play_action_screen()
                self.close()
        else:
            self.ui.textEdit.setPlainText(countdownTimer.toString(secondsLeft))

def show_player_entry_screen():
    global main_window
    main_window = PlayerEntryWindow()
    main_window.ui = Ui_MainWindow()
    main_window.ui.setupUi(main_window)
    main_window.setupUIEvents()
    main_window.show()
    startingGameTimer.reset()
    
    return main_window

def show_timer_screen():
    global main_window

    try:
        startingGameTimer.duration = int (main_window.ui.textEdit.toPlainText())
        startingGameTimer.reset()
    except:
        pass

    main_window = TimerScreen()
    main_window.ui = TimerWindow()
    main_window.ui.setupUi(main_window)
    main_window.setupUIEvents()
    main_window.show()

    startingGameTimer.intervalFunc = main_window.warningTimer
    startingGameTimer.timeoutFunc = main_window.warningTimer
    main_window.warningTimer(startingGameTimer.duration)
    startingGameTimer.start()

def show_play_action_screen():
    global main_window

    # we're replacing the window, so it's fine if it gets gc'd
    main_window = PlayActionScreen()
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