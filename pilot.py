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

    def __init__(self, tello):
        self.tello = tello

    def on_frame(self, frame):
        # These are our center dimensions
        cWidth = int(F_WIDTH / 2)
        cHeight = int(F_HEIGHT / 2)

        frameRet, im_height = resize_image_arr(frame, CROP_WIDTH)
        faces = detect(frameRet)

        wR = F_WIDTH / CROP_WIDTH
        hR = F_HEIGHT / im_height

        for (x, y, w, h) in faces:
            # Record that we've seen a face
            self.last_face_seen = time.time()

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
            targ_cord_x = int((end_cord_x + x) / 2)
            targ_cord_y = int((end_cord_y + y) / 2) + UDOffset

            # This calculates the vector from your face to the center of the screen
            vTrue = np.array((cWidth, cHeight, FBOX_Z))
            vTarget = np.array((targ_cord_x, targ_cord_y, end_size))
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

        # if there are no faces
        if len(faces) < 1:
            if self.last_face_seen < time.time() - (1000 * TIME_TIL_SEARCH):
                self.yaw_velocity = S*3
                height = int(self.tello.get_height().replace(
                    'ok', '').replace('dm', ''))
                if height < 20:
                    self.up_down_velocity = S
            else:
                self.yaw_velocity = 0
                self.up_down_velocity = 0

            self.for_back_velocity = 0
            print("NO TARGET")
