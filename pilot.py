from constants import F_WIDTH, F_HEIGHT, CROP_WIDTH, TIME_TIL_SEARCH, FBOX_Z
import numpy as np

from faces import detect
from image import resize_image_arr
import time


class Pilot:
    """
    Handles the controls for the drone
    """

    last_face_seen = time.time()

    def __init__(self, tello, ui):
        self.tello = tello
        self.ui = ui

    def on_frame(self, frame):
        # These are our center dimensions
        frameRet, im_height = resize_image_arr(frame, CROP_WIDTH)
        faces = detect(frameRet)

        # Record that we've seen a face
        if len(faces) > 0:
            self.last_face_seen = time.time()

        if len(faces) < 1:
            if self.last_face_seen < time.time() - (1000 * TIME_TIL_SEARCH):
                self.start_search()
            else:
                self.tello.yaw_velocity = 0
                self.tello.up_down_velocity = 0

            self.tello.forward_backward_velocity = 0
            return

        biggest = None
        maxArea = 0

        for i in range(len(faces)):
            (_, __, w, h) = faces[i]
            if w * h > maxArea:
                maxArea = w * h
                biggest = faces[i]

        self.move_to_face(*biggest, im_height)

        # Draw boxes on UI Frame
        for (x, y, w, h) in faces:
            self.ui.draw_box(frame, x, y, x+w, y+h,
                             F_WIDTH // 2, F_HEIGHT // 2)

    def move_to_face(self, x, y, w, h, im_height):
        cWidth = F_WIDTH // 2
        cHeight = F_HEIGHT // 2
        wR = F_WIDTH / CROP_WIDTH
        hR = F_HEIGHT / im_height

        # Put coordinates back into original scale
        x = int(x * wR)
        w = int(w * wR)
        y = int(y * hR)

        # Turning
        yawR = (x - cWidth) / cWidth
        self.tello.yaw_velocity = int(
            50 * yawR)

        # We want the height to be relative to our ideal position
        heightR = - (y - (cHeight-100)) / cHeight
        self.tello.up_down_velocity = int(40 * heightR)

        # We want the width to be our ideal width (Hacky depth perception)
        forwardR = (FBOX_Z - w) / FBOX_Z
        self.tello.forward_backward_velocity = int(50 * forwardR)

    def start_search(self):
        self.tello.yaw_velocity = 50*3
        height = int(self.tello.get_height().replace(
            'ok', '').replace('dm', ''))
        if height < 10:
            self.tello.up_down_velocity = 40
