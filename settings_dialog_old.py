from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.pyplot import close
from temp_gui import Ui_MainWindow
import sys

#default value for skeletal extraction


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
        def accept(self):
                #get device input
                if (self.cpuOption.isChecked()):
                        self.gui.setDevice("cpu")
                elif (self.gpuOption.isChecked()):
                        self.gui.setDevice("gpu")
                
                #get model input
                if (self.cocoOption.isChecked()):
                        self.gui.setModel("COCO")
                elif (self.mpiOption.isChecked()):
                        self.gui.setModel("MPI")
                elif (self.body25Option.isChecked()):
                        self.gui.setModel("BODY_25")
                
                #get threshold value
                self.gui.setThreshold(self.thresholdBox.value())
                self.gui.modelLabel.setText(self.model)

        def setupUi(self, settingsDialog):
                settingsDialog.setObjectName("settingsDialog")
                settingsDialog.resize(461, 294)
                settingsDialog.setStyleSheet("background-color: rgb(44, 44, 44); color: rgb(255, 255, 255);")
                self.settingButton = QtWidgets.QDialogButtonBox(settingsDialog)
                self.settingButton.setEnabled(True)
                self.settingButton.setGeometry(QtCore.QRect(360, 30, 81, 161))
                self.settingButton.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(44, 44, 44); border-color: rgba(255, 255, 255, 0);")
                self.settingButton.setOrientation(QtCore.Qt.Vertical)
                self.settingButton.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
                self.settingButton.setObjectName("settingButton")
               
                self.deviceBox = QtWidgets.QGroupBox(settingsDialog)
                self.deviceBox.setGeometry(QtCore.QRect(20, 20, 311, 71))
                self.deviceBox.setObjectName("deviceBox")
               
                self.cpuOption = QtWidgets.QRadioButton(self.deviceBox)
                self.cpuOption.setGeometry(QtCore.QRect(20, 30, 95, 20))
                if (self.gui.device == "cpu"):
                        self.cpuOption.setChecked(True)
                self.cpuOption.setObjectName("cpuOption")
                self.gpuOption = QtWidgets.QRadioButton(self.deviceBox)
                self.gpuOption.setGeometry(QtCore.QRect(120, 30, 95, 20))
                if (self.gui.device == "gpu"):
                        self.gpuOption.setChecked(True)
                self.gpuOption.setObjectName("gpuOption")
                self.modelBox = QtWidgets.QGroupBox(settingsDialog)
                self.modelBox.setGeometry(QtCore.QRect(20, 120, 311, 71))
                self.modelBox.setObjectName("modelBox")
                #COCO model
                self.cocoOption = QtWidgets.QRadioButton(self.modelBox)
                self.cocoOption.setGeometry(QtCore.QRect(20, 30, 95, 20))
                if (self.gui.model == "COCO"):
                        self.cocoOption.setChecked(True)
                self.cocoOption.setObjectName("cocoOption")
                #MPI model
                self.mpiOption = QtWidgets.QRadioButton(self.modelBox)
                self.mpiOption.setGeometry(QtCore.QRect(120, 30, 95, 20))
                if (self.gui.model == "MPI"):
                        self.mpiOption.setChecked(True)
                self.mpiOption.setObjectName("mpiOption")
                #BODY_25
                self.body25Option = QtWidgets.QRadioButton(self.modelBox)
                self.body25Option.setGeometry(QtCore.QRect(210, 30, 95, 20))
                if (self.gui.model == "BODY_25"):
                        self.body25Option.setChecked(True)
                self.body25Option.setObjectName("body25Option")
                
                self.label = QtWidgets.QLabel(settingsDialog)
                self.label.setGeometry(QtCore.QRect(20, 240, 61, 16))
                self.label.setObjectName("label")
                self.thresholdBox = QtWidgets.QDoubleSpinBox(settingsDialog)
                self.thresholdBox.setGeometry(QtCore.QRect(90, 240, 241, 21))
                self.thresholdBox.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(44, 44, 44);")
                self.thresholdBox.setMinimum(0.0)
                self.thresholdBox.setSingleStep(0.01)
                self.thresholdBox.setProperty("value", self.gui.thres)
                self.thresholdBox.setObjectName("thresholdBox")

                self.retranslateUi(settingsDialog)
                self.settingButton.accepted.connect(self.accept) # type: ignore
                self.settingButton.rejected.connect(settingsDialog.reject) # type: ignore
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
                self.body25Option.setText(_translate("settingsDialog", "Body-25"))
                self.label.setText(_translate("settingsDialog", "Threshold"))


if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        settingsDialog = QtWidgets.QDialog()
        ui = Ui_settingsDialog()
        ui.setupUi(settingsDialog)
        settingsDialog.show()
        sys.exit(app.exec_())
