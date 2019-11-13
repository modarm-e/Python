import face_recognition
import cv2
import numpy as np

video_capture =cv2.VideoCapture(0)

myFace = face_recognition.load_image_file("my.jpg")
myFace_face_encoding= face_recognition.face_encodings(myFace)[0]

known_face_encodings=[myFace_face_encoding,]
known_face_names=["mj",]

face_locations=[]
face_encodings=[]
face_names=[]
process_this_frame=True

while True:
    ret, frame=video_capture.read()

    small_frame =cv2.resize(frame, (0,0), fx=0.25, fy=0.25) #왜 small?

    rgb_small_frame = small_frame[:,:,::-1]
###################################################################################
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        print("encodings",face_encodings)
        #face_names=[]
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
            print('face_distance',face_distances)
            best_match_index=np.argmin(face_distances)
            print('best_match_index',best_match_index)
            print('matches[best_match_index] : ',matches[best_match_index])
            if matches[best_match_index]:
                name=known_face_names[best_match_index]
                print('known_face_names[best_match_index] : ',known_face_names[best_match_index])
            face_names.append(name)
    
    process_this_frame= not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *=4
        right *=4
        bottom *=4
        left *=4

        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255),2)

        cv2.rectangle(frame, (left,bottom -35), (right,bottom) ,(0,0,255) , cv2.FILLED)
        font=cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255,255,255), 1)
    
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
