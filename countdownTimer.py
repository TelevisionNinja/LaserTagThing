from PyQt5.QtCore import QTimer

# imports for testing
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import sys


class countdownTimer:
    def __init__(self, duration, timeoutFunc, intervalFunc = lambda *args: None):
        """
        duration: amount of seconds the timer will take to execute the "timeoutFunc" function
        timeoutFunc: the function to be executed at the end of the timer duration. first parameter passed is the number of seconds left (0 seconds)
        intervalFunc: the function to be executed during every second. first parameter passed is the number of seconds left (n seconds)
        """

        self.__timer = QTimer()

        # default value of 30 seconds
        if duration is None or duration == 0:
            duration = 30

        self.duration = duration
        self.__remainingTime = self.duration
        self.intervalFunc = intervalFunc
        self.timeoutFunc = timeoutFunc
        self.__timer.timeout.connect(self.__timerInterval)


    def __timerInterval(self):
        self.__remainingTime -= 1

        if self.__remainingTime == 0:
            self.timeoutFunc(0)
            self.stop()
        else:
            self.intervalFunc(self.__remainingTime)


    def start(self):
        """
        starts the timer

        the timer will nto start if the time left is 0 seconds
        """

        if self.__remainingTime != 0:
            self.__timer.start(1000)


    def stop(self):
        """
        stops the timer
        """

        self.__timer.stop()


    def reset(self):
        """
        stops and resets the timer
        """

        self.stop()
        self.__remainingTime = self.duration


    def toString(seconds):
        """
        converts an integer of seconds to a formatted string output of minutes and seconds
        """

        minutes = seconds // 60
        seconds %= 60
        return f'{minutes:02}:{seconds:02}'


# test the timer with a pretty little window
def main():
    class Test(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()

            # window
            self.setGeometry(200, 200, 200, 200)
            self.setWindowTitle("test")

            # label
            self.timerLabel = QtWidgets.QLabel(self)
            self.timerLabel.move(50,50)
            self.timerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # self.timerLabel.setStyleSheet("font: 10pt Calibri")

            self.timer = countdownTimer(5, self.updateGUI, self.updateGUI)
            # self.timer = countdownTimer(5, self.updateGUI)

            self.updateGUI(self.timer.duration)

            # buttons
            self.startButton = QtWidgets.QPushButton(self)
            self.startButton.setText("Start")
            self.startButton.move(50,100)
            self.startButton.clicked.connect(self.timer.start)

            self.stopButton = QtWidgets.QPushButton(self)
            self.stopButton.setText("Stop")
            self.stopButton.move(50,130)
            self.stopButton.clicked.connect(self.timer.stop)

            self.resetButton = QtWidgets.QPushButton(self)
            self.resetButton.setText("Reset")
            self.resetButton.move(50,160)
            self.resetButton.clicked.connect(self.reset)


        def updateGUI(self, remainingTIme = 0):
            self.timerLabel.setText(countdownTimer.toString(remainingTIme))

        
        def reset(self):
            self.timer.reset()
            self.timerLabel.setText(countdownTimer.toString(self.timer.duration))


    app = QtWidgets.QApplication(sys.argv)
    main_window = Test()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

    




