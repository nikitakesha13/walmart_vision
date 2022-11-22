import sys, cv2
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import QTimer, Qt

enter_coordinates = (120, 50)
radius = 8
color = (255, 0, 0)
thickness = -1
frame_no = 0
x_coor = 10
y_coor = 10

class Play(QMainWindow):
    def __init__(self, gui):
        super().__init__()
        self.initUI(gui)

    def initUI(self, gui):
        self.statusBar().showMessage("Ready")
        self.setGeometry(50, 50, 1200, 1200)
        self.setWindowTitle("Statusbar")
        self.vidWindow = QLabel(gui)
        self.vidWindow.setGeometry(20, 20, 1000, 1000)
        self.maskWindow = QLabel(gui)
        self.maskWindow.setGeometry(20, 20, 640, 480)
        self.maskWindow.setStyleSheet("background-color: rgba(0,0,0,0%)")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.maskWindow.setFont(font)
        self.maskWindow.setText("Message is on the mask Qlabel object")
        self.msgLabel = QLabel(self)
        self.msgLabel.setGeometry(675, 300, 100, 20)

        self.marker_label = QLabel(self)

        pixmap = QPixmap(100, 100)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
        painter.drawEllipse(pixmap.rect().adjusted(4, 4, -4, -4))
        painter.end()

        self.marker_label.setPixmap(pixmap)
        self.marker_label.adjustSize()
        self.marker_label.hide()
        self.marker_label.raise_()

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.frame_rate = 5
        self.show()
        self.start()

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            img = img.scaled(640, 600, Qt.KeepAspectRatio)
            frame = cv2.circle(frame,(10, 10),10,color,thickness)
            pix = QPixmap.fromImage(img)
            self.vidWindow.setPixmap(pix)
            key = cv2.waitKey(1)
                
            if key == ord('q') or key == 27:
                print("A")

    def mousePressEvent(self, event):
        self.msgLabel.setText("Mouse Clicked!")
        if self.vidWindow.rect().contains(event.pos()):
            self.marker_label.move(event.pos() - self.marker_label.rect().center())
            self.marker_label.show()
        super().mousePressEvent(event)

    def start(self):
        rate = int(1000.0 / self.frame_rate)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(rate)

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        super().closeEvent(event)
    
    def keyPressEvent(self, event):
        if self.cap.isOpened() and event.key() == Qt.Key_Escape:
            self.cap.release()
        return super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Play()
    sys.exit(app.exec_())