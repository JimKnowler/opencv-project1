import cv2

class FaceCascade:
    def __init__(self):
        self._cascade = cv2.CascadeClassifier('./resources/haarcascade_frontalface_default.xml')
    
    def get_faces(self, img_gray):
        faces = self._cascade.detectMultiScale(img_gray, 1.1, 4)

        return faces
    