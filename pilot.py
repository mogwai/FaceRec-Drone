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
        cWidth = F_WIDTH // 2
        cHeight = F_HEIGHT // 2

        frameRet, im_height = resize_image_arr(frame, CROP_WIDTH)
        faces = detect(frameRet)

        wR = F_WIDTH / CROP_WIDTH
        hR = F_HEIGHT / im_height

        # Record that we've seen a face
        if len(faces) > 0:
            self.last_face_seen = time.time()

        for (x, y, w, h) in faces:

            # Put coordinates back into original scale
            x = int(x * wR)
            w = int(w * wR)
            y = int(y * hR)
            h = int(h * hR)

            # for turning
            yawR = (x - cWidth) / cWidth
            self.tello.yaw_velocity = int(
                50 * yawR)

            # We want the height to be relative to our ideal position
            heightR = - (y - (cHeight-100)) / cHeight
            self.tello.up_down_velocity = int(40 * heightR)

            # We want the width to be our ideal width (Hacky depth perception)
            forwardR = (FBOX_Z - w) / FBOX_Z
            self.tello.forward_backward_velocity = int(50 * forwardR)

            print("Position", (x, y, w))
            print("Target", (cWidth, cHeight-100, FBOX_Z))
            print("DISANCE", (x - cWidth,
                              y - cHeight, FBOX_Z - w))
            print("RATIOS", (yawR, heightR, forwardR))
            print("VELOCITIES",
                  self.tello.yaw_velocity,
                  self.tello.up_down_velocity,
                  self.tello.forward_backward_velocity)

            # Draw box on UI Frame
            self.ui.draw_box(frame, x, y, x+w, y+h, cWidth, cHeight)

        if len(faces) < 1:
            if self.last_face_seen < time.time() - (1000 * TIME_TIL_SEARCH):
                self.tello.yaw_velocity = S*3
                height = int(self.tello.get_height().replace(
                    'ok', '').replace('dm', ''))
                if height < 10:
                    self.tello.up_down_velocity = S
            else:
                self.tello.yaw_velocity = 0
                self.tello.up_down_velocity = 0

            self.tello.forward_backward_velocity = 0
