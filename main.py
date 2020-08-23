import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)     # width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)     # height

face_cascade = cv2.CascadeClassifier('./resources/haarcascade_frontalface_default.xml')

while True:
    success, img = cap.read()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)

    max_area = 0
    index = -1

    for i, (x,y,w,h) in enumerate(faces):
        area = w * h
        if area > max_area:
            index = i
            max_area = area

    if index == -1:
        img_face = np.zeros_like(img)
    else:
        # copy the detected face to a separate image
        face = faces[index]
        x,y,w,h = face
        img_face_cropped = img[y:y+h, x:x+w]
        img_face = cv2.resize(img_face_cropped, (img.shape[1], img.shape[0]))

        # add rect to img captured from camera
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 2)

    rectangle = np.hstack((img, img_face))

    cv2.imshow('Video + Face', rectangle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

