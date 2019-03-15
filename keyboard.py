import cv2

from constants import tDistance, S


class KeyboardController:
    def __init__(self, tello):
        self.cv2 = cv2
        self.tello = tello

    def check_key(self):
         # Listen for key presses
        k = cv2.waitKey(20)

        try:
            speed = int(k)
            if speed < 7 and speed > -1:
                tDistance = speed
        except:
            pass

        # Quit the software
        if k == 27:
            raise "Esc Pressed"

        # Press T to take off
        if k == ord('t'):
            print("Taking Off")
            self.tello.takeoff()
            self.tello.get_battery()

        # Press L to land
        if k == ord('l'):
            print("Landing")
            self.tello.land()

        # Press Backspace for controls override
        if k == 8:
            if not OVERRIDE:
                OVERRIDE = True
                print("OVERRIDE ENABLED")
            else:
                OVERRIDE = False
                print("OVERRIDE DISABLED")

        oSpeed = tDistance

        # S & W to fly forward & back
        if k == ord('w'):
            self.for_back_velocity = int(S * oSpeed)
        elif k == ord('s'):
            self.for_back_velocity = -int(S * oSpeed)
        else:
            self.for_back_velocity = 0

        # a & d to pan left & right
        if k == ord('d'):
            self.yaw_velocity = int(S * oSpeed)
        elif k == ord('a'):
            self.yaw_velocity = -int(S * oSpeed)
        else:
            self.yaw_velocity = 0

        # Q & E to fly up & down
        if k == ord('e'):
            self.up_down_velocity = int(S * oSpeed)
        elif k == ord('q'):
            self.up_down_velocity = -int(S * oSpeed)
        else:
            self.up_down_velocity = 0

        # c & z to fly left & right
        if k == ord('c'):
            self.left_right_velocity = int(S * oSpeed)
        elif k == ord('z'):
            self.left_right_velocity = -int(S * oSpeed)
        else:
            self.left_right_velocity = 0
