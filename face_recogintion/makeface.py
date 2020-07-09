import sys ,cv2
import numpy as np
import face_recognition
import ctypes
import pickle
import os
from PyQt5 import QtWidgets ,QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# 이름 출력
def print_name():
        print(Application.known_face_names)
        print(Application.known_face_encodings)
        print(Application.unknown_face_names)
        print(Application.unknown_face_encodings)
        # 현재 list값을 출력

# 이름 읽기
def read_name():
    with open('name.p', 'rb') as file:
        # 'name.p'라는 파일을 읽어들이고 file이라는 이름으로 사용.
        print('이름 읽기')
        Application.known_face_names = pickle.load(file)
        Application.known_face_encodings = pickle.load(file)
        Application.unknown_face_names = pickle.load(file)
        Application.unknown_face_encodings = pickle.load(file)
        # 'name.p'에 있는 값을 하나씩 대입한다.
        print_name()

#이름 저장
def save_name():
    print('파일 저장')
    with open('name.p', 'wb') as file:
        # 'name.p'라는 파일을 수정/작성 하고 file이라는 이름으로 사용
        pickle.dump(Application.known_face_names, file)
        pickle.dump(Application.known_face_encodings, file)
        pickle.dump(Application.unknown_face_names, file)
        pickle.dump(Application.unknown_face_encodings, file)
        # 파일에 작성한다.
        print_name()

class Application(QMainWindow):
    known_face_encodings=[]
    known_face_names=[]
    unknown_face_encodings=[] 
    unknown_face_names=[] ######## 개발자 info추가

    def __init__(self):
        super(Application,self).__init__()
        self.title="you얼굴 recognition한다"
        self.setWindowTitle(self.title)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        # self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'face.ico'))
        self.setGeometry(150,150,650,550)
        menu=self.menuBar()
        menu_file=menu.addMenu("file")
        menu_info=menu.addMenu("_info")

        file_new=QAction("파일에서 찾기",self)
        file_new.triggered.connect(Widget.showDialog)
        # file_cap=QAction("웹캠으로 추가",self)
        # file_cap.triggered.connect(Widget.capDialog)
        file_ban=QAction("비허가자 추가",self)
        file_ban.triggered.connect(Widget.banDialog)
        file_new_del=QAction("사용자 삭제",self)
        file_new_del.triggered.connect(Widget.delShowDialog)
        file_ban_del=QAction("비허가자 삭제",self)
        file_ban_del.triggered.connect(Widget.delBanDialog)
        file_info=QAction('정보',self)
        file_info.triggered.connect(Widget.weAre)
        
        file_create=QMenu('추가',self)
        file_delete=QMenu('삭제',self)
        menu_user=QMenu('허가자',self)
        

        menu_user.addAction(file_new)
        # menu_user.addAction(file_cap)
        file_create.addMenu(menu_user)
        file_create.addAction(file_ban)
        file_delete.addAction(file_new_del)
        file_delete.addAction(file_ban_del)
        

        menu_file.addMenu(file_create)
        menu_file.addMenu(file_delete)
        menu_info.addAction(file_info)

        self.main_widget=Widget(self)
        self.setCentralWidget(self.main_widget)
        self.show()

        try:
            read_name()
            # 저장되어 있는 'name.p'파일을 읽어들인다.
            # 저장되어 있는 'name.p'파일이 없을 시 에러 발생 -> exception
        except IOError as err:
            with open('name.p', 'wb') as file:
                # 'name.p'파일이 존재하지 않으므로 수정/생성을 진행한다.
                print('최초 파일 생성')
                pickle.dump(self.known_face_names, file)
                pickle.dump(self.known_face_encodings, file)
                pickle.dump(self.unknown_face_names, file)
                pickle.dump(self.unknown_face_encodings, file)
                # 최초 생성 시 list들은 [][][][]로 빈 상태이다.
                print_name()
        except Exception as exceptError:
            print('Exception Error : ' + str(exceptError))


class Widget(QWidget):

    def __init__(self,parent):
        super(QWidget,self).__init__(parent)
    
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
        self.sldr.move(520,490)
        self.sldr.setMinimum(1)
        self.sldr.setMaximum(60)
        self.sldr.setValue(24)
        self.sldr.valueChanged.connect(self.setFps)

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
                Application.known_face_names.append(user)
                Application.known_face_encodings.append(ReadFace_encoding)
                print_name()
                save_name()
                #배열에 값이 append되면 save_name()함수로 수정/생성 작업 해준다.

            
                

    def delShowDialog(self):
        qid=QInputDialog()
        qa=QAction()
        qmb=QMessageBox()
        user,ok = QInputDialog.getText(qid,'허가자 삭제', "이미 등록된 허가자 : " + ", ".join(Application.known_face_names) + '\n이름을 적어주세요:')
        if user=='':
            QMessageBox.information(qmb,"오류","사용자명을 입력하지 않았습니다.")
        elif ok:
            print('user: ok',user,ok)
            index = Application.known_face_names.index(user)
            Application.known_face_names.remove(user)
            del Application.known_face_encodings[index]
            print_name()
            save_name()
            # 배열에 값이 append되면 save_name()함수로 수정/생성 작업 해준다.
                      
    def banDialog(self):
        qid=QInputDialog()
        qa=QAction()
        qmb=QMessageBox()
        user,ok = QInputDialog.getText(qid,'비허가자 추가','이름을 적어주세요:')
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
                Application.unknown_face_names.append(user)
                Application.unknown_face_encodings.append(ReadFace_encoding)
                print_name()
                save_name()
            # 배열에 값이 append되면 save_name()함수로 수정/생성 작업 해준다.

    def delBanDialog(self):
        qid=QInputDialog()
        qa=QAction()
        qmb=QMessageBox()
        user,ok = QInputDialog.getText(qid,'비허가자 삭제',"이미 등록된 비허가자 : " + ", ".join(Application.unknown_face_names) + '\n이름을 적어주세요:')
        if user=='':
            QMessageBox.information(qmb,"오류","사용자명을 입력하지 않았습니다.")
        elif ok:
            print('user: ok',user,ok)
            index = Application.unknown_face_names.index(user)
            Application.unknown_face_names.remove(user)
            del Application.unknown_face_encodings[index]
            print_name()
            save_name()
            # 배열에 값이 append되면 save_name()함수로 수정/생성 작업 해준다.


    def setFps(self):
        self.fps=self.sldr.value() 
        self.prt.setText("FPS "+str(self.fps)+"로 조정!")
        self.timer.stop() #타이머를 껏다가 다시킴
        self.timer.start(1000 / self.fps)


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
                    self.noone=0
                    #사용자 얼굴 인식
                    matches=face_recognition.compare_faces(Application.known_face_encodings , face_encoding , tolerance=0.53)  #인코딩차이값을 기준이되는 tolerance값과 비교해서 작으면 true, 크면 false로 배열생성
                    # self.name="Unknown"
                    print('matches',matches)
                    
                    face_distances=face_recognition.face_distance(Application.known_face_encodings , face_encoding)  # 얼굴인코딩값을 일단 비교해서 차이값을 배열로 표출
                    print('허가자',face_distances)
                    best_match_index=np.argmin(face_distances)  #배열값중 가장 작은 값의 인덱스를 리턴  
                                                                # |문제점  ++++++얼굴하나만 들고옴+++++++ 
                                                                # 여러사람의 정보를 들고오려면 여기서 unknown_encodings값을 비교한 matches를 들고와서 true값의 index저장후 같이 계산 해야됨
                                                                                                
                    
                    if matches[best_match_index]:
                        for(top,right,bottom,left)in self.face_locations:
                                top *=4
                                right *=4
                                bottom *=4
                                left *=4
                                cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
                                font=cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(frame,"Licensed",(left+6,bottom-6), font, 1.0,(255,255,255),1)
                        self.name=Application.known_face_names[best_match_index]
                        self.i=0
                        self.j=0
                    #비허가자
                    elif Application.unknown_face_names:
                        matches=face_recognition.compare_faces(Application.unknown_face_encodings,face_encoding, tolerance=0.56)
                        print('=========matches',matches)
                        face_distances=face_recognition.face_distance(Application.unknown_face_encodings,face_encoding)
                        best_match_index=np.argmin(face_distances)
                        print('=========비허가자',Application.unknown_face_names[best_match_index])
                        
                        if matches[best_match_index]:
                            for(top,right,bottom,left)in self.face_locations:
                                top *=4
                                right *=4
                                bottom *=4
                                left *=4
                                cv2.rectangle(frame,(left,top),(right,bottom),(255,0,0),2)
                                font=cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(frame,"Unlicensed",(left+6,bottom-6), font, 1.0,(255,255,255),1)

                            self.name=Application.unknown_face_names[best_match_index]
                            self.unPermission()
                        else:
                            for(top,right,bottom,left)in self.face_locations:
                                top *=4
                                right *=4
                                bottom *=4
                                left *=4
                                cv2.rectangle(frame,(left,top),(right,bottom),(150,150,0),2)
                                font=cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(frame,"Who are you",(left+6,bottom-6), font, 1.0,(255,255,255),1)
                            self.name="Unknown"
                            self.unknowncount()
                    else:
                        for(top,right,bottom,left)in self.face_locations:
                                top *=4
                                right *=4
                                bottom *=4
                                left *=4
                                cv2.rectangle(frame,(left,top),(right,bottom),(150,150,0),2)
                                font=cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(frame,"Who are you",(left+6,bottom-6), font, 1.0,(255,255,255),1)
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
            self.noone=0
            self.stop()
            ctypes.windll.user32.LockWorkStation()


    def unknowncount(self):
        self.i+=1
        print("i:",self.i)
        if self.i>6:
            self.yellowcard+=1
            self.i=0
            print("yellow:",self.yellowcard)
        if self.yellowcard%5==0:
            self.yellowcard=1
            self.stop()
            ctypes.windll.user32.LockWorkStation()

    def unPermission(self):
        self.j+=1
        print("j:",self.j)
        if self.j>4:
            self.redcard+=1
            self.j=0
            print("red:",self.redcard)
        if self.redcard%3==0:
            self.redcard=1
            self.stop()
            ctypes.windll.user32.LockWorkStation()
            

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))#영상을 비우고 
        self.timer.stop()   #타임을 끔
        self.prt.setText("사용중지")

    def weAre(self):
        mydialog=QDialog()
        mydialog.setGeometry(250,250,325,270)
        label1=QLabel("  잘생긴 파이썬 개발자")
        label2=QLabel("  ==> 안희건, 최민준")
        label3=QLabel("  버전:      ver.1")

        layout=QGridLayout()
        layout.addWidget(label1,0,0)
        layout.addWidget(label2,1,0)
        layout.addWidget(label3,2,0)
        mydialog.setLayout(layout)

        mydialog.setModal(True)
        mydialog.exec()
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    apl=Application()
    apl.show()
    sys.exit(app.exec_())