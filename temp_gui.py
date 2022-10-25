from cProfile import label
from re import U
from PyQt5 import QtCore, QtGui, QtWidgets
from cv2 import threshold
from skeleton_extraction import Skeleton
from datetime import datetime
from misc import Misc

class Ui_MainWindow(object):
    def __init__(self):
        self.helper = Misc()

        self.source = 0
        self.device = "cpu"
        self.model = "BODY_25"
        self.thres = 0.1

        self.weight = 0
        self.wu = "lb"

        self.grip = "Good"

        self.freq = 1.0
        self.fu = "second"

        self.objDist = 0
        self.ou = "in"

        self.hDist = 0
        self.hu = "in"

        self.vDist = 0
        self.vu = "in"

    def setSource(self, _source):
        self.source = _source
    def setDevice(self, _device):
        self.device = _device
    def setModel(self, _model):
        self.model = _model
    def setThreshold(self, _thres):
        self.thres = _thres

    def setWeight(self, w, u):
        self.weight = w
        self.wu = u

    def setGrip(self, _g):
        self.grip = _g
   
    def setFrequency(self, f, u):
        self.fu = u
        self.freq = f

    def setObjDist(self, d, u):
        self.objDist = d
        self.ou = u

    def setHDist(self, h, u):
        self.hDist = h
        self.hu = u

    def setVDist(self, v, u):
        self.vDist = v
        self.vu = u

    def accept(self):
        self.nameLabel.setText((self.nameInput.toPlainText()).upper())

    def newRecording(self):
        name = self.nameLabel.text()
        if (name == "-"):
            currentTime = datetime.now()
            date = currentTime.strftime("%m%d%Y_%H%M%S")
            name = "user_" + date

        skeleton = Skeleton(self.helper.cleanName(name), self.source, self.device, self.model, self.thres)
        avg_fps = skeleton.pose_estimation()
        skeleton.release()
        print(name)
        print("Using", self.model)
        print(f"Average FPS: {avg_fps:.3f}")

    def openNIOSH(self):
        from niosh_dialog import Ui_nioshDialog
        self.window = QtWidgets.QDialog()
        self.ui = Ui_nioshDialog(self.weight, self.grip, self.freq, self.objDist, self.hDist, self.vDist, self.wu, self.fu, self.ou, self.hu, self.vu, self)
        self.ui.setupUi(self.window)
        self.window.show()
    
    def openSettings(self):
        from settings_dialog import Ui_settingsDialog
        self.window = QtWidgets.QDialog()
        self.ui = Ui_settingsDialog(self.device, self.model, self.thres, self)
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1282, 728)
        MainWindow.setMinimumSize(QtCore.QSize(1282, 728))
        MainWindow.setMaximumSize(QtCore.QSize(1366, 728))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(54, 54, 54); color: #fff;")
        MainWindow.setIconSize(QtCore.QSize(25, 25))
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.videoPlayer = QtWidgets.QWidget(self.centralwidget)
        self.videoPlayer.setGeometry(QtCore.QRect(350, 40, 921, 461))
        self.videoPlayer.setStyleSheet("background-color: rgb(44, 44, 44)")
        self.videoPlayer.setObjectName("videoPlayer")
        self.summaryBox = QtWidgets.QGroupBox(self.centralwidget)
        self.summaryBox.setGeometry(QtCore.QRect(950, 520, 321, 121))
        self.summaryBox.setStyleSheet("")
        self.summaryBox.setObjectName("summaryBox")
        self.label = QtWidgets.QLabel(self.summaryBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.summaryBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 131, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.summaryBox)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 121, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.summaryBox)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 121, 16))
        self.label_4.setObjectName("label_4")
        self.nameLabel = QtWidgets.QLabel(self.summaryBox)
        self.nameLabel.setGeometry(QtCore.QRect(150, 30, 161, 16))
        self.nameLabel.setObjectName("nameLabel")
        self.weightLabel = QtWidgets.QLabel(self.summaryBox)
        self.weightLabel.setGeometry(QtCore.QRect(150, 50, 161, 16))
        self.weightLabel.setObjectName("weightLabel")
        self.riskLabel = QtWidgets.QLabel(self.summaryBox)
        self.riskLabel.setGeometry(QtCore.QRect(150, 70, 161, 16))
        self.riskLabel.setObjectName("riskLabel")
        self.modelLabel = QtWidgets.QLabel(self.summaryBox)
        self.modelLabel.setGeometry(QtCore.QRect(150, 90, 161, 16))
        self.modelLabel.setObjectName("modelLabel")
        self.rcmBoard = QtWidgets.QGroupBox(self.centralwidget)
        self.rcmBoard.setGeometry(QtCore.QRect(10, 520, 931, 121))
        self.rcmBoard.setStyleSheet("")
        self.rcmBoard.setObjectName("rcmBoard")
        self.msgBoard = QtWidgets.QScrollArea(self.centralwidget)
        self.msgBoard.setGeometry(QtCore.QRect(10, 40, 331, 461))
        self.msgBoard.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(44, 44, 44);")
        self.msgBoard.setWidgetResizable(True)
        self.msgBoard.setObjectName("msgBoard")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 329, 459))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.msgPrint = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.msgPrint.setGeometry(QtCore.QRect(100, 220, 111, 16))
        self.msgPrint.setObjectName("msgPrint")
        self.msgBoard.setWidget(self.scrollAreaWidgetContents)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 131, 16))
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.nameInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(890, 0, 231, 31))
        self.nameInput.setObjectName("nameInput")
        self.nameButton = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.nameButton.setGeometry(QtCore.QRect(1130, 0, 131, 28))
        self.nameButton.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(44, 44, 44);")
        self.nameButton.setStandardButtons(QtWidgets.QDialogButtonBox.Discard|QtWidgets.QDialogButtonBox.Save)
        self.nameButton.setObjectName("nameButton")
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
        self.toolBar.setStyleSheet("color: rgb(44, 44, 44)")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionRecord = QtWidgets.QAction(MainWindow, triggered = lambda:self.newRecording())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRecord.setIcon(icon)
        self.actionRecord.setObjectName("actionRecord")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/folder (2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCalculator = QtWidgets.QAction(MainWindow, triggered = lambda: self.openNIOSH())
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/bar-chart (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCalculator.setIcon(icon2)
        self.actionCalculator.setObjectName("actionCalculator")
        self.actionSettings = QtWidgets.QAction(MainWindow, triggered = lambda: self.openSettings())
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon3)
        self.actionSettings.setObjectName("actionSettings")
        self.actionInfo = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon/information (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInfo.setIcon(icon4)
        self.actionInfo.setObjectName("actionInfo")
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionCalculator)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionInfo)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.nameButton.accepted.connect(self.accept)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Walmart Vision"))
        self.summaryBox.setTitle(_translate("MainWindow", "Summary"))
        self.label.setText(_translate("MainWindow", "Current User:"))
        self.label_2.setText(_translate("MainWindow", "Object Weight (lbs):"))
        self.label_3.setText(_translate("MainWindow", "NIOSH Risk Index:"))
        self.label_4.setText(_translate("MainWindow", "Model Used:"))
        self.nameLabel.setText(_translate("MainWindow", "-"))
        self.weightLabel.setText(_translate("MainWindow", "-"))
        self.riskLabel.setText(_translate("MainWindow", "-"))
        self.modelLabel.setText(_translate("MainWindow", "BODY_25"))
        self.rcmBoard.setTitle(_translate("MainWindow", "Recommendations"))
        self.msgPrint.setText(_translate("MainWindow", "There\'s no activity"))
        self.label_6.setText(_translate("MainWindow", "Warning log"))
        self.nameInput.setPlaceholderText(_translate("MainWindow", "Subject name"))
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
