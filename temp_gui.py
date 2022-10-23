# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from cProfile import label
from PyQt5 import QtCore, QtGui, QtWidgets
from niosh_dialog import Ui_nioshDialog
from settings_dialog import Ui_settingsDialog

class Ui_MainWindow(object):
    def openNIOSH(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_nioshDialog()
        self.ui.setupUi(self.window)
        self.window.show()
    
    def openSettings(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setMinimumSize(QtCore.QSize(1366, 768))
        MainWindow.setMaximumSize(QtCore.QSize(1366, 768))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(54, 54, 54); color: #fff;")
        MainWindow.setIconSize(QtCore.QSize(25, 25))
        MainWindow.setAnimated(True)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.video_player = QtWidgets.QWidget(self.centralwidget)
        self.video_player.setGeometry(QtCore.QRect(310, 10, 761, 501))
        self.video_player.setStyleSheet("background-color: rgb(44, 44, 44)")
        self.video_player.setObjectName("video_player")
        self.message_board = QtWidgets.QWidget(self.centralwidget)
        self.message_board.setGeometry(QtCore.QRect(10, 10, 291, 501))
        self.message_board.setStyleSheet("background-color: rgb(44, 44, 44)")
        self.message_board.setObjectName("message_board")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 500, 1061, 131))
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setStyleSheet("padding: 3px 5px;")
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(35, 35))
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionRecord = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/rec.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRecord.setIcon(icon)
        self.actionRecord.setObjectName("actionRecord")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/open-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCalculator = QtWidgets.QAction(MainWindow, triggered = lambda: self.openNIOSH())
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/speed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCalculator.setIcon(icon2)
        self.actionCalculator.setObjectName("actionCalculator")
        self.actionSettings = QtWidgets.QAction(MainWindow, triggered = lambda: self.openSettings())
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon3)
        self.actionSettings.setObjectName("actionSettings")
        self.actionInfo = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInfo.setIcon(icon4)
        self.actionInfo.setObjectName("actionInfo")
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionCalculator)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionInfo)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Walmart Vision"))
        self.groupBox.setTitle(_translate("MainWindow", "Recent"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionRecord.setText(_translate("MainWindow", "Record"))
        self.actionRecord.setToolTip(_translate("MainWindow", "Record a new video (Ctrl+N)"))
        self.actionRecord.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open from a video (Ctrl+O)"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionCalculator.setText(_translate("MainWindow", "Calculator"))
        self.actionCalculator.setToolTip(_translate("MainWindow", "NIOSH Risk Calculator"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.setToolTip(_translate("MainWindow", "Settings"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
        self.actionInfo.setToolTip(_translate("MainWindow", "About Us"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
