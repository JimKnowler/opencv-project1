import cv2


class Camera:
    def __init__(self, width = 640, height = 480):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.cap = cap

    def capture_image(self):
        attempts = 0
        while True:
            success, img = self.cap.read()

            if success:
                break
            else:
                attempts += 1
                print('failed attempt ', attempts)
                
                if attempts > 3:
                    raise Exception("unable to acquire image from video camera")
        
        return img