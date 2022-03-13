import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from playerEntryScreen import Ui_MainWindow
from playActionScreen import Ui_PlayActionWindow
from database.database import database
from countdownTimer import countdownTimer


# pyqt/python is stupid and will immediately gc all windows
# so hold a reference to all windows so it knows not to destroy them
main_window = None
#database = database()
#database.open()
timer = countdownTimer(None, lambda * args: None)
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
        self.ui.startGame.clicked.connect(self.startGameEvent)

    def startGameEvent(self):
        main_window = show_play_action_screen()
       # timer = countdownTimer(5, main_window.warningTimer, main_window.warningTimer)
       # timer.start()
        timer.intervalFunc = main_window.warningTimer
        timer.timeoutFunc = main_window.warningTimer

    def closeEvent(self, event):
        # close here instead of after splash
        # sys.exit()
        event.accept()
    
    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_F5:
            show_play_action_screen()

class PlayActionScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
    def setupUIEvents(self):
       pass

    def closeEvent(self, event):
        # close here instead of after splash
        sys.exit()
        event.accept()

    def warningTimer(self, secondsLeft10):
        #self.textEdit.setPlainText("Hello")
        if(secondsLeft10 <= 10):
            self.ui.textEdit.setPlainText("WARNING!\n" + countdownTimer.toString(secondsLeft10))
        else:
            self.ui.textEdit.setPlainText(countdownTimer.toString(secondsLeft10))
            
    
def show_player_entry_screen():
    global main_window
    main_window = PlayerEntryWindow()
    main_window.ui = Ui_MainWindow()
    main_window.ui.setupUi(main_window)
    main_window.setupUIEvents()
    main_window.show()
    
    return main_window

def show_play_action_screen():
    global main_window
    timer.duration = int (main_window.ui.textEdit.toPlainText())
    timer.reset()
    # we're replacing the window, so it's fine if it gets gc'd
    main_window = PlayActionScreen()
    #timer = countdownTimer(5, main_window.__warningTimer, main_window.__warningTimer)
    main_window.ui = Ui_PlayActionWindow()
    main_window.ui.setupUi(main_window)
    main_window.setupUIEvents()
    main_window.show()
    timer.start()
    
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