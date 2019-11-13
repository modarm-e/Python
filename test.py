import dlib
import numpy as np
import cv2


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

def read_img(img_path):
  img = cv2.imread(img_path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  return img

def encode_face(img):
  dets = detector(img, 1)

  if len(dets) == 0:
    return np.empty(0)

  for k, d in enumerate(dets):
    # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img, d)
    face_descriptor = facerec.compute_face_descriptor(img, shape)

    return np.array(face_descriptor)

# main
img1_path = 'my.jpg' 


#img2_path = '/img/mo.jpg' 
img1 = read_img(img1_path)
img1_encoded = encode_face(img1)

#img2 = read_img(img2_path)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
  exit()

while True:
  ret, img2 = cap.read()
  if not ret:
    break
  cv2.imshow('window',img2)
  img2 = cv2.resize(img2, (640, img2.shape[0] * 640 // img2.shape[1]))
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
  img2_encoded = encode_face(img2)

  if len(img2_encoded) == 0:
    continue

  dist = np.linalg.norm(img1_encoded - img2_encoded, axis=0)

  print('%s, Distance: %s' % (dist < 0.6, dist))
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()
