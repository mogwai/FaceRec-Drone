from functools import wraps
import tello
from tello_control_ui import TelloUI
from faces import detect
import time
import threading
from threading import Timer

width = 970
height = 720

midX = width // 2
midY = height // 2
box = 100


class limit(object):
    class Exception(BaseException):
        pass

    def __init__(self, per_second=None, per_minute=None):
        self.period = 0.0
        self.max_calls = 0
        if per_second:
            self.period = 1.0
            self.max_calls = per_second
        elif per_minute:
            self.period = 60.0
            self.max_calls = per_minute
        else:
            raise limit.Exception("You must provide either per_second,"
                                  "per_minute or per_hour values.")

        self.calls_counter = 0
        self.last_call_time = None

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            now = time.time()
            delay = 0.0
            if self.last_call_time is not None:
                timedelta = now - self.last_call_time
                if timedelta <= self.period and self.calls_counter >= self.max_calls:
                    self.calls_counter = 0
                    delay = abs(self.period - timedelta)
            time.sleep(delay)
            self.last_call_time = time.time()
            f(*args, **kwargs)
            self.calls_counter += 1
        return wrapped


class DroneController():

    def __init__(self, drone):
        self.drone = drone
        self.receive_thread = threading.Thread(target=self._checkHeight)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def _checkHeight(self):
        while True:
            height = self.drone.get_height()
            print(height)
            if height < 3:
                self.drone.takeoff()
            time.sleep(5)

    def new_frame(self, frame):
        rects = detect(frame)

        if len(rects) < 1:
            return

        main_rect = None
        maxi = -1
        for r in rects:
            size = r.width() * r.height()
            if size > maxi:
                maxi = size
                main_rect = r

        x = main_rect.tl_corner().x + main_rect.width()//2
        y = main_rect.tl_corner().y + main_rect.height()//2
        self.handle_position(x, y, maxi)
        return rects

    @limit(per_second=1)
    def handle_position(self, x, y, size):
        print(x, y, size)
        t = self.drone
        if size < 80*80:
            t.move_forward(0.2)
        elif size > 100*100:
            t.move_backward(0.2)
        elif x < midX - 80:
            t.rotate_ccw(11)
        elif x > midX + 80:
            t.rotate_cw(11)
        elif y < midY:
            t.move_up(.15)
        elif y > midY + 50:
            t.move_down(.15)


def main():
    drone = tello.Tello('', 8889)
    ctrl = DroneController(drone)
    vplayer = TelloUI(drone, "./img/", ctrl.new_frame)
    vplayer.root.mainloop()


if __name__ == "__main__":
    main()
