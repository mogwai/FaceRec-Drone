from dlib import get_frontal_face_detector

cnn_face_detector = get_frontal_face_detector()


def detect(img):
    dets = cnn_face_detector(img, 1)
    arr = []
    for i in range(len(dets)):
        c = dets[i]
        tr = c.tl_corner()
        arr.append((tr.x, tr.y, c.width(), c.height()))
    return arr
