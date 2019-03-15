import cv2
import numpy as np

from constants import (CROP_WIDTH, F_HEIGHT, F_WIDTH, FBOX_Z, UDOffset, fbCol,
                       fbStroke, szX, szY)
from djitellopy import Tello
from keyboard import KeyboardController
from pilot import Pilot


class FrontEnd:

    def __init__(self):
        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(10):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

    def run(self):

        frame_read = self.tello.get_frame_read()
        should_stop = False
        self.battery()

        while not should_stop:
            self.tello.send_rc_control()

            if frame_read.stopped:
                frame_read.stop()
                break

            frame = frame_read.frame
            
            # Draw the face bounding box
            cv2.rectangle(frame, (x, y), (end_cord_x,
                                          end_cord_y), fbCol, fbStroke)

            # Draw the target as a circle
            cv2.circle(frame, (targ_cord_x, targ_cord_y),
                       10, (0, 255, 0), 2)

            # Draw the safety zone
            cv2.rectangle(frame, (targ_cord_x - szX, targ_cord_y - szY),
                          (targ_cord_x + szX, targ_cord_y + szY), (0, 255, 0), fbStroke)

            # Draw the center of screen circle
            cv2.circle(frame, (F_WIDTH/2, F_HEIGHT/2), 10, (0, 0, 255), 2)

            # Display the resulting frame
            cv2.imshow('Hide n Seek', frame)

        self.exit()

    def battery(self):
        return self.tello.get_battery()[:2]

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
