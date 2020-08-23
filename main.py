import numpy as np
import cv2
import camera

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

def process_frame(cam, face_cascade):
    img = cam.capture_image()
        
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)
    
    img_faces = gray_to_bgr(img_gray.copy())

    # rect around all faces in blue
    for face in faces:
        x,y,w,h = face
        cv2.rectangle(img_faces, (x,y), (x+w, y+h), (255,0,0), 2)

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
        cv2.rectangle(img_faces, (x,y), (x+w, y+h), (0,0,255), 2)
        
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

def main():
    cam = camera.Camera()
    cam.init()

    face_cascade = cv2.CascadeClassifier('./resources/haarcascade_frontalface_default.xml')

    while True:
        video_feeds = process_frame(cam, face_cascade)

        cv2.imshow('opencv-project1', video_feeds)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # user has pressed 'q' to exit
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
