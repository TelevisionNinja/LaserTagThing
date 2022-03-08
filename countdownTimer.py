from PyQt5 import QtCore

# imports for testing
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class countdownTimer:
    def __init__(self, timeoutFunc, intervalFunc = None):
        self.timer = QtCore.QTimer()
        self.duration = 30 # default value of 30 seconds
        self.intervalFunc = intervalFunc
        self.timeoutFunc = timeoutFunc
        self.remainingTime = 0


    def __timeout(self):
        self.remainingTime -= 1

        if self.remainingTime == 0:
            self.timeoutFunc(self.remainingTime)
            self.remainingTime = self.duration
        
        self.intervalFunc(self.remainingTime)


    def start(self):
        self.timer.timeout.connect(self.__timeout)
        self.timer.start(self.duration * 100)


    def stop(self):
        self.timer.stop()


    def reset(self):
        self.remainingTime = self.duration


    def toString(seconds):
        """
        converts an integer of seconds to a formatted string output of minutes and seconds
        """

        minutes = seconds // 60
        seconds %= 60
        return f'{minutes:02}:{seconds:02}'


# test the timer with a pretty little window
def main():
    class App(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            self.timer = countdownTimer(self.updateGUI, self.updateGUI)

            # window
            self.app = QApplication(sys.argv)
            self.win = QMainWindow()
            self.win.setGeometry(200, 200, 200, 200)
            self.win.setWindowTitle("test")

            # buttons and labels
            self.timerLabel = QtWidgets.QLabel(self.win)
            self.timerLabel.move(50,50)
            self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.timerLabel.setStyleSheet("font: 10pt Calibri")

            self.startButton = QtWidgets.QPushButton(self.win)
            self.startButton.setText("Start")
            self.startButton.move(50,100)
            self.startButton.clicked.connect(self.timer.start)

            self.stopButton = QtWidgets.QPushButton(self.win)
            self.stopButton.setText("Stop")
            self.stopButton.move(50,130)
            self.startButton.clicked.connect(self.timer.stop)

            self.stopButton = QtWidgets.QPushButton(self.win)
            self.stopButton.setText("Reset")
            self.stopButton.move(50,160)
            self.startButton.clicked.connect(self.timer.reset)

            self.updateGUI(self.timer.duration)

            # window
            self.win.show()
            sys.exit(app.exec_())


        def updateGUI(self, remainingTIme):
            self.timerLabel.setText(countdownTimer.toString(remainingTIme))


    app = QtWidgets.QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
