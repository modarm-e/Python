import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow ,QAction, QMenu, QPushButton ,QFileDialog
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *


class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sid=QImage("mj.jpg").scaled(120,120)

        btn=QPushButton("이미지 변경",self)
        btn.resize(btn.sizeHint())
        btn.move(20,150)
        btn.clicked.connect(self.openFileNameDialog)

        self.setGeometry(1400,250,320,200)
        self.show()
    
    def paintEvent(self,event):  #이미지 물러올때마다 이미지를 그려야 하기 떄문에 이벤트를 재정의해서 사용
        painter=QPainter()
        painter.begin(self)
        self.drawImages(painter)
        painter.end()

    def drawImages(self,painter):  #이미지를 그려주는 메서드 | 항상 painter객체를 사용해서 그려준다
        painter.drawImage(5,15,self.sid)
        # painter.drawImage(self.sid.width() + 10,15, self.grayScale(self.sid.copy()))

    # def grayScale(self,image):
    #     for i in range(self.sid.width()):
    #         for j in range(self.sid.hight()):
    #             c=image.pixel(i,j)
    #             gray=qGray(c)
    #             alpha=qAlpha(c)
    #             image.setPixel(i,j,qRgba(gray,gray,gray,alpha))
    #     return image

    def openFileNameDialog(self): #해당 파일의 경로를 읽어 올수 있단
        fileName, ok = QFileDialog.getOpenFileName(self,"불러올 이미지를 선택하세요", "", \
                                            "All Files (*);;Python Files (*.py)")
            # ( 두번째 인수 : 설명글 ,세번째 인수: 파일이름에 미리 적혀있을것 입력
            #  네번째 인수: 앍어야할 파일의 타입을 지정할수 있다.  
            #  결과는 튜플형식으로 (경로,타입)이 나온다)
        if fileName:
            print("ok",ok)
            print(fileName)
            self.sid=QImage(fileName).scaled(120,120)

app=QApplication([])
ex=Exam()
sys.exit(app.exec_())






# class Exam(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#     def initUI(self):
#         menu=self.menuBar()
#         menu_file=menu.addMenu("file")
#         menu_edit=menu.addMenu("edit")

#         file_exit=QAction('Exit' , self) #메뉴 객체 생성
#         file_exit.setShortcut('Ctrl+Q') #단축키
#         file_exit.setStatusTip('무어ㅐ아')

#         new_txt = QAction("텍스트 파일", self)
#         new_py = QAction("파이썬 파일", self)

#         file_exit.triggered.connect(QCoreApplication.instance().quit)

#         file_new = QMenu("New",self) #서브그룹
#         file_new.addAction(new_txt) #서브메뉴
#         file_new.addAction(new_py)

#         menu_file.addMenu(file_new) #주메뉴등록
#         menu_file.addAction(file_exit) #주메뉴등록

#         self.resize(450,400)
#         self.show()

# app=QApplication([])
# ex=Exam()
# sys.exit(app.exec_())