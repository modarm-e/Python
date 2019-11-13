import ctypes,cv2
import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class ShowVideo(QtCore.QObject):
    flag =0 
    camera = cv2.VideoCapture(0)

    ret,image=camera.read()
    height,width = image.shape[:2]

    VideoSignal1=QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self,parent=None):
        super(ShowVideo , self).__init__(parent)
    
    @QtCore.pyqtSlot()
    def startVideo(self):
        global image

        run_video = True
        while run_video:
            ret, image=self.camera.read()
            
            color_swapped_image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)

            loop=QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25,loop.quit)
            loop.exec_()
    
    # CAM_ID=0
    # def capture(camid=CAM_ID):
    #     cam=cv2.VideoCapture(camid)
    #     if cam.isOpened() == False:
    #         print('cant open the cam (%d)'&camid)
    #         return None
    #     ret, frame = cam.read()
    #     if frame is None:
    #         print('frame is not exist')
    #         return None
    #     cv2.imwrite('me.jpg')
    #     cam.release()
        

class ImageViewer(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image=QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0,self.image)
        self.image=QtGui.QImage()
        
    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self,image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image=image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    thread=QtCore.QThread()
    thread.start()
    vid=ShowVideo()
    vid.moveToThread(thread)

    image_viewer1= ImageViewer()

    vid.VideoSignal1.connect(image_viewer1.setImage)
    
    push_button1=QPushButton('start')
    push_button2=QtWidgets.QPushButton('end')
    push_button1.clicked.connect(vid.startVideo)
    # push_button2.clicked.disconnect(vid.startVideo)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)
    

    layout_widget=QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window=QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())



# ####### 레이아웃 공부
# class MyApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
    
#     def initUI(self):
#         self.statusBar().showMessage('Ready')
#         # self.setGeometry(000,000,300,200) # 위치, 크기 QMainWindow
#         self.setWindowTitle("My First Application") #제목설정
#         # self.move(300,300) #위치이동  QWidget
#         self.resize(400,200) #위젯 크기
#         self.show() #위젯 보여줌
#         self.center()

#     def center(self):    # 가운데 창 생성
#         qr=self.frameGeometry()   # 창정보를 가져옴
#         cp=QDesktopWidget().availableGeometry().center() #사용자 모니터 center확인
#         qr.moveCenter(cp)   # qr창을  center로 이동
#         self.move(qr.topLeft())     #현재창을 qr창의 위치로 이동

# if __name__ == '__main__':   # __name__ : 현재 모듈의 이름이 저장되는 내장변수 
#                              # 직접실행하면 __name__은 __main__이 된다. 
#     app= QApplication(sys.argv)     #어플리케이션 객체를 생성한다.
#     ex=MyApp()
#     sys.exit(app.exec_())

#######model
# detector = dlib.get_frontal_face_detector()
# predictor=dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

# # find face function 
# def find_faces(img):
#     dets = detector(img,1)
#     # 얼굴없으면 빈배열
#     if len(dets)==0:
#         return np.empty(0), np.empty(0), np.empty(0)

#     rects, shapes= [],[] 
#     shapes_np = np.zeros((len(dets),68,2), dtype=np.list)
#     for k, d in enumerate(dets):
#         rect=((d.left(),d.top()), (d.right(),d.bottom()))
#         rects.append(rect)
#         shape = predictor(img,d)

#         for i in range(68):
#             shapes_np[k][i]=(shape.part(i).x, shape.part(i).y)
#         shapes.append(shape)
#     return rects, shapes, shapes_np


# # face recognition
# def encode_faces(img, shapes):
#     face_descriptors=[]
#     for shape in shapes:
#         face_descriptor = facerec.compute_face_descriptor(img,shape)
#         face_descriptors.append(np.array(face_descriptor))
#     return np.array(face_descriptors)



#윈도우 장금
# ctypes.windll.user32.LockWorkStation()

#카메라 켜기
# capture=cv2.VideoCapture(0)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

# while True:
#     ret, frame = capture.read()
#     cv2.imshow("VideoFrame",frame)
#     if cv2.waitKey(1) > 0 : break

# capture.release()
# cv2.destroyAllWindows