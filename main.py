import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from playerEntryScreen import Ui_MainWindow
from database.database import database


# pyqt/python is stupid and will immediately gc all windows
# so hold a reference to all windows so it knows not to destroy them
main_window = None
database = database()
database.open()

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

        player0IDNumber = self.ui.player0FirstName.toPlainText() 
        player0UserName = self.ui.player0LastName.toPlainText()
        player1IDNumber = self.ui.player1FirstName.toPlainText()
        player1UserName = self.ui.player1LastName.toPlainText()
        database.upsert(int(player0IDNumber),"John","Doe", player0UserName)
        database.upsert(int(player1IDNumber),"John","Doe", player1UserName)


    def closeEvent(self, event):
        # close here instead of after splash
        sys.exit()
        event.accept()

def show_player_entry_screen():
    global main_window
    
    main_window = PlayerEntryWindow()
    main_window.ui = Ui_MainWindow()
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