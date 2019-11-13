import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QCoreApplication


class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn=QPushButton("push me!", self)
        btn.resize(btn.sizeHint())
        btn.move(200,180)#절대좌표


        #클릭 QtCore 모듈이용
        btn.clicked.connect(QCoreApplication.instance().quit)#객체호출  
                                                    # quit: 창 끄기  //QCloseEvent와 다른이벤트
        self.resize(500,500)
        self.setWindowTitle("두번째")
        self.show()

    def closeEvent(self,QCloseEvent):
        ans = QMessageBox.question(self,"종료확인","종료하시겠습니까?"
                                  ,QMessageBox.Yes | QMessageBox.No , QMessageBox.Yes)
                                    # yes 이벤트 , No이벤트, 기본값 )
        if ans == QMessageBox.Yes: #상수라서 가능
            QCloseEvent.accept()  #클로즈 이벤트 발생
        else:
            QCloseEvent.ignore()  # 이벤트 무시



app=QApplication(sys.argv)
w=Exam()
sys.exit(app.exec_())