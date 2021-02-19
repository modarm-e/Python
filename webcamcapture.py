import sys
# from PyQt4 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore ,QtGui
import cv2

class QtCapture(QWidget):
    def __init__(self):
        super().__init__()

        self.fps = 24
        self.cap = cv2.VideoCapture(0)

        self.video_frame = QLabel()
        lay = QVBoxLayout()
        # lay.setMargin(0)
        lay.addWidget(self.video_frame)
        self.setLayout(lay)

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        # My webcam yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(self).deleteLater()


class ControlWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.capture = None

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.startCapture)
        self.quit_button = QPushButton('End')
        self.quit_button.clicked.connect(self.endCapture)
        self.end_button = QPushButton('Stop')

        vbox =QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.end_button)
        vbox.addWidget(self.quit_button)
        self.setLayout(vbox)
        self.setWindowTitle('Control Panel')
        self.setGeometry(200,200,200,200)
        self.show()

    def startCapture(self):
        if not self.capture:
            self.capture = QtCapture()
            self.end_button.clicked.connect(self.capture.stop)
            # self.capture.setFPS(1)
            self.capture.setParent(self)
            self.capture.setWindowFlags(QtCore.Qt.Tool)
        self.capture.start()
        self.capture.setGeometry(400,250,200,200)
        self.capture.show()

    def endCapture(self):
        self.capture.deleteLater()
        self.capture = None


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = ControlWindow()
    sys.exit(app.exec_())