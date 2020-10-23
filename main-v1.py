from tkinter import *
from PIL import Image, ImageTk
from imageai.Detection.Custom import CustomObjectDetection
import cv2
import random
import os
import time
import serial

Arduino = serial.Serial('COM3', 9600)

status = False

object_name = ''
object_probability = 0


def exit_app(e):
    exit(0)


def test(self, path):
    global object_name
    global status

    pics = os.listdir(path)
    p_picked = random.choice(pics)
    img = Image.open(path + "\\" + str(p_picked))
    object_name = ''
    #  Hur länge info bilden ska synas
    self.delay = 2000
    status = False
    return img

class Gui:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.attributes('-fullscreen', True)
        self.window.config(background="#736f6f")
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = Camera(self.video_source)
        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(window, width=self.vid.width, height=self.vid.height, highlightbackground="grey")
        self.canvas.pack()

        # Buttons
        self.window.bind('<Escape>', exit_app)
        self.window.bind('q', exit_app)

        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        global status, img
        global object_name
        global object_probability
        global Arduino
        start_time = time.time()
        arduino_data = Arduino.read()
        decoded = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
        self.delay = 15
        ret, frame = self.vid.get_frame()

        if ret:
            print("Arduino value: " + decoded)
            print("Status: " + str(status))
            #  Om sensor triggar
            if int(object_probability) > 89:
                status = True
            if object_name != '' and int(object_probability) > 89 and status:
                 #  Kanske ändra att object_probibility är statisk inuti
                 #  Bestäm fil beroende på sensor
                if decoded == 'K':
                    if object_name == 'Kartong':
                        path = os.getcwd() + "\\Kartong"
                        img = test(self, path)
                        status = False
                elif decoded == 'M':
                    if object_name == 'Metall':
                        path = os.getcwd() + "\\Metall"
                        img = test(self, path)
                        status = False
                elif decoded == 'P':
                    if object_name == 'Plast':
                        path = os.getcwd() + "\\Plast"
                        img = test(self, path)
                        status = False
                else:
                    if object_name == 'Kartong':
                        path = os.getcwd() + "\\Kartongslut"
                    elif object_name == 'Metall':
                        path = os.getcwd() + "\\Metallslut"
                    elif object_name == 'Plast':
                        path = os.getcwd() + "\\Plastslut"
                    pics = os.listdir(path)
                    p_picked = random.choice(pics)
                    img = Image.open(path + "\\" + str(p_picked))
            else:
                img = Image.fromarray(frame)

            fpsinfo = "FPS: " + str(1.0 / (time.time() - start_time))
            print(fpsinfo)
            img = img.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.window.after(self.delay, self.update)


class Camera:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = window.winfo_screenwidth()
        self.height = window.winfo_screenheight()

    def get_frame(self, ret=None):
        if self.vid.isOpened():
            global object_name
            global object_probability
            ret, frame = self.vid.read()
            frame = cv2.flip(frame, 1)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                detected_image, detections = detector.detectObjectsFromImage(
                                        input_image=frame,
                                        input_type="array",
                                        output_type="array",
                                        display_percentage_probability=True)

                for detection in detections:
                    (x1, y1, x2, y2) = detection["box_points"]
                    object_name = detection["name"]
                    object_probability = detection["percentage_probability"]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    fontscale = 1
                    org = (x1 + 6, y1 - 6)
                    thickness = 1
                    if int(object_probability) < 50:
                        color = (0, 0, 255)
                    elif int(50 < object_probability < 75):
                        color = (0, 230, 230)
                    else:
                        color = (0, 179, 0)

                    cv2.putText(
                                frame,
                                object_name + ": " + str(int(object_probability)) + "%",
                                org,
                                font,
                                fontscale,
                                color,
                                thickness)

                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
# Load dataset/model
detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("manafv5.h5")
detector.setJsonPath("detection_config.json")
detector.loadModel()

window = Tk()
Gui(window, "Techrecycle")
