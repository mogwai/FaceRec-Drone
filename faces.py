import sys
import dlib
import requests

cnn_face_detector = dlib.cnn_face_detection_model_v1('./face_model.dat')

model_url = 'http://dlib.net/files/mmod_human_face_detector.dat.bz2'

def download():
  himion0

def detect(img):
    dets = cnn_face_detector(img, 1)
    rects = dlib.rectangles()
    rects.extend([d.rect for d in dets])
    return rects