import cv2

class KeyboardController:
    def __init__(self, tello):
        self.cv2 = cv2
        self.tello = tello

    def on_frame(self, frame):
         # Listen for key presses
        k = cv2.waitKey(20)

        # Press 0 to set distance to 0
        if k == ord('0'):
            if not OVERRIDE:
                print("Distance = 0")
                tDistance = 0

        # Press 1 to set distance to 1
        if k == ord('1'):
            if OVERRIDE:
                oSpeed = 1
            else:
                print("Distance = 1")
                tDistance = 1

        # Press 2 to set distance to 2
        if k == ord('2'):
            if OVERRIDE:
                oSpeed = 2
            else:
                print("Distance = 2")
                tDistance = 2

        # Press 3 to set distance to 3
        if k == ord('3'):
            if OVERRIDE:
                oSpeed = 3
            else:
                print("Distance = 3")
                tDistance = 3

        # Press 4 to set distance to 4
        if k == ord('4'):
            print("Distance = 4")
            tDistance = 4

        # Press 5 to set distance to 5
        if k == ord('5'):
            print("Distance = 5")
            tDistance = 5

        # Press 6 to set distance to 6
        if k == ord('6'):
            print("Distance = 6")
            tDistance = 6

        # Press T to take off
        if k == ord('t'):
            print("Taking Off")
            self.tello.takeoff()
            self.tello.get_battery()
            self.send_rc_control = True

        # Press L to land
        if k == ord('l'):
            print("Landing")
            self.tello.land()
            self.send_rc_control = False

        # Press Backspace for controls override
        if k == 8:
            if not OVERRIDE:
                OVERRIDE = True
                print("OVERRIDE ENABLED")
            else:
                OVERRIDE = False
                print("OVERRIDE DISABLED")

        if OVERRIDE:
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

        # Quit the software
        if k == 27:
            should_stop = True
