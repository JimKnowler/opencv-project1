import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

face_cascade = cv2.CascadeClassifier('./resources/haarcascade_frontalface_default.xml')

def gray_to_bgr(img):
    # convert 1 channel grayscale to 3 channel BGR
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

def get_largest_face(faces):
    max_area = 0
    index = -1

    for i, (_,_,w,h) in enumerate(faces):
        area = w * h
        if area > max_area:
            index = i
            max_area = area
    
    if -1 == index:
        return (False, None)
    else:
        return (True, faces[i])

while True:
    success, img = cap.read()

    if not success:
        raise "unable to acquire image from video camera"

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)
    
    img_faces = gray_to_bgr(img_gray.copy())

    # rect around all faces in blue
    for face in faces:
        x,y,w,h = face
        cv2.rectangle(img_faces, (x,y), (x+w, y+h), (255,0,0), 2)

    # find the largest face
    has_face, face = get_largest_face(faces)
    
    if not has_face:
        img_face = np.zeros_like(img)
    else:
        # copy the detected face to a separate image
        x,y,w,h = face
        img_face_cropped = img[y:y+h, x:x+w]
        img_face = cv2.resize(img_face_cropped, (img.shape[1], img.shape[0]))

        # rect around selected face in red
        # todo: feed this to stabiliser and render output of stabiliser in red
        cv2.rectangle(img_faces, (x,y), (x+w, y+h), (0,0,255), 2)

    # combine images
    img_blank = np.zeros_like(img)

    video_feeds = np.vstack((
        np.hstack((img, gray_to_bgr(img_gray), img_faces)),
        np.hstack((img_blank, img_blank, img_blank))
    ))

    cv2.imshow('opencv-project1', video_feeds)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

