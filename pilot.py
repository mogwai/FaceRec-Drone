from constants import F_WIDTH, F_HEIGHT, CROP_WIDTH, TIME_TIL_SEARCH, FBOX_Z, NUM_FACES
import numpy as np

from faces import detect
from image import resize_image_arr
import time
from memory import LimitedMemory


class Pilot:
    """
    Handles the controls for the drone
    """
    last_face_seen = time.time()
    _face_memory = LimitedMemory(NUM_FACES)

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
            if time.time() - self.last_face_seen >= TIME_TIL_SEARCH:
                self.start_search()
            else:
                self.tello.yaw_velocity = 0
                self.tello.up_down_velocity = 0

            self.tello.forward_backward_velocity = 0
            return

        biggest = None
        maxArea = 0
        wR = F_WIDTH / CROP_WIDTH
        hR = F_HEIGHT / im_height

        for i in range(len(faces)):
            (x, y, w, h) = faces[i]

            # Put coordinates back into original scale
            x = int(x * wR)
            w = int(w * wR)
            y = int(y * hR)
            h = int(h * hR)
            faces[i] = (x, y, w, h)

            if w * h > maxArea:
                maxArea = w * h
                biggest = faces[i]

            mem = np.array([*faces[i], time.time()])
            self._face_memory.append(mem)

        self.move_to_face(*biggest)

        # Draw boxes on UI Frame
        for (x, y, w, h) in faces:
            self.ui.draw_box(frame, x, y, x+w, y+h,
                             F_WIDTH // 2, F_HEIGHT // 2)

    def move_to_face(self, x, y, w, h):
        cWidth = F_WIDTH // 2
        cHeight = F_HEIGHT // 2

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
        # Basic level of searching
        self.tello.yaw_velocity = 65
        arr = []
        memory = np.array(self._face_memory)
        
        # Use basic search (Spinning)
        if not len(memory):
            return
        
        # Filter by the times that 
        memory = memory[np.where([time.time() - i[-1] < 8 for i in memory])]
        
        # Use basic search (Spinning)
        if not len(memory):
            return
        
        movX = self.tello.yaw_velocity
        movY = self.tello.up_down_velocity
        newpos = memory - [movX, movY, 0, 0, 0]

        # Work out the vector to the next position as long as its nearby
        newpos = newpos[::-1]
        for i in range(len(newpos)-1):
            p = newpos[i]
            p1 = newpos[i + 1]
            dist = np.linalg.norm(p1 - p)
            if dist <= 100:
                arr.append(p1 - p)
            else:
                break

        # Use basic search (Spinning)
        if not len(arr):
            return

        # Get average vector
        avgV = np.mean(arr, axis=1)
        
        # Apply it to tello movement
        self.tello.yaw_velocity = 65 * (avgV[0] / avgV[0])
        self.tello.up_down_velocity = 30 * (avgV[1] / avgV[1])
