import numpy as np
import cv2

from camera import Camera
from stabiliser import Stabiliser
from face_cascade import FaceCascade

COLOUR_RECT_FACE = (255,0,0)
COLOUR_RECT_FACE_SELECTED = (0,0,255)

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
        
class App:
    def __init__(self):
        self.cam = Camera()
        self.face_cascade = FaceCascade()

    def process_frame(self):
        img = self.cam.capture_image()

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.get_faces(img_gray)
        
        img_faces = gray_to_bgr(img_gray.copy())

        # render rect around all faces in blue
        for face in faces:
            x,y,w,h = face
            cv2.rectangle(img_faces, (x,y), (x+w, y+h), COLOUR_RECT_FACE, 2)

        # find the largest face
        has_face, face = get_largest_face(faces)

        img_face_cropped = np.zeros_like(img)
        
        if not has_face:
            # todo: let stabiliser determine if there's no face
            img_face = np.zeros_like(img)
            img_face_porthole = np.zeros_like(img)
        else:
            # copy the detected face to a separate image
            x,y,w,h = face

            # rect around selected face in red
            # todo: feed this to stabiliser and render output of stabiliser in red
            cv2.rectangle(img_faces, (x,y), (x+w, y+h), COLOUR_RECT_FACE_SELECTED, 2)
            
            # copy the area of the face
            img_face_cropped[y:y+h, x:x+w] = img[y:y+h, x:x+w]

            # resize face
            width = img.shape[1]
            height = img.shape[0]
            img_face = cv2.resize(img[y:y+h, x:x+w], (width, height))

            # add porthole  
            img_face_porthole = img_face.copy()
            radius = int(min(width, height)/2)
            cv2.circle(img_face_porthole, (int(width/2), int(height/2)), radius, (255,255,255), 3)

        # combine images
        video_feeds = np.vstack((
            np.hstack((img, gray_to_bgr(img_gray), img_faces)),
            np.hstack((img_face_cropped, img_face, img_face_porthole))
        ))
        
        return video_feeds
    