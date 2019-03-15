import cv2


class KeyboardController:
    def __init__(self, tello):
        self.cv2 = cv2
        self.tello = tello
        self.speed = 1

    def check_key(self):
         # Listen for key presses
        k = cv2.waitKey(20)
        S = 20
        try:
            speed = int(k)
            if speed < 7 and speed > -1:
                self.speed = speed * 10
        except:
            pass

        # Quit the software
        if k == 27:
            raise Exception("Esc Pressed")

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

        # S & W to fly forward & back
        if k == ord('w'):
            self.tello.forward_backward_velocity = int(S * self.speed)
        elif k == ord('s'):
            self.tello.forward_backward_velocity = -int(S * self.speed)
        else:
            self.tello.forward_backward_velocitya = 0

        # a & d to pan left & right
        if k == ord('d'):
            self.tello.yaw_velocity = int(S * self.speed)
        elif k == ord('a'):
            self.tello.yaw_velocity = -int(S * self.speed)
        else:
            self.tello.yaw_velocity = 0

        # Q & E to fly up & down
        if k == ord('e'):
            self.tello.up_down_velocity = int(S * self.speed)
        elif k == ord('q'):
            self.tello.up_down_velocity = -int(S * self.speed)
        else:
            self.tello.up_down_velocity = 0

        # c & z to fly left & right
        if k == ord('c'):
            self.tello.left_right_velocity = int(S * self.speed)
        elif k == ord('z'):
            self.tello.left_right_velocity = -int(S * self.speed)
        else:
            self.tello.left_right_velocity = 0

        return k != -1
