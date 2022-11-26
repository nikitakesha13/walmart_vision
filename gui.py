from re import U
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QSizePolicy, QStyle
from PyQt5.QtCore import QTimer
from skeleton import Skeleton
from misc import *
from player import DrawVideo
from form_analysis import *
from report_gen import Report
from PyQt5.QtCore import QTimer, Qt
from time import sleep
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import time

class Ui_MainWindow(object):
    def __init__(self):
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

        self.timer = QTimer()

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
        currentName = self.nameInput.toPlainText()
        if currentName != "":
            self.nameLabel.setText((currentName).upper())
    
    def skeletonExtract(self, source):
        name = self.nameLabel.text()
        if (name == "-"):
            name = "user"

        self.skeleton = Skeleton(cleanName(name), source, self.device, self.model, self.thres)
        self.arr = self.skeleton.pose_estimation()
        self.skeleton.release()
        # arr = [average_fps, reba_max, reba_average, path]
        
        matrix = analysis(create_dicts(self.skeleton.get_form_analysis_matrix()))
        exp = DrawVideo(self.arr[3],matrix)
        err = exp.export()

        report = Report(self.arr[3], cleanName(name.capitalize()), today('slash'), self.arr[2], self.arr[1], err[0])
        report.generate_report()
        self.printMsgLog(err[0])
        self.printMsgGuide(err[1])
        self.openPlayer(self.arr[3])
    
    def newRecording(self):
        self.skeletonExtract(0)

    def openNIOSH(self):
        from NIOSH import Ui_nioshDialog
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

    def openPlayer(self, path):
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.playButton = QPushButton(self.videoPlayer)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path + "result.avi")))
        self.videoPlayer.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.playButton.setEnabled(True)
        self.layout.removeWidget(self.videoWidget)
        self.layout.addWidget(self.videoWidget)
        self.videoPlayer.setLayout(self.layout)
    
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Open Video",
                "./test-video", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")

        if fileName != '':
            print(fileName)
            self.skeletonExtract(fileName)
    
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.videoPlayer.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.videoPlayer.style().standardIcon(QStyle.SP_MediaPlay))
    
    def printMsgGuide(self, arr):
        self.guideLines.clear()
        self.guideLines.setAlignment(QtCore.Qt.AlignLeft)
        text = ""
        for msg in arr:
            text += msg + "\n"
        self.guideLines.setText(text)

    def printMsgLog(self, arr):
        self.msgPrint.clear()
        self.msgPrint.setAlignment(QtCore.Qt.AlignTop)
        text = ""
        for msg in arr:
            text += "Frame " + str(msg[1]) + ": " + msg[0] + "\n"
        
        self.msgPrint.setGeometry(QtCore.QRect(10, 10, 311, 441))
        self.msgPrint.setText(text)

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
        self.videoPlayer = QtWidgets.QWidget(self.centralwidget)
        self.videoPlayer.setGeometry(QtCore.QRect(340, 40, 931, 421))
        self.videoPlayer.setObjectName("videoPlayer")

        self.playbar = QtWidgets.QWidget(self.centralwidget)
        self.playbar.setGeometry(QtCore.QRect(340, 470, 931, 31))
        self.playbar.setStyleSheet("background-color: rgb(54, 54, 54)")
        self.playbar.setObjectName("playbar")

        self.mediaPlayer = QMediaPlayer(self.videoPlayer, QMediaPlayer.VideoSurface)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.videoWidget = QVideoWidget()

        self.playButton = QPushButton(self.playbar)
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.videoPlayer.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.playButton.setEnabled(True)

        self.positionSlider = QSlider(Qt.Horizontal, self.playbar)
        self.positionSlider.setGeometry(QtCore.QRect(50, 0, 861, 22))
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)

        self.layout = QVBoxLayout()
        self.layout.addLayout(controlLayout)
        self.videoPlayer.setLayout(self.layout)
        
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
        self.msgBoard.setGeometry(QtCore.QRect(10, 40, 321, 461))
        self.msgBoard.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(44, 44, 44);")
        self.msgBoard.setWidgetResizable(True)
        self.msgBoard.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.msgBoard.setObjectName("msgBoard")

        self.msgPrint = QtWidgets.QLabel(self.msgBoard)
        self.msgPrint.setGeometry(QtCore.QRect(100, 220, 111, 16))
        self.msgPrint.setObjectName("msgPrint")

        self.guideLines = QtWidgets.QLabel(self.rcmBoard)
        self.guideLines.setGeometry(QtCore.QRect(10, 20, 911, 91))
        self.guideLines.setObjectName("guideLines")
        
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
        
        self.actionOpen = QtWidgets.QAction(MainWindow, triggered = lambda:self.openFile())
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
        self.guideLines.setText(_translate("MainWindow", "(Empty)"))
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