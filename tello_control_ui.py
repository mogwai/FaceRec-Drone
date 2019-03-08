from PIL import Image
from PIL import ImageTk
import Tkinter as tki
from Tkinter import Toplevel, Scale
import threading
import datetime
import cv2
import os
import time
import platform


class TelloUI:
    """Wrapper class to enable the GUI."""

    def __init__(self, tello, outputpath, frame_func):
        """
        Initial all the element of the GUI,support by Tkinter

        :param tello: class interacts with the Tello drone.

        Raises:
            RuntimeError: If the Tello rejects the attempt to enter command mode.
        """
        self.handle_frame = frame_func
        self.tello = tello  # videostream device
        # the path that save pictures created by clicking the takeSnapshot button
        self.outputPath = outputpath
        self.frame = None  # frame read from h264decoder and used for pose recognition
        self.thread = None  # thread of the Tkinter mainloop
        self.stopEvent = None

        # control variables
        self.distance = 0.1  # default distance for 'move' cmd
        self.degree = 30  # default degree for 'cw' or 'ccw' cmd

        # if the flag is TRUE,the auto-takeoff thread will stop waiting for the response from tello
        self.quit_waiting_flag = False

        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None
        self.canvas = None

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("TELLO Controller")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        # the sending_command will send command to tello every 5 seconds
        self.sending_command_thread = threading.Thread(
            target=self._sendingCommand)

    def videoLoop(self):
        """
        The mainloop thread of Tkinter
        Raises:
            RuntimeError: To get around a RunTime error that Tkinter throws due to threading.
        """
        try:
            # start the thread that get GUI image and drwa skeleton
            time.sleep(0.5)
            self.sending_command_thread.start()
            while not self.stopEvent.is_set():
                system = platform.system()

            # read the frame for GUI show
                self.frame = self.tello.read()
                if self.frame is None or self.frame.size == 0:
                    continue

                # transfer the format from frame to image
                image = Image.fromarray(self.frame)
                rects = self.handle_frame(self.frame)
                self._updateGUIImage(image, rects)
        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")

    def drawRects(self, rects):
        if self.canvas is None:
            self.canvas = tki.Canvas(self.root)
            self.canvas.place(x=0, y=0)
        else:
            self.canvas.delete('all')

        if rects is None or len(rects) < 1:
            return

        for rect in rects:
            x1 = rect.tl_corner().x
            y1 = rect.tl_corner().y
            x2 = rect.br_corner().x
            y2 = rect.br_corner().y
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         outline="#f11", width=2)

    def _updateGUIImage(self, image, rects):
        """
        Main operation to initial the object of image,and update the GUI panel 
        """
        image = ImageTk.PhotoImage(image)

        if self.panel is None:
            self.panel = tki.Label(image=image)
            self.panel.image = image
            self.panel.place(x=0, y=0)
        # otherwise, simply update the panel
        else:
            self.panel.configure(image=image)
            self.panel.image = image
        self.drawRects(rects)

    def _sendingCommand(self):
        """
        start a while loop that sends 'command' to tello every 5 second
        """

        while True:
            self.tello.send_command('command')
            time.sleep(5)

    def _setQuitWaitingFlag(self):
        """
        set the variable as TRUE,it will stop computer waiting for response from tello  
        """
        self.quit_waiting_flag = True

    def telloTakeOff(self):
        return self.tello.takeoff()

    def telloLanding(self):
        return self.tello.land()

    def telloFlip_l(self):
        return self.tello.flip('l')

    def telloFlip_r(self):
        return self.tello.flip('r')

    def telloFlip_f(self):
        return self.tello.flip('f')

    def telloFlip_b(self):
        return self.tello.flip('b')

    def telloCW(self, degree):
        return self.tello.rotate_cw(degree)

    def telloCCW(self, degree):
        return self.tello.rotate_ccw(degree)

    def telloMoveForward(self, distance):
        return self.tello.move_forward(distance)

    def telloMoveBackward(self, distance):
        return self.tello.move_backward(distance)

    def telloMoveLeft(self, distance):
        return self.tello.move_left(distance)

    def telloMoveRight(self, distance):
        return self.tello.move_right(distance)

    def telloUp(self, dist):
        return self.tello.move_up(dist)

    def telloDown(self, dist):
        return self.tello.move_down(dist)

    def updateTrackBar(self):
        self.my_tello_hand.setThr(self.hand_thr_bar.get())

    def updateDistancebar(self):
        self.distance = self.distance_bar.get()
        print 'reset distance to %.1f' % self.distance

    def updateDegreebar(self):
        self.degree = self.degree_bar.get()
        print 'reset distance to %d' % self.degree

    def on_keypress_w(self, event):
        print "up %d m" % self.distance
        self.telloUp(self.distance)

    def on_keypress_s(self, event):
        print "down %d m" % self.distance
        self.telloDown(self.distance)

    def on_keypress_a(self, event):
        print "ccw %d degree" % self.degree
        self.tello.rotate_ccw(self.degree)

    def on_keypress_d(self, event):
        print "cw %d m" % self.degree
        self.tello.rotate_cw(self.degree)

    def on_keypress_up(self, event):
        print "forward %d m" % self.distance
        self.telloMoveForward(self.distance)

    def on_keypress_down(self, event):
        print "backward %d m" % self.distance
        self.telloMoveBackward(self.distance)

    def on_keypress_left(self, event):
        print "left %d m" % self.distance
        self.telloMoveLeft(self.distance)

    def on_keypress_right(self, event):
        print "right %d m" % self.distance
        self.telloMoveRight(self.distance)

    def on_keypress_enter(self, event):
        if self.frame is not None:
            self.registerFace()
        self.tmp_f.focus_set()

    def onClose(self):
        """
        set the stop event, cleanup the camera, and allow the rest of

        the quit process to continue
        """
        print("[INFO] closing...")
        self.stopEvent.set()
        self.tello.land()
        del self.tello
        self.root.quit()
