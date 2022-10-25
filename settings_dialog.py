from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_settingsDialog(object):
	def __init__(self, _device, _model, _thres, _main_gui):
		self.device = _device
		self.model = _model
		self.thres = _thres
		self.gui = _main_gui

	def getDevice(self):
		return self.device
	def getModel(self):
		return self.model
	def getThreshold(self):
		return self.thres
        
        #Set selected values for device, model and threshold after the OK button is pressed.
	def applyChanges(self):
		#get device input
		if (self.cpuOption.isChecked()):
				self.gui.setDevice("cpu")
				self.device = "cpu"
		elif (self.gpuOption.isChecked()):
				self.gui.setDevice("gpu")
				self.device = "gpu"
			
		#get model input
		if (self.cocoOption.isChecked()):
				self.gui.setModel("COCO")
				self.model = "COCO"
		elif (self.mpiOption.isChecked()):
				self.gui.setModel("MPI")
				self.model = "MPI"
		elif (self.body25Option.isChecked()):
				self.gui.setModel("BODY_25")
				self.model = "BODY_25"
		
		#get threshold value
		self.gui.setThreshold(self.thresholdBox.value())
		self.thres = self.thresholdBox.value()

		self.gui.modelLabel.setText(self.model)
	
	def resetValue(self):
		self.cpuOption.setChecked(True)
		self.body25Option.setChecked(True)
		self.thresholdBox.setProperty("value", 0.1)
		self.applyChanges()

	def setupUi(self, settingsDialog):
		settingsDialog.setObjectName("settingsDialog")
		settingsDialog.resize(461, 294)
		settingsDialog.setStyleSheet("background-color: rgb(44, 44, 44); color: rgb(255, 255, 255);")
		self.deviceBox = QtWidgets.QGroupBox(settingsDialog)
		self.deviceBox.setGeometry(QtCore.QRect(20, 20, 311, 71))
		self.deviceBox.setObjectName("deviceBox")
		self.cpuOption = QtWidgets.QRadioButton(self.deviceBox)
		self.cpuOption.setGeometry(QtCore.QRect(20, 30, 95, 20))
		self.cpuOption.setChecked(True)
		self.cpuOption.setObjectName("cpuOption")
		self.gpuOption = QtWidgets.QRadioButton(self.deviceBox)
		self.gpuOption.setGeometry(QtCore.QRect(120, 30, 95, 20))
		self.gpuOption.setObjectName("gpuOption")
		self.modelBox = QtWidgets.QGroupBox(settingsDialog)
		self.modelBox.setGeometry(QtCore.QRect(20, 120, 311, 71))
		self.modelBox.setObjectName("modelBox")
		self.cocoOption = QtWidgets.QRadioButton(self.modelBox)
		self.cocoOption.setGeometry(QtCore.QRect(20, 30, 95, 20))
		self.cocoOption.setObjectName("cocoOption")
		self.mpiOption = QtWidgets.QRadioButton(self.modelBox)
		self.mpiOption.setGeometry(QtCore.QRect(120, 30, 95, 20))
		self.mpiOption.setObjectName("mpiOption")
		self.body25Option = QtWidgets.QRadioButton(self.modelBox)
		self.body25Option.setGeometry(QtCore.QRect(210, 30, 95, 20))
		self.body25Option.setChecked(True)
		self.body25Option.setObjectName("body25Option")
		self.label = QtWidgets.QLabel(settingsDialog)
		self.label.setGeometry(QtCore.QRect(20, 240, 61, 16))
		self.label.setObjectName("label")
		self.thresholdBox = QtWidgets.QDoubleSpinBox(settingsDialog)
		self.thresholdBox.setGeometry(QtCore.QRect(90, 240, 241, 21))
		self.thresholdBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.thresholdBox.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(44, 44, 44);")
		self.thresholdBox.setMinimum(0.1)
		self.thresholdBox.setSingleStep(0.01)
		self.thresholdBox.setProperty("value", 0.1)
		self.thresholdBox.setObjectName("thresholdBox")
		self.applyBttn = QtWidgets.QPushButton(settingsDialog, clicked = lambda: self.applyChanges())
		self.applyBttn.setGeometry(QtCore.QRect(350, 30, 93, 31))
		self.applyBttn.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(44, 44, 44);")
		self.applyBttn.setObjectName("applyBttn")
		self.restoreBttn = QtWidgets.QPushButton(settingsDialog, clicked = lambda: self.resetValue())
		self.restoreBttn.setGeometry(QtCore.QRect(350, 70, 93, 31))
		self.restoreBttn.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(44, 44, 44);")
		self.restoreBttn.setObjectName("restoreBttn")
		self.closeBttn = QtWidgets.QDialogButtonBox(settingsDialog)
		self.closeBttn.setGeometry(QtCore.QRect(350, 110, 91, 31))
		self.closeBttn.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(44, 44, 44);")
		self.closeBttn.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
		self.closeBttn.setObjectName("closeBttn")

		self.retranslateUi(settingsDialog)
		self.closeBttn.rejected.connect(settingsDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(settingsDialog)

	def retranslateUi(self, settingsDialog):
		_translate = QtCore.QCoreApplication.translate
		settingsDialog.setWindowTitle(_translate("settingsDialog", "Settings"))
		self.deviceBox.setTitle(_translate("settingsDialog", "Device"))
		self.cpuOption.setText(_translate("settingsDialog", "CPU"))
		self.gpuOption.setText(_translate("settingsDialog", "GPU"))
		self.modelBox.setTitle(_translate("settingsDialog", "Model"))
		self.cocoOption.setText(_translate("settingsDialog", "COCO"))
		self.mpiOption.setText(_translate("settingsDialog", "MPI"))
		self.body25Option.setText(_translate("settingsDialog", "BODY-25"))
		self.label.setText(_translate("settingsDialog", "Threshold"))
		self.applyBttn.setText(_translate("settingsDialog", "Apply"))
		self.restoreBttn.setText(_translate("settingsDialog", "Reset"))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	settingsDialog = QtWidgets.QDialog()
	ui = Ui_settingsDialog()
	ui.setupUi(settingsDialog)
	settingsDialog.show()
	sys.exit(app.exec_())
