import sys ,cv2, dlib
import numpy as np
import face_recognition
import ctypes
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Application(QMainWindow):
    known_face_encodings=[]
    known_face_names=[]
    unknown_face_encodings=[] 
    unknown_face_names=[] ######## 개발자 info추가
    def __init__(self):
        super().__init__()
        self.title="you얼굴 recognition한다"
        self.setWindowTitle(self.title)
        self.setGeometry(150,150,650,550)

        menu=self.menuBar()
        menu_file=menu.addMenu("file")

        file_new=QAction("사용자 추가",self)
        file_new.triggered.connect(Widget.showDialog)
        file_ban=QAction("비허가자 추가",self)
        file_ban.triggered.connect(Widget.banDialog)
        
        menu_file.addAction(file_new)
        menu_file.addAction(file_ban)

        self.main_widget=Widget(self)
        self.setCentralWidget(self.main_widget)
        self.show()


class Widget(QWidget):

    def __init__(self,parent):
        super(QWidget,self).__init__(parent)
        
        ##아이유얼굴 기본으로 추가한것
        # IUFace=face_recognition.load_image_file("img/chang.jpg")
        # IUFace_face_encoding=face_recognition.face_encodings(IUFace)[0]
        
        # Application.known_face_encodings=[IUFace_face_encoding]
        # Application.known_face_names=["강동원"]
        

        self.i=0
        self.j=0
        self.yellowcard=1
        self.redcard=1
        self.noone=0
        self.readname=""
        self.face_locations=[]
        self.face_encodings=[]
        self.face_names=[]
        self.name=''
        self.process_this_frame=True
        self.initUI()

    
    
    def initUI(self):
        self.cpt=cv2.VideoCapture(0)
        self.fps=60
        self.sens=300

        self.frame=QLabel(self) # 얼굴 표출 화면
        self.frame.resize(640,480)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)
        
        self.btn_on=QPushButton("켜기",self)
        self.btn_on.resize(100,25)
        self.btn_on.move(5,490)
        self.btn_on.clicked.connect(self.start)

        self.btn_off=QPushButton("끄기",self)
        self.btn_off.resize(100,25)
        self.btn_off.move(110,490)
        self.btn_off.clicked.connect(self.stop)

        self.prt=QLabel(self)
        self.prt.resize(200,25)
        self.prt.move(215,490)

        self.sldr=QSlider(Qt.Horizontal,self)
        self.sldr.resize(100,25)
        self.sldr.move(415,490)
        self.sldr.setMinimum(1)
        self.sldr.setMaximum(60)
        self.sldr.setValue(24)
        self.sldr.valueChanged.connect(self.setFps)

        self.sldr1=QSlider(Qt.Horizontal,self)
        self.sldr1.resize(100,25)
        self.sldr1.move(520,490)
        self.sldr1.setMinimum(50)
        self.sldr1.setMaximum(500)
        self.sldr1.setValue(300)
        self.sldr1.valueChanged.connect(self.setSens)

        self.setGeometry(150,150,650,540)
        self.setWindowTitle("Cam_exam")
        self.show()

    def showDialog(self):
        qid=QInputDialog()
        qa=QAction()
        qmb=QMessageBox()
        user,ok = QInputDialog.getText(qid,'사용자 추가','이름을 적어주세요:')
        if user=='':
            QMessageBox.information(qmb,"오류","사용자명을 입력하지 않았습니다.")
        elif ok:
            print('user: ok',user,ok)
            qfd=QFileDialog()
            fileName, _ = QFileDialog.getOpenFileName(qfd,"불러올 이미지를 선택하세요", "", "Images (*png, *.jpg)")  
            if fileName:
                print(fileName)
                
                ReadFace=face_recognition.load_image_file(fileName)
                ReadFace_encoding=face_recognition.face_encodings(ReadFace)[0]
                # print(ReadFace_encoding)
                Application.known_face_names.append(user)
                Application.known_face_encodings.append(ReadFace_encoding)
                print(Application.known_face_names)
    def banDialog(self):
        qid=QInputDialog()
        qa=QAction()
        qmb=QMessageBox()
        user,ok = QInputDialog.getText(qid,'사용자 추가','이름을 적어주세요:')
        if user=='':
            QMessageBox.information(qmb,"오류","사용자명을 입력하지 않았습니다.")
        elif ok:
            print('user: ok',user,ok)
            qfd=QFileDialog()
            fileName, _ = QFileDialog.getOpenFileName(qfd,"불러올 이미지를 선택하세요", "", "Images (*png, *.jpg)")  
            if fileName:
                print(fileName)
                
                ReadFace=face_recognition.load_image_file(fileName)
                ReadFace_encoding=face_recognition.face_encodings(ReadFace)[0]
                # print(ReadFace_encoding)
                Application.unknown_face_names.append(user)
                Application.unknown_face_encodings.append(ReadFace_encoding)
                print(Application.unknown_face_names)

    def setFps(self):
        self.fps=self.sldr.value() 
        self.prt.setText("FPS "+str(self.fps)+"로 조정!")
        self.timer.stop() #타이머를 껏다가 다시킴
        self.timer.start(1000 / self.fps)

    def setSens(self):
        self.sens=self.sldr1.value()
        self.prt.setText("감도 "+str(self.sens)+"로 조정!")

    def start(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 /self.fps) #24분의 1초마다 반복

    def nextFrameSlot(self):
        
        _, frame=self.cpt.read()
        small_frame=cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb_small_frame=small_frame[ :, :,::-1]
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        if len(Application.known_face_names)==0:
            self.name="사용자를 추가해주세요."
        else:

        # if self.process_this_frame:
            self.face_locations=face_recognition.face_locations(rgb_small_frame)
            self.face_encodings=face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            
            if len(self.face_locations)==0:
                self.noperson()
            else:
                for face_encoding in self.face_encodings:
                    
                    #사용자 얼굴 인식
                    matches=face_recognition.compare_faces(Application.known_face_encodings , face_encoding)
                    # self.name="Unknown"
                    print('matches',matches)
                    
                    face_distances=face_recognition.face_distance(Application.known_face_encodings , face_encoding)
                    print('허가자',face_distances)
                    best_match_index=np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        self.name=Application.known_face_names[best_match_index]
                        self.i=0
                        self.j=0
                    #비허가자
                    elif Application.unknown_face_names:
                        matches=face_recognition.compare_faces(Application.unknown_face_encodings,face_encoding)
                        print('=========matches',matches)
                        face_distances=face_recognition.face_distance(Application.unknown_face_encodings,face_encoding)
                        best_match_index=np.argmin(face_distances)
                        print('=========비허가자',Application.unknown_face_names[best_match_index])
                        
                        if matches[best_match_index]:
                            self.name=Application.unknown_face_names[best_match_index]
                            self.unPermission()
                        else:
                            self.name="Unknown"
                            self.unknowncount()
                    else:
                        self.name="Unknown"
                        self.unknowncount()
                    self.face_names.append(self.name)


                    

        self.prt.setText('사용자 : '+self.name)
        self.process_this_frame = not self.process_this_frame
        img=QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix=QPixmap.fromImage(img)
        self.frame.setPixmap(pix)
    
    def noperson(self):
        self.noone+=1
        if self.noone>500:
            self.stop()
            ctypes.windll.user32.LockWorkStation()


    def unknowncount(self):
        self.i+=1
        print("i:",self.i)
        if self.i>4:
            self.yellowcard+=1
            self.i=0
            print("yellow:",self.yellowcard)
        if self.yellowcard%5==0:
            self.stop()
            self.yellowcard=1
            ctypes.windll.user32.LockWorkStation()

    def unPermission(self):
        self.j+=1
        print("j:",self.j)
        if self.j>4:
            self.redcard+=1
            self.j=0
            print("red:",self.redcard)
        if self.redcard%3==0:
            self.stop()
            self.redcard=1
            ctypes.windll.user32.LockWorkStation()
            

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))#영상을 비우고 
        self.timer.stop()   #타임을 끔
        self.prt.setText("사용중지")

    
if __name__ == '__main__':
    app=QApplication(sys.argv)
    apl=Application()
    sys.exit(app.exec_())