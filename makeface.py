import sys ,cv2, dlib
import numpy as np
import face_recognition
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Application(QMainWindow):
    known_face_encodings=[]
    known_face_names=[]
    unknown_face_encodings=[] ########비허가자 추가 & 윈도우 잠금 ctypes.windll.user32.LockWorkStation()
    unknown_face_names=[] ######## 개발자 info추가
    def __init__(self):
        super().__init__()
        self.title="you얼굴 recognition한다"
        self.setWindowTitle(self.title)
        self.setGeometry(150,150,650,550)

        IUFace=face_recognition.load_image_file("sana.jpg")
        IUFace_face_encoding=face_recognition.face_encodings(IUFace)[0]
        known_face_encodings=[IUFace_face_encoding]
        known_face_names=["SANA"]

        menu=self.menuBar()
        menu_file=menu.addMenu("file")

        file_new=QAction("사용자 추가",self)
        file_new.triggered.connect(Widget.showDialog)
        file_ban=QAction("비허가 사용자 추가",self)
        file_ban.triggered.connect(Widget.banDialog)

        menu_file.addAction(file_new)
        menu_file.addAction(file_ban)

        self.main_widget=Widget(self)
        self.setCentralWidget(self.main_widget)
        self.show()


class Widget(QWidget):

    def __init__(self,parent):
        super(QWidget,self).__init__(parent)
        

        #내얼굴 허가자로 추가 한것
        myFace=face_recognition.load_image_file('my.jpg')
        myFace_encoding=face_recognition.face_encodings(myFace)

        Application.known_face_encodings=[myFace_encoding]
        Application.known_face_names=["MJ"]
        # ##사나얼굴 밴으로 추가한것
        # SanaFace=face_recognition.load_image_file("sana.jpg")
        # SanaFace_face_encoding=face_recognition.face_encodings(SanaFace)[0]
        
        # Application.unknown_face_encodings=[SanaFace_face_encoding]
        # Application.unknown_face_names=["IU"]
        

        self.i=0
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
        # _, self.img_O = self.cpt.read()
        # self.img_O= cv2.cvtColor(self.img_O, cv2.COLOR_RGB2GRAY)
        # cv2.imwrite('img_O.jpg',self.img_O) 
        # my.jpg읽어오는걸로 바꾸면 됌

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
            print('newUser: ok',user,ok)
            qfd=QFileDialog()
            fileName, _ = QFileDialog.getOpenFileName(qfd,"불러올 이미지를 선택하세요", "", "Images (*png, *.jpg)")  
            if fileName:
                print(fileName)
                
                ReadFace=face_recognition.load_image_file(fileName)
                ReadFace_encoding=face_recognition.face_encodings(ReadFace)[0]
                print(ReadFace_encoding)
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
            print('banUser: ok',user,ok)
            qfd=QFileDialog()
            fileName, _ = QFileDialog.getOpenFileName(qfd,"불러올 이미지를 선택하세요", "", "Images (*png, *.jpg)")  
            if fileName:
                print(fileName)
                
                ReadFace=face_recognition.load_image_file(fileName)
                ReadFace_encoding=face_recognition.face_encodings(ReadFace)[0]
                print(ReadFace_encoding)        
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
        self.i+= 1
        _, frame=self.cpt.read()
        small_frame=cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb_small_frame=small_frame[ :, :,::-1]
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.process_this_frame:
            self.face_locations=face_recognition.face_locations(rgb_small_frame)
            self.face_encodings=face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            self.face_names=[]  #필요없느거 아닌가??
            for face_encoding in self.face_encodings:
                
                matches=face_recognition.compare_faces(Application.known_face_encodings,face_encoding)
                self.name="Unknown"
                self.i=0
                face_distances=face_recognition.face_distance(Application.known_face_encodings , face_encoding)
                best_match_index=np.argmin(face_distances)
                print(face_distances)
                print(best_match_index)
                self.name=Application.known_face_names[best_match_index]
                self.face_names.append(self.name) #필요없는거 아닌가?
                if matches[best_match_index]:
                    self.name=Application.known_face_names[best_match_index]
                print(self.name)




                # matches=face_recognition.compare_faces(Application.known_face_encodings , face_encoding)
                # unmatches=face_recognition.compare_faces(Application.unknown_face_encodings,face_encoding)
                # print(matches)
                # print(unmatches)
                # if len(matches)==0:
                #     self.name='사용자를 추가하세요 '
                # elif matches[0]==True:
                #     face_distances=face_recognition.face_distance(Application.known_face_encodings , face_encoding)
                #     best_match_index=np.argmin(face_distances)
                #     print(face_distances)
                #     print(best_match_index)
                #     self.name=Application.known_face_names[best_match_index]  
                # elif matches[0]==False:
                #     if len(unmatches)!=0:
                #         self.name="Unkown"
                #         ban_face_distances=face_recognition.face_distance(Application.unknown_face_encodings,face_encoding)
                #         ban_best_match_index=np.argmin(ban_face_distances)
                #         print(ban_face_distances)
                #         print(ban_best_match_index)
                #         if unmatches[ban_best_match_index]:
                #             self.name=Application.unknown_face_names[ban_best_match_index]   
                
                # self.name="Unknown"
                # print(matches)
                # print(len(matches))
                # if matches[0]==True:
                #     face_distances=face_recognition.face_distance(Application.known_face_encodings , face_encoding)
                #     best_match_index=np.argmin(face_distances)
                #     print(face_distances)
                #     print(best_match_index)
                #     self.name=Application.known_face_names[best_match_index]
                # elif matches[0]==False:
                #     ban_face_distances=face_recognition.face_distance(Application.unknown_face_encodings,face_encoding)
                #     ban_best_match_index=np.argmin(ban_face_distances)
                #     self.name=Application.unknown_face_names[ban_best_match_index]
                #     #print(matches)  #등록된 얼굴 맞는지 true , false값 반환
                #     # if matches[0]==True:
                # else:
                #     self.name="Unkown"
                ############################################################################################################
        self.prt.setText('사용자 : '+self.name)
        self.process_this_frame = not self.process_this_frame
        img=QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix=QPixmap.fromImage(img)
        self.frame.setPixmap(pix)
        #print(self.i)

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))#영상을 비우고 
        self.timer.stop()   #타임을 끔
        self.prt.setText("사용중지")

    
if __name__ == '__main__':
    app=QApplication(sys.argv)
    apl=Application()
    sys.exit(app.exec_())