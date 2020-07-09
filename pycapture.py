
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# import makethis
import sys ,cv2, dlib
import numpy as np
import face_recognition
import ctypes
import pickle

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.title="pyqt5 QDialog"
        self.left=500
        self.top=200
        self.width=300
        self.height=250
        # self.iconName="home.png"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left,self.top,self.width,self.height)

        vbox = QVBoxLayout()
        self.btn=QPushButton('open second dialog')
        # self.btn.setFont(QtGui.QFont('sanserif',15))
        self.btn.clicked.connect(self.openSecondDialog)

        vbox.addWidget(self.btn)

        self.setLayout(vbox)
        self.show()

    def openSecondDialog(self):
        mydialog=QDialog()
        mydialog.setModal(True)
        mydialog.exec()


App=QApplication(sys.argv)
widnow=Window()
sys.exit(App.exec())