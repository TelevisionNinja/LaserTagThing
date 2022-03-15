# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'playActionScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PlayActionWindow(object):
    def setupUi(self, PlayActionWindow):
        PlayActionWindow.setObjectName("PlayActionWindow")
        PlayActionWindow.resize(1004, 541)
        self.centralwidget = QtWidgets.QWidget(PlayActionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.currentAction = QtWidgets.QListWidget(self.centralwidget)
        self.currentAction.setGeometry(QtCore.QRect(90, 230, 801, 231))
        self.currentAction.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.currentAction.setProperty("showDropIndicator", True)
        self.currentAction.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.currentAction.setObjectName("currentAction")
        self.team1 = QtWidgets.QTableWidget(self.centralwidget)
        self.team1.setGeometry(QtCore.QRect(90, 50, 401, 191))
        self.team1.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.team1.setFont(font)
        self.team1.setLineWidth(1)
        self.team1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.team1.setRowCount(5)
        self.team1.setColumnCount(2)
        self.team1.setObjectName("team1")
        item = QtWidgets.QTableWidgetItem()
        self.team1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.team1.setHorizontalHeaderItem(1, item)
        self.team1.horizontalHeader().setCascadingSectionResizes(False)
        self.team1.horizontalHeader().setDefaultSectionSize(185)
        self.team1.horizontalHeader().setMinimumSectionSize(0)
        self.team1.horizontalHeader().setSortIndicatorShown(False)
        self.team1.horizontalHeader().setStretchLastSection(True)
        self.team1.verticalHeader().setCascadingSectionResizes(False)
        self.team1.verticalHeader().setDefaultSectionSize(30)
        self.team1.verticalHeader().setHighlightSections(True)
        self.team2 = QtWidgets.QTableWidget(self.centralwidget)
        self.team2.setGeometry(QtCore.QRect(490, 50, 401, 191))
        self.team2.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.team2.setFont(font)
        self.team2.setLineWidth(1)
        self.team2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.team2.setRowCount(5)
        self.team2.setColumnCount(2)
        self.team2.setObjectName("team2")
        item = QtWidgets.QTableWidgetItem()
        self.team2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.team2.setHorizontalHeaderItem(1, item)
        self.team2.horizontalHeader().setCascadingSectionResizes(False)
        self.team2.horizontalHeader().setDefaultSectionSize(185)
        self.team2.horizontalHeader().setMinimumSectionSize(0)
        self.team2.horizontalHeader().setSortIndicatorShown(False)
        self.team2.horizontalHeader().setStretchLastSection(True)
        self.team2.verticalHeader().setCascadingSectionResizes(False)
        self.team2.verticalHeader().setDefaultSectionSize(30)
        self.team2.verticalHeader().setHighlightSections(True)
        self.timeRemaining = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.timeRemaining.setGeometry(QtCore.QRect(660, 460, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.timeRemaining.setFont(font)
        self.timeRemaining.setReadOnly(True)
        self.timeRemaining.setObjectName("timeRemaining")
        PlayActionWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(PlayActionWindow)
        self.statusbar.setObjectName("statusbar")
        PlayActionWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PlayActionWindow)
        QtCore.QMetaObject.connectSlotsByName(PlayActionWindow)

    def retranslateUi(self, PlayActionWindow):
        _translate = QtCore.QCoreApplication.translate
        PlayActionWindow.setWindowTitle(_translate("PlayActionWindow", "Play Action Window"))
        item = self.team1.horizontalHeaderItem(0)
        item.setText(_translate("PlayActionWindow", "Name"))
        item = self.team1.horizontalHeaderItem(1)
        item.setText(_translate("PlayActionWindow", "Score"))
        item = self.team2.horizontalHeaderItem(0)
        item.setText(_translate("PlayActionWindow", "Name"))
        item = self.team2.horizontalHeaderItem(1)
        item.setText(_translate("PlayActionWindow", "Score"))
        self.timeRemaining.setPlainText(_translate("PlayActionWindow", "Time Remaining: "))
