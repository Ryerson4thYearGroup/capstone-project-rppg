#Miaosen Zhou

from HB_Function import FBDunction
import cv2
#from imutils.video.pivideostream import PiVideoStream
#import imutils
import time
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')


class VideoCamera(object):
    def __init__(self, flip = False):
        self.video = cv2.VideoCapture(0)
        #self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    
    def get_frame(self):
        #image = self.flip_if_needed(self.vs.read())
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_frame = image[y:y+h,x:x+w]
        #image = cv2.resize(image, dsize=(320,240), interpolation=cv2.INTER_CUBIC)
        ret, jpeg = cv2.imencode('.jpg', image)
        for (x, y, w, h) in faces:
            image = image[y:y+h,x:x+w]
        image = cv2.resize(image, dsize=(320,240), interpolation=cv2.INTER_CUBIC)
        norm_image = cv2.normalize(image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        return jpeg,norm_image
