import numpy as np
import cv2

from camera import Camera
from stabiliser import Stabiliser
from face_cascade import FaceCascade
from porthole import Porthole

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

COLOUR_RECT_FACE = (255,0,0)
COLOUR_RECT_FACE_SELECTED = (0,0,255)
COLOUR_RECT_PORTHOLE = (0,255,255)
COLOUR_CIRCLE_PORTHOLE = (255,255,255)

def gray_to_bgr(img):
    # convert 1 channel grayscale to 3 channel BGR
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
class App:
    def __init__(self):
        self._cam = Camera(IMAGE_WIDTH, IMAGE_HEIGHT)
        self._face_cascade = FaceCascade()
        self._stabiliser = Stabiliser()
        porthole = Porthole(IMAGE_WIDTH, IMAGE_HEIGHT)
        porthole.set_padding(10)
        self._porthole = porthole

    def process_frame(self):
        img = self._cam.capture_image()

        # detect all faces in a grayscale version of captured image
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.get_faces(img_gray)

        # render rect around all faces in blue
        img_faces = gray_to_bgr(img_gray.copy())
        for face in faces:
            x,y,w,h = face
            cv2.rectangle(img_faces, (x,y), (x+w, y+h), COLOUR_RECT_FACE, 2)

        # use Stabiliser to decide where the face currently is in the image
        has_face, face = self._stabiliser.process(faces)

        # create the cropped face image, resized face image + porthole image
        img_face_cropped = np.zeros_like(img)
        if not has_face:
            img_face = np.zeros_like(img)
            img_face_porthole = np.zeros_like(img)
        else:
            x,y,w,h = face

            # rect around selected face in red
            cv2.rectangle(img_faces, (x,y), (x+w, y+h), COLOUR_RECT_FACE_SELECTED, 2)

            # get the porthole for the face
            self._porthole.set_face(face)
            px, py, pw, ph = self._porthole.get_bounding_box()

            # copy the area of the porthole bounding box
            img_face_cropped[py:py+ph, px:px+pw] = img[py:py+ph, px:px+pw]

            # rect around porthole in yellow
            cv2.rectangle(img_faces, (px,py), (px+pw, py+ph), COLOUR_RECT_PORTHOLE, 2)

            # resize porthole-face to full size square
            width = img.shape[1]
            height = img.shape[0]
            square_width = min(width,height)
            img_face_box = cv2.resize(img[py:py+ph, px:px+pw], (square_width, square_width))

            # add border around square to create image with same dimensions as image from camera
            bx = int((width - square_width) / 2)
            by = int((height - square_width) / 2)
            img_face = cv2.copyMakeBorder(img_face_box, by, by, bx, bx, cv2.BORDER_CONSTANT, (0,0,0))

            # add circle around porthole  
            img_face_porthole = img_face.copy()
            radius = int(min(width, height)/2)
            cv2.circle(img_face_porthole, (int(width/2), int(height/2)), radius, COLOUR_CIRCLE_PORTHOLE, 3)

        # combine images into a video wall that shows stages of processing
        video_wall = np.vstack((
            np.hstack((img, gray_to_bgr(img_gray), img_faces)),
            np.hstack((img_face_cropped, img_face, img_face_porthole))
        ))
        
        return video_wall
    