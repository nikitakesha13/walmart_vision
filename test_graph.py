from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import NIOSH_graph
from PyQt5 import QtCore, QtGui, QtWidgets
from misc import Misc

#helper functions
misc = Misc()

class Ui_Form(object):
    def __init__(self, _weight=0, _objDist=0, _hDist=0, _vDist=0, _wUnit=0, _fUnit=0, _oUnit=0, _hUnit=0, _vUnit=0, _gui=None):

        self.weight = _weight
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
        

        
    def setGraph(self):
        self.weight = self.weightBox.value()
        self.wUnit = self.weightUnit.currentText()
        #self.gui.setWeight(self.weight, self.wUnit)

        self.objDist = self.objDistBox.value()
        self.oUnit = self.objUnit.currentText()
        #self.gui.setObjDist(self.objDist, self.oUnit)

        self.hDist = self.hdDistBox.value()
        self.hUnit = self.hdUnit.currentText()
        #self.gui.setHDist(self.hDist, self.hUnit)

        self.vDist = self.vdDistBox.value()
        self.vUnit = self.weightUnit_5.currentText()
        #self.gui.setVDist(self.vDist, self.vUnit)

        self.graphingObj = NIOSH_graph.Graph(misc.convertToInch(self.hDist, self.hUnit), misc.convertToInch(self.vDist, self.vUnit), misc.convertToInch(self.objDist, self.oUnit), "Good", misc.convertToLb(self.weight, self.wUnit))
        #create the arrays to plot
    

        self.graphingObj.create_weight_array(self.weight_arr)
        self.graphingObj.create_risk_array(self.good_risk, self.fair_risk, self.poor_risk, self.y_arr, self.weight_arr)
        #set axis titles
        self.graphWidget.setLabel('left', "<span style=\"color:white;font-size:15px\">NIOSH Risk Index</span>")
        self.graphWidget.setLabel('bottom', "<span style=\"color:white;font-size:15px\">Weight of Box (lbs)</span>")
        #add a legend
        self.graphWidget.addLegend()
        #create pens to edit the colors of the graph
        pen_good = pg.mkPen(color=(0, 255, 0))
        pen_fair = pg.mkPen(color=(0, 255, 0),style=QtCore.Qt.DashLine)
        pen_poor = pg.mkPen(color=(0, 255, 0),style=QtCore.Qt.DotLine)
        pen_high_risk = pg.mkPen(color=(255, 0, 0))
        #Plot the lines on the graph
        self.graphWidget.plot(self.weight_arr, self.good_risk, name = "Good Grip", pen = pen_good)
        self.graphWidget.plot(self.weight_arr, self.fair_risk, name = "Fair Grip", pen = pen_fair)
        self.graphWidget.plot(self.weight_arr, self.poor_risk, name = "Poor Grip", pen = pen_poor)
        self.graphWidget.plot(self.weight_arr, self.y_arr, name = "High Risk", pen = pen_high_risk)
        



    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1005, 429)
        Form.setStyleSheet("background-color: rgb(44, 44, 44);\n" "color: #fff;")
        
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setGeometry(QtCore.QRect(30, 30, 421, 341))
        self.groupBox_4.setStyleSheet("")
        self.groupBox_4.setObjectName("groupBox_4")
        
        self.weightLabel = QtWidgets.QLabel(self.groupBox_4)
        self.weightLabel.setGeometry(QtCore.QRect(10, 50, 91, 20))
        self.weightLabel.setObjectName("weightLabel")
        
        self.weightBox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.weightBox.setGeometry(QtCore.QRect(150, 50, 121, 21))
        self.weightBox.setStyleSheet("border-color: rgb(44, 44, 44);")
        self.weightBox.setObjectName("weightBox")
        
        self.weightUnit = QtWidgets.QComboBox(self.groupBox_4)
        self.weightUnit.setGeometry(QtCore.QRect(310, 50, 51, 22))
        self.weightUnit.setObjectName("weightUnit")
        self.weightUnit.addItem("")
        self.weightUnit.addItem("")
        
        self.objDistLabel = QtWidgets.QLabel(self.groupBox_4)
        self.objDistLabel.setGeometry(QtCore.QRect(10, 90, 91, 20))
        self.objDistLabel.setObjectName("objDistLabel")
        
        self.hdLabel = QtWidgets.QLabel(self.groupBox_4)
        self.hdLabel.setGeometry(QtCore.QRect(10, 130, 121, 16))
        self.hdLabel.setObjectName("hdLabel")
        
        self.vdLabel = QtWidgets.QLabel(self.groupBox_4)
        self.vdLabel.setGeometry(QtCore.QRect(10, 170, 121, 16))
        self.vdLabel.setObjectName("vdLabel")
        
        self.objDistBox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.objDistBox.setGeometry(QtCore.QRect(150, 90, 121, 21))
        self.objDistBox.setStyleSheet("border-color: rgb(44, 44, 44);")
        self.objDistBox.setObjectName("objDistBox")
        
        self.hdDistBox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.hdDistBox.setGeometry(QtCore.QRect(150, 130, 121, 21))
        self.hdDistBox.setStyleSheet("border-color: rgb(44, 44, 44);")
        self.hdDistBox.setObjectName("hdDistBox")
        
        self.vdDistBox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.vdDistBox.setGeometry(QtCore.QRect(150, 170, 121, 21))
        self.vdDistBox.setStyleSheet("border-color: rgb(44, 44, 44);")
        self.vdDistBox.setObjectName("vdDistBox")
        
        self.objUnit = QtWidgets.QComboBox(self.groupBox_4)
        self.objUnit.setGeometry(QtCore.QRect(310, 90, 51, 22))
        self.objUnit.setObjectName("objUnit")
        self.objUnit.addItem("")
        self.objUnit.addItem("")
        
        self.hdUnit = QtWidgets.QComboBox(self.groupBox_4)
        self.hdUnit.setGeometry(QtCore.QRect(310, 130, 51, 22))
        self.hdUnit.setObjectName("hdUnit")
        self.hdUnit.addItem("")
        self.hdUnit.addItem("")
        
        self.weightUnit_5 = QtWidgets.QComboBox(self.groupBox_4)
        self.weightUnit_5.setGeometry(QtCore.QRect(310, 170, 51, 22))
        self.weightUnit_5.setObjectName("weightUnit_5")
        self.weightUnit_5.addItem("")
        self.weightUnit_5.addItem("")
        
        self.plot = QtWidgets.QPushButton(Form, clicked = lambda:self.setGraph())
        self.plot.setGeometry(QtCore.QRect(70, 250, 241, 21))
        self.plot.setStyleSheet("background-color: white;\n""color: black;")
        self.plot.setObjectName("plot")
        
        self.graphWidget = PlotWidget(Form)
        self.graphWidget.setGeometry(QtCore.QRect(490, 40, 481, 331))
        self.graphWidget.setObjectName("graphWidget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_4.setTitle(_translate("Form", "General"))
        self.weightLabel.setText(_translate("Form", "Object Weight"))
        self.weightUnit.setItemText(0, _translate("Form", "lb"))
        self.weightUnit.setItemText(1, _translate("Form", "kg"))
        self.objDistLabel.setText(_translate("Form", "Object Distance"))
        self.hdLabel.setText(_translate("Form", "Horizontal Distnance"))
        self.vdLabel.setText(_translate("Form", "Vertical Distance"))
        self.objUnit.setItemText(0, _translate("Form", "lb"))
        self.objUnit.setItemText(1, _translate("Form", "kg"))
        self.hdUnit.setItemText(0, _translate("Form", "lb"))
        self.hdUnit.setItemText(1, _translate("Form", "kg"))
        self.weightUnit_5.setItemText(0, _translate("Form", "lb"))
        self.weightUnit_5.setItemText(1, _translate("Form", "kg"))
        self.plot.setText(_translate("Form", "Plot"))

if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        form = QtWidgets.QDialog()
        ui = Ui_Form()
        ui.setupUi(form)
        form.show()
        sys.exit(app.exec_())


