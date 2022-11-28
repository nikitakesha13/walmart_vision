from PyQt5 import QtCore, QtGui, QtWidgets
import NIOSH_graph
from misc import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os


#helper functions
class Ui_nioshDialog(object):
	def __init__(self, _weight=0, _grip=0, _freq=0, _objDist=0, _hDist=0, _vDist=0, _wUnit=0, _fUnit=0, _oUnit=0, _hUnit=0, _vUnit=0, _gui=None):
		self.weight = _weight
		self.grip = _grip
		self.freq = _freq
		self.objDist = _objDist
		self.hDist = _hDist
		self.vDist = _vDist

		self.wUnit = _wUnit
		self.fUnit = _fUnit
		self.oUnit = _oUnit
		self.hUnit = _hUnit
		self.vUnit = _vUnit

		self.gui = _gui

		self.weight_arr = []
		self.y_arr = []
		self.good_risk = []
		self.fair_risk = []
		self.poor_risk = []

	def getNIOSHIndex(self):
		self.weight = self.weightBox.value()
		self.wUnit = self.weightUnit.currentText()
		self.gui.setWeight(self.weight, self.wUnit)

		self.grip = self.gripBox.currentText()
		self.gui.setGrip(self.grip)

		self.freq = self.freqBox.value()
		self.fUnit = self.freqUnit.currentText
		self.gui.setFrequency(self.freq, self.fUnit)

		self.objDist = self.objDistBox.value()
		self.oUnit = self.objDistUnit.currentText()
		self.gui.setObjDist(self.objDist, self.oUnit)

		self.hDist = self.hDistanceBox.value()
		self.hUnit = self.hDistUnit.currentText()
		self.gui.setHDist(self.hDist, self.hUnit)

		self.vDist = self.vDistanceBox.value()
		self.vUnit = self.vDistUnit.currentText()
		self.gui.setVDist(self.vDist, self.vUnit)

		self.calcObj = Calc(convertToInch(self.hDist, self.hUnit), convertToInch(self.vDist, self.vUnit), convertToInch(self.objDist, self.objDistUnit), self.grip, convertToLb(self.weight, self.weightUnit))
		niosh_in = self.calcObj.liftingIndex()

		if (niosh_in == -1):
				niosh_in = "Warning: VERY HIGH RISK"
				self.gui.riskLabel.setStyleSheet("color: #f00;")
		elif (niosh_in < 1):
				niosh_in = str(round(niosh_in,5)) + " - NORMAL"
				self.gui.riskLabel.setStyleSheet("color: lime;")
		elif (niosh_in >= 1):
				niosh_in = str(round(niosh_in,5)) + " - RISKY"
				self.gui.riskLabel.setStyleSheet("color: #fab432;")

		self.gui.riskLabel.setText(niosh_in)
		self.gui.label_2.setText("Object Weight (" + self.weightUnit.currentText() + "):")
		self.gui.weightLabel.setText(str(self.weightBox.value()))

	def setGraph(self):
		#create the graphing object
		self.graphingObj = NIOSH_graph.Graph(convertToInch(self.hDist, self.hUnit), convertToInch(self.vDist, self.vUnit), convertToInch(self.objDist, self.oUnit), "Good", convertToLb(self.weight, self.wUnit))
		self.graphingObj.create_weight_array(self.weight_arr)
		self.graphingObj.create_risk_array(self.good_risk, self.fair_risk, self.poor_risk, self.y_arr, self.weight_arr)
        #set axis titles
		self.graphwidget.setLabel('left', "<span style=\"color:white;font-size:15px\">NIOSH Risk Index</span>")
		self.graphwidget.setLabel('bottom', "<span style=\"color:white;font-size:15px\">Weight of Box (lbs)</span>")
        #add a legend
		self.graphwidget.addLegend()
        #create pens to edit the colors of the graph
		pen_good = pg.mkPen(color=(0, 255, 0))
		pen_fair = pg.mkPen(color=(0, 255, 0),style=QtCore.Qt.DashLine)
		pen_poor = pg.mkPen(color=(0, 255, 0),style=QtCore.Qt.DotLine)
		pen_high_risk = pg.mkPen(color=(255, 0, 0))
        #Plot the lines on the graph
		self.graphwidget.plot(self.weight_arr, self.good_risk, name = "Good Grip", pen = pen_good)
		self.graphwidget.plot(self.weight_arr, self.fair_risk, name = "Fair Grip", pen = pen_fair)
		self.graphwidget.plot(self.weight_arr, self.poor_risk, name = "Poor Grip", pen = pen_poor)
		self.graphwidget.plot(self.weight_arr, self.y_arr, name = "High Risk", pen = pen_high_risk)

	def setupUi(self, nioshDialog):
		nioshDialog.setObjectName("nioshDialog")
		nioshDialog.resize(814, 444)
		nioshDialog.setAcceptDrops(False)
		nioshDialog.setAutoFillBackground(False)
		nioshDialog.setStyleSheet("background-color: rgb(44, 44, 44);\n" "color: #fff;")
		nioshDialog.setSizeGripEnabled(False)
		nioshDialog.setModal(False)
		
		self.saveButton = QtWidgets.QPushButton(nioshDialog, clicked = lambda:self.getNIOSHIndex())
		self.saveButton.setGeometry(QtCore.QRect(90, 370, 101, 30))
		self.saveButton.setStyleSheet("background-color: white;\n" "color: black;")
		self.saveButton.setObjectName("saveButton")
		
		self.clearButton = QtWidgets.QPushButton(nioshDialog)
		self.clearButton.setGeometry(QtCore.QRect(200, 370, 100, 30))
		self.clearButton.setStyleSheet("background-color: white;\n" "color: black;")
		self.clearButton.setObjectName("clearButton")
		
		self.groupBox = QtWidgets.QGroupBox(nioshDialog)
		self.groupBox.setGeometry(QtCore.QRect(20, 10, 341, 101))
		self.groupBox.setStyleSheet("")
		self.groupBox.setObjectName("groupBox")
		
		self.weightLabel = QtWidgets.QLabel(self.groupBox)
		self.weightLabel.setGeometry(QtCore.QRect(10, 30, 91, 20))
		self.weightLabel.setObjectName("weightLabel")
		
		self.weightBox = QtWidgets.QDoubleSpinBox(self.groupBox)
		self.weightBox.setGeometry(QtCore.QRect(140, 30, 121, 21))
		self.weightBox.setStyleSheet("border-color: rgb(44, 44, 44);")
		self.weightBox.setObjectName("weightBox")
		
		self.gripLabel = QtWidgets.QLabel(self.groupBox)
		self.gripLabel.setGeometry(QtCore.QRect(10, 60, 71, 16))
		self.gripLabel.setObjectName("gripLabel")
		
		self.gripBox = QtWidgets.QComboBox(self.groupBox)
		self.gripBox.setGeometry(QtCore.QRect(140, 60, 181, 21))
		self.gripBox.setStyleSheet("background-color: rgb(44, 44, 44);\n" "color: rgb(255, 255, 255);")
		self.gripBox.setMinimumContentsLength(3)
		self.gripBox.setObjectName("gripBox")
		self.gripBox.addItem("")
		self.gripBox.addItem("")
		self.gripBox.addItem("")
		
		self.weightUnit = QtWidgets.QComboBox(self.groupBox)
		self.weightUnit.setGeometry(QtCore.QRect(270, 30, 51, 22))
		self.weightUnit.setObjectName("weightUnit")
		self.weightUnit.addItem("")
		self.weightUnit.addItem("")
		
		self.groupBox_2 = QtWidgets.QGroupBox(nioshDialog)
		self.groupBox_2.setGeometry(QtCore.QRect(20, 130, 341, 71))
		self.groupBox_2.setObjectName("groupBox_2")
		
		self.freqLabel = QtWidgets.QLabel(self.groupBox_2)
		self.freqLabel.setGeometry(QtCore.QRect(10, 30, 91, 20))
		self.freqLabel.setObjectName("freqLabel")
		
		self.freqBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
		self.freqBox.setGeometry(QtCore.QRect(140, 30, 61, 21))
		self.freqBox.setStyleSheet("border-color: rgb(44, 44, 44);")
		self.freqBox.setDecimals(0)
		self.freqBox.setObjectName("freqBox")
		
		self.label = QtWidgets.QLabel(self.groupBox_2)
		self.label.setGeometry(QtCore.QRect(210, 30, 31, 16))
		self.label.setObjectName("label")
		
		self.freqUnit = QtWidgets.QComboBox(self.groupBox_2)
		self.freqUnit.setGeometry(QtCore.QRect(240, 30, 81, 22))
		self.freqUnit.setObjectName("freqUnit")
		self.freqUnit.addItem("")
		self.freqUnit.addItem("")
		self.freqUnit.addItem("")
		
		self.groupBox_3 = QtWidgets.QGroupBox(nioshDialog)
		self.groupBox_3.setGeometry(QtCore.QRect(20, 220, 341, 141))
		self.groupBox_3.setObjectName("groupBox_3")
		
		self.objDistLabel = QtWidgets.QLabel(self.groupBox_3)
		self.objDistLabel.setGeometry(QtCore.QRect(10, 30, 91, 20))
		self.objDistLabel.setObjectName("objDistLabel")
		self.objDistBox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
		self.objDistBox.setGeometry(QtCore.QRect(140, 30, 121, 21))
		self.objDistBox.setStyleSheet("border-color: rgb(44, 44, 44);")
		self.objDistBox.setObjectName("objDistBox")
		
		self.hdLabel = QtWidgets.QLabel(self.groupBox_3)
		self.hdLabel.setGeometry(QtCore.QRect(10, 60, 121, 16))
		self.hdLabel.setObjectName("hdLabel")
		
		self.hDistanceBox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
		self.hDistanceBox.setGeometry(QtCore.QRect(140, 60, 121, 21))
		self.hDistanceBox.setStyleSheet("border-color: rgb(44, 44, 44);")
		self.hDistanceBox.setObjectName("hDistanceBox")
		
		self.vDistanceBox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
		self.vDistanceBox.setGeometry(QtCore.QRect(140, 90, 121, 21))
		self.vDistanceBox.setStyleSheet("border-color: rgb(44, 44, 44);")
		self.vDistanceBox.setObjectName("vDistanceBox")
		
		self.vdLabel = QtWidgets.QLabel(self.groupBox_3)
		self.vdLabel.setGeometry(QtCore.QRect(10, 90, 121, 16))
		self.vdLabel.setObjectName("vdLabel")
		
		self.objDistUnit = QtWidgets.QComboBox(self.groupBox_3)
		self.objDistUnit.setGeometry(QtCore.QRect(270, 30, 51, 22))
		self.objDistUnit.setObjectName("objDistUnit")
		self.objDistUnit.addItem("")
		self.objDistUnit.addItem("")
		self.objDistUnit.addItem("")
		self.objDistUnit.addItem("")
		
		self.hDistUnit = QtWidgets.QComboBox(self.groupBox_3)
		self.hDistUnit.setGeometry(QtCore.QRect(270, 60, 51, 22))
		self.hDistUnit.setObjectName("hDistUnit")
		self.hDistUnit.addItem("")
		self.hDistUnit.addItem("")
		
		self.vDistUnit = QtWidgets.QComboBox(self.groupBox_3)
		self.vDistUnit.setGeometry(QtCore.QRect(270, 90, 51, 22))
		self.vDistUnit.setObjectName("vDistUnit")
		self.vDistUnit.addItem("")
		self.vDistUnit.addItem("")
		
		self.graphwidget = PlotWidget(nioshDialog)
		self.graphwidget.setGeometry(QtCore.QRect(409, 39, 371, 321))
		self.graphwidget.setObjectName("graphwidget")
		
		self.plot = QtWidgets.QPushButton(nioshDialog, clicked = lambda:self.setGraph())
		self.plot.setGeometry(QtCore.QRect(520, 370, 151, 30))
		self.plot.setStyleSheet("background-color: white;\n""color: black;")
		self.plot.setObjectName("plot")
		
		self.retranslateUi(nioshDialog)
		QtCore.QMetaObject.connectSlotsByName(nioshDialog)

	def retranslateUi(self, nioshDialog):
		_translate = QtCore.QCoreApplication.translate
		nioshDialog.setWindowTitle(_translate("nioshDialog", "NIOSH Calculator"))
		
		self.saveButton.setText(_translate("nioshDialog", "Save"))
		self.clearButton.setText(_translate("nioshDialog", "Reset"))
		
		self.groupBox.setTitle(_translate("nioshDialog", "General"))
		
		self.weightLabel.setText(_translate("nioshDialog", "Object Weight"))
		
		self.gripLabel.setText(_translate("nioshDialog", "Grip Quality"))
		self.gripBox.setItemText(0, _translate("nioshDialog", "Good"))
		self.gripBox.setItemText(1, _translate("nioshDialog", "Fair"))
		self.gripBox.setItemText(2, _translate("nioshDialog", "Bad"))
		
		self.weightUnit.setItemText(0, _translate("nioshDialog", "lb"))
		self.weightUnit.setItemText(1, _translate("nioshDialog", "kg"))
		
		self.groupBox_2.setTitle(_translate("nioshDialog", "Advanced"))
		
		self.freqLabel.setText(_translate("nioshDialog", "Frequency"))
		
		self.label.setText(_translate("nioshDialog", "per"))
		
		self.freqUnit.setItemText(0, _translate("nioshDialog", "second"))
		self.freqUnit.setItemText(1, _translate("nioshDialog", "minute"))
		self.freqUnit.setItemText(2, _translate("nioshDialog", "hour"))
		
		self.groupBox_3.setTitle(_translate("nioshDialog", "NIOSH Risk Index"))
		
		self.objDistLabel.setText(_translate("nioshDialog", "Object Distance"))
		
		self.hdLabel.setText(_translate("nioshDialog", "Horizontal Distnance"))
		self.vdLabel.setText(_translate("nioshDialog", "Vertical Distance"))
		
		self.objDistUnit.setItemText(0, _translate("nioshDialog", "in"))
		self.objDistUnit.setItemText(1, _translate("nioshDialog", "ft"))
		self.objDistUnit.setItemText(2, _translate("nioshDialog", "cm"))
		self.objDistUnit.setItemText(3, _translate("nioshDialog", "m"))
		
		self.hDistUnit.setItemText(0, _translate("nioshDialog", "lb"))
		self.hDistUnit.setItemText(1, _translate("nioshDialog", "kg"))
		
		self.vDistUnit.setItemText(0, _translate("nioshDialog", "lb"))
		self.vDistUnit.setItemText(1, _translate("nioshDialog", "kg"))
		
		self.plot.setText(_translate("nioshDialog", "Plot"))

#create a class for the NIOSH equation
class Calc:
    def __init__(self, horizontalMulti, verticalMulti, DistMulti, cm, weight):
        self.horizontialMulti = HMFactor(horizontalMulti)
        self.verticalMulti = VMFactor(verticalMulti)
        self.DistMulti = DMFactor(DistMulti)
        self.cm = couplingMultiplier(cm)
        self.weight = weight

   #run just a basic calculation for the recommended weight
    def RecommendWeight (self):
        #set the defult values since we dont add this to our equation and its mutiplying make it 1
        asymetricMulti = 1.0
        freq = 1.0
        #RWL = LC (51) x HM x VM x DM x AM x FM x CM
        recWeight = 51.0 * self.horizontialMulti * self.verticalMulti * self.DistMulti * self.cm * freq * asymetricMulti
        
        return recWeight

    #run for the  lifting index 
    def liftingIndex (self):
        #index is Lifting weight index = weight / RWL
        if (self.RecommendWeight() > 0):
            index = float(self.weight) / self.RecommendWeight()
        else:
            return -1
        return index