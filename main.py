import dlib, cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects

###모델
#얼굴 탐지 모델
detector = dlib.get_frontal_face_detector()
#얼굴 랜드마크 탐지 모델
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
#얼굴 인식 모델
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')


###### 얼굴을 찾는 함수
def find_faces(img):
    dets = detector(img, 1) # dets에 얼굴찾는 결과물들이 들어감
    print('얼굴 갯수: ',dets)
    #만약 얼굴을 하나도 못찾았다고 하면 빈배열을 반환해줌
    if len(dets) ==0:
        return np.empty(0), np.empty(0), np.empty(0)
    
    #얼굴결과물을 저장할 변수들을 설정하기
    rects, shapes= [],[]
    shapes_np = np.zeros((len(dets),68, 2), dtype=np.int) #68개점을 구하는 함수
    #얼굴갯수 만큼 루프돌기     | for in enumerate(객체): 리스트의 순서와 값을 전달하는 기능
    for k,d in enumerate(dets):
        rect=((d.left(),d.top()),(d.right(),d.bottom()))
        rects.append(rect)
        #shape에 68개 점이 나옴  | img = 사진, d=사각형
        shape=sp(img,d)

        #랜드마크(눈,코,입,턱선,눈썹) 결과물을 shpaes에 추가
        for i in range(68):
            shapes_np[k][i]=(shape.part(i).x, shape.part(i).y)
        shapes.append(shape)
    #결과물 반환
    return rects,shapes, shapes_np

 
###### 얼굴을 인코딩하는 함수   
# 얼굴찾는 68개점을 인코더에 넣으면 128개의 벡터가 나옴 이벡터간의 거리가 
# 얼마나 머냐 가깝냐에따라 사람을 구분함
def encode_faces(img,shapes):
    face_descriptors=[]
    for shape in shapes:
                        # facerec모델의 cumpute_face_descriptor(img,shape)을 돌려준다 : 얼굴을 인코딩한다
                        # @img: 전체 사진 , shape: 랜드마크 결과 
        face_descriptor = facerec.compute_face_descriptor(img,shape)
                        # 결과값을 numpy.array로 바꿔서 리스트에 쌓음
        face_descriptors.append(np.array(face_descriptor))
        
        #값 반환
        return np.array(face_descriptors)


#실행과정
""" 전체사진에서 사람이 여러명 있다면 
1. Face Detection: 을 통해서 얼굴을 찾고
2. Face Landmark Detection을 통해서 얼굴 랜드마크 찾고 shapes 변수에 넣기
3. Face Encoding : computer_face_descriptor을 통해서 얼굴 인코딩하기 
    (사진,얼굴 랜드마크)넣어 face_descriptor을 구하고 반환
 """



#Compute Saved Feace Edscriptions
img_paths={
    'nayeon': 'img/na.jpg',
    'momo': 'img/mo.jpg',
    'cheyoung': 'img/chang.jpg'
}
descs={ 
    'nayeon':None,
    'momo':None,
    'cheyoung':None
}

for name, img_path in img_paths.items():
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr,  cv2.COLOR_BGR2RGB)

    _, img_shapes, _ = find_faces(img_rgb)
    descs[name]=encode_faces(img_rgb, img_shapes)[0]
np.save('img/descs.npy',descs)
print(descs)

#Compute Input
img_bgr = cv2.imread('img/namochang.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
print("출력 사진 입력")
rects, shapes, _ = find_faces(img_rgb)
descriptors=encode_faces(img_rgb, shapes)


#Visualize Output
fig, ax = plt.subplots(1,figsize=(20,20))
ax.imshow(img_rgb)

for i , desc in enumerate(descriptors):
    found = False
    for name, saved_desc in descs.items():
        dist = np.linalg.norm([desc] - saved_desc, axis=1) #유클리디안 거리

        if dist < 0.6:
            found=True

            text=ax.text(rects[i][0][0], rects[i][0][0], name, 
                color='b', fontsize=40, fontweight='bold')
            text.set_path_effects([path_effects.Stroke(linewidth=10, 
                foreground='white'), path_effects.Normal()])
            rect = patches.Rectangle(rects[i][0], 
                    rects[i][1][1]-rects[i][0][1], rects[i][1][0] - rects[i][0][0], 
                    linewidth=2, edgecolor='w',facecolor='none')
            ax.add_patch(rect)
            break
    if not found:
        ax.text(rects[i][0][0], rects[i][0][1], 'unknown',
            color='r',fontsize=20,fontweight='bold')
        
        rect = patches.Rectangle(rects[i][0], 
            rects[i][1][1]-rects[i][0][1],
            rects[i][1][0] - rects[i][0][0], 
            linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

plt.axis('off')
plt.savefig('output.png')
plt.show()
