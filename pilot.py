from constants import F_WIDTH, F_HEIGHT, CROP_WIDTH, TIME_TIL_SEARCH, FBOX_Z, S, F, szX, szY, UDOffset
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
        cWidth = int(F_WIDTH / 2)
        cHeight = int(F_HEIGHT / 2)

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
            y = int(y * hR)
            w = int(wR * w)
            h = int(h * hR)

            # end coords are the end of the bounding box x & y
            end_cord_x = x + w
            end_cord_y = y + h
            end_size = w * 2

            # these are our target coordinates
            target_x = int((end_cord_x + x) / 2)
            target_y = int((end_cord_y + y) / 2) + UDOffset

            # This calculates the vector from your face to the center of the screen
            vTrue = np.array((cWidth, cHeight, FBOX_Z))
            vTarget = np.array((target_x, target_y, end_size))
            vDistance = vTrue - vTarget

            # for turning
            if vDistance[0] < -szX:
                self.yaw_velocity = S
            elif vDistance[0] > szX:
                self.yaw_velocity = -S
            else:
                self.yaw_velocity = 0

            # for up & down
            if vDistance[1] > szY:
                self.up_down_velocity = S
            elif vDistance[1] < -szY:
                self.up_down_velocity = -S
            else:
                self.up_down_velocity = 0

            # for forward back
            vel = vDistance[2]/FBOX_Z

            if vDistance[2] == 0:
                self.for_back_velocity = 0
            else:
                self.for_back_velocity = int((S + F)*vel)

            self.ui.draw_box(frame, x, y, end_cord_x,
                             end_cord_y, target_x, target_y)

        if len(faces) < 1:
            if self.last_face_seen < time.time() - (1000 * TIME_TIL_SEARCH):
                self.yaw_velocity = S*3
                height = int(self.tello.get_height().replace(
                    'ok', '').replace('dm', ''))
                if height < 10:
                    self.up_down_velocity = S
            else:
                self.yaw_velocity = 0
                self.up_down_velocity = 0

            self.for_back_velocity = 0
            print("NO TARGET")
