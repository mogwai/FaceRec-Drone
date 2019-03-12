import numpy as np
from PIL import Image


def resize_image_arr(arr, width=500):
    im = Image.fromarray(arr)
    im = resize_image(im, width)
    return np.asarray(im, dtype="uint8")


def resize_image(im, width=500):
    wpercent = (width / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(wpercent)))
    im.thumbnail((width, hsize), Image.ANTIALIAS)
    return im, hsize
