import sys
import dlib

cnn_face_detector = dlib.cnn_face_detection_model_v1('./face_model.dat')

def detect(img):
    dets = cnn_face_detector(img, 1)
    rects = dlib.rectangles()
    rects.extend([d.rect for d in dets])
    return rects