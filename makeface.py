import sys ,cv2, dlib
import numpy as np
import face_recognition
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

    
class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        myFace=face_recognition.load_image_file("my.jpg")
        myFace_face_encoding=face_recognition.face_encodings(myFace)[0]
        
        self.known_face_encodings=[myFace_face_encoding]
        self.known_face_names=["mj"]

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

        if self.process_this_frame:
            self.face_locations=face_recognition.face_locations(rgb_small_frame)
            self.face_encodings=face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            #self.face_names=[]
            for face_encoding in self.face_encodings:
                matches=face_recognition.compare_faces(self.known_face_encodings , face_encoding)
                self.name="Unknown"

                face_distances=face_recognition.face_distance(self.known_face_encodings , face_encoding)
                best_match_index=np.argmin(face_distances)
                if matches[best_match_index]:
                    self.name=self.known_face_names[best_match_index]
                self.face_names.append(self.name)
                print(self.name)
        self.prt.setText('사용자 : '+self.name)
        self.process_this_frame = not self.process_this_frame
        img=QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix=QPixmap.fromImage(img)
        self.frame.setPixmap(pix)

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))#영상을 비우고 
        self.timer.stop()   #타임을 끔
        self.prt.setText("사용중지")

    
if __name__ == '__main__':
    app=QApplication(sys.argv)
    wd=Widget()
    sys.exit(app.exec_())