import cv2
import numpy as np

from constants import (CROP_WIDTH, F_HEIGHT, F_WIDTH, FBOX_Z, fbCol, fbStroke)
from djitellopy import Tello
from keyboard import KeyboardController
from pilot import Pilot
from ml.depth import predict_depth

class FrontEnd:

    def __init__(self):
        # Init Tello object that interacts with the Tello drone
        tello = Tello(logging=False)
        self.tello = tello
        if not self.tello.connect():
            raise Exception("Tello not connected")

        if not self.tello.set_speed(10):
            raise Exception("Not set speed to lowest possible")

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            raise Exception("Could not stop video stream")

        if not self.tello.streamon():
            raise Exception("Could not start video stream")

        self.frame_read = tello.get_frame_read()
        self.pilot = Pilot(tello, self)
        self.key_ctrl = KeyboardController(tello)

    def run(self):
        self.tello.get_battery()
        while 1:
            self.draw()

        self.exit()

    def draw(self):
        self.tello.send_rc_control()

        if self.frame_read.stopped:
            self.frame_read.stop()

        frame = self.frame_read.frame
        np.save('frame', frame)
        depth = predict_depth(frame)
        print(depth.min()/25.5)

        # TODO add some delay here to allow user to control 
        if not self.key_ctrl.check_key(): 
            self.pilot.on_frame(frame, depth)

        # Draw the center of screen circle
        cv2.circle(depth, (220//2, 220//2), 10, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Hide n Seek', depth)
        cv2.imshow('Real', frame)

    def draw_box(self, frame, x, y, end_cord_x, end_cord_y, target_x, target_y):
        # Draw the face bounding box
        cv2.rectangle(frame, (x, y), (end_cord_x,
                                      end_cord_y), fbCol, fbStroke)

    def exit(self):
            # On exit, print the battery
        self.tello.get_battery()

        # When everything done, release the capture
        cv2.destroyAllWindows()

        # Call it always before finishing. I deallocate resources.
        self.tello.end()


def main():
    frontend = FrontEnd()
    frontend.run()


if __name__ == '__main__':
    main()
