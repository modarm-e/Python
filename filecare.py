import sys, os, shutil
from PyQt5.QtWidgets import QWidget, QApplication ,QTreeView, \
    QFileSystemModel, QVBoxLayout, QPushButton, QInputDialog, QLineEdit

class main(QWidget):
    def __init__(self):
        super().__init__()
        self.path="C:"
        self.index=None

        self.tv=QTreeView(self)  #변수지정
        self.model=QFileSystemModel()
        self.btnRen=QPushButton('이름바꾸기')
        self.btnDel=QPushButton("파일삭제")
        self.layout = QVBoxLayout()

        self.setUi() #유아이 지정
        self.setSlot() #슬롯 지정

    def setUi(self):
        self.setGeometry(300,300,700,350)
        self.setWindowTitle("QFileSystemModel")
        self.model.setRootPath(self.path) #모델의 루트 패스 할당
        self.tv.setModel(self.model)    #트리뷰 모델 보여줄곳 
        self.tv.setColumnWidth(0,250) # 가로를 넓게 만들어 줬다

        self.layout.addWidget(self.tv)
        self.layout.addWidget(self.btnDel)
        self.layout.addWidget(self.btnRen)
        self.setLayout(self.layout) #레이아웃 지정
    
    def setSlot(self):
        self.tv.clicked.connect(self.setIndex) # Clicked 가 QModelIndex로 connect 되어 setIndex메서드에 clicked값이 넘어간다
        self.btnRen.clicked.connect(self.ren)
        self.btnDel.clicked.connect(self.rm)
    
    def setIndex(self,index): #인덱스 값을 지정 | QmodelIndex의 값을 두번째 인자에 담는다  
         self.index=index #현재 클릭된 인덱스를 저장
    
    def ren(self):
        os.chdir(self.model.filePath(self.model.parent(self.index)))  #작업폴더 가지고 오기 | 내파일의 상위 폴더의 경로를 찾는다
        fname=self.model.fileName(self.index) #파일이름 가져오기
        text, res = QInputDialog.getText(self, "이름 바꾸기", "바꿀 이름을 입력하세요",
                                        QLineEdit.Normal, fname) #기본값, fame:파일이름들고옴
        if res:  #res : ok, no 변수 저장
            while True:
                self.ok = True
                for i in os.listdir(os.getcwd()): #os.getcwd() : 현재 내가 작업하고 있는 폴더 
                                                #os.listdir() : 이경로의 파일목록을 들고 오세요
                    print(i)
                    if i == text:
                        text, res=QInputDialog.getText(self, "중복 오류!", "바꿀 이름을 입력하세요", QLineEdit.Normal, text)
                    
                        if not res:
                            return
                        self.ok=False
                if self.ok:
                    break
            os.rename(fname, text)


    def rm(self): #파일삭제
        os.chdir(self.model.filePath(self.model.parent(self.index)))
        fname=self.model.fileName(self.index)
        try:
            if not self.model.isDir(self.index):
                os.unlink(fname)
                print(fname+ "파일 삭제")
            else:
                shutil.rmtree(fname)
                print(fname+"폴더 삭제") #폴더안에 한꺼번에 삭제
        except:
            print("에러발생")
app=QApplication([])
ex=main()
ex.show()
sys.exit(app.exec_())