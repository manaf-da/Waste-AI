#   TechRecycle
#   Skapad av Joakim Söderlund, Manaf Dawud, Reza Aalami
#
#   Applikationen använder sig av ImageAI biblioteket för att kunna upptäcka objekt från en tränad modul och
#   med hjälp av en arduino avläsa sensorer för att ge användaren feedback beroende på hens val av sortering
#
from tkinter import *
from PIL import Image, ImageTk
from imageai.Detection.Custom import CustomObjectDetection
import threading
import cv2
import random
import os
import serial

#  Öppna kommunikationen med Arduino genom port COM3/USB/SERIAL
Arduino = serial.Serial('COM3', 57600, timeout=0)

#  Globala variabler
decoded = ''
status = False

#  Globala variabler
object_name_temp = ''
object_name = ''
object_probability = 0

#  Exit_app avslutar applikationen då e = Esc eller q
def exit_app(e):
    exit(0)

#  Väljer en slumpad bild ifrån path
def random_p_img(self, path):
    global object_name
    global status

    #  Hittar alla bilder som kan väljas
    pics = os.listdir(path)
    #  Väljer en av dessa bilder
    p_picked = random.choice(pics)
    #  Ladda in den valda bilden till variabeln img
    img = Image.open(path + "\\" + str(p_picked))
    object_name = ''
    #  Hur länge info bilden ska synas på displayen
    self.delay = 2000
    status = False
    return img

#  Läser inkommande data från arduino
def read_arduino():
    global Arduino
    global decoded
    #  Läser arduino data
    arduino_data = Arduino.read()
    #  Decodar datan till rätt format
    decoded = str(arduino_data[0:len(arduino_data)].decode("utf-8"))

#  GUI klass med bakomliggande funktioner
class Gui(threading.Thread):
    #  Ändra 0 till -1 eller 1 om flera kameror finns aktiva.
    def __init__(self, window, window_title, video_source=0):
        threading.Thread.__init__(self)
        #  Skapar mainwindow
        self.window = window
        #  Sätter titeln för applikationsfönstret
        self.window.title(window_title)
        #  Specificerar storleken på applikationsfönstret
        self.window.attributes('-fullscreen', True)
        #  Anger bakgrundsfärg
        self.window.config(background="#736f6f")
        #  Specificerar vilken kamera som används på datorn, default är det 0 om endast 1 kamera existerar på systemet
        self.video_source = video_source

        # Öppna video feed, default startas kameran
        self.vid = Camera(self.video_source)
        #  Skapar en canvas med storlek av kamerans input
        self.canvas = Canvas(window, width=self.vid.width, height=self.vid.height, highlightbackground="grey")
        self.canvas.pack()

        # Knappar, specificerar att knapparna Esc och q avslutar applikationen
        self.window.bind('<Escape>', exit_app)
        self.window.bind('q', exit_app)

        self.update()

        self.window.mainloop()

    def update(self):
        #  Använder globala variabler
        global status, img
        global object_name_temp
        global object_name
        global object_probability
        global Arduino
        global decoded
        #  Initierar arduino tråd och startar
        thread_arduino = threading.Thread(target=read_arduino)
        thread_arduino.start()
        #  Delay för nästa iteration
        self.delay = 15
        #  Tar en bild med kameran
        ret, frame = self.vid.get_frame()

        #  Om bilden gick att ta
        if ret:
            #  Om något objekt upptäckts och objektet har större än 90 procents säkerhet eller status == True
            if object_name != '' and int(object_probability) > 90 or status:
                #  Om status == False, dvs första gången ett objekt upptäcks med 90% säkerhet
                if not status:
                    #  Spara detta objekt för att inte kunna byta till ett annat
                    object_name_temp = object_name
                    status = True
                #  Om sensorer reagerar i soptunna med Kartong
                if decoded == 'K':
                    #  Om kartong
                    if object_name_temp == 'Kartong':
                        #  Ladda bild från specifik mapp
                        img = random_p_img(self, os.getcwd() + "\\Kartong")
                        status = False
                    #  Annars om felsorterat objekt
                    else:
                        #  Ladda bild från specifik mapp
                        img = random_p_img(self, os.getcwd() + "\\Felsortering")
                        status = False
                #  Om sensorer reagerar i soptunna med Metall
                elif decoded == 'M':
                    #  Om Metall
                    if object_name_temp == 'Metall':
                        #  Ladda bild från specifik mapp
                        img = random_p_img(self, os.getcwd() + "\\Metall")
                        status = False
                    #  Annars om felsorterat objekt
                    else:
                        #  Ladda bild från specifik mapp
                        img = random_p_img(self, os.getcwd() + "\\Felsortering")
                        status = False
                #  Om sensorer reagerar i soptunna med Plast
                elif decoded == 'P':
                    #  Om Plast
                    if object_name_temp == 'Plast':
                        #  Ladda bild från specifik mapp
                        img = random_p_img(self, os.getcwd() + "\\Plast")
                        status = False
                    #  Annars om felsorterat objekt
                    else:
                        #  Ladda bild från specifik mapp
                        img = random_p_img(self, os.getcwd() + "\\Felsortering")
                        status = False
                #  Om sensorerna inte reagerat
                else:
                    #  Om Kartong
                    if object_name_temp == 'Kartong':
                        path = os.getcwd() + "\\Kartongslut"
                    #  Om Metall
                    elif object_name_temp == 'Metall':
                        path = os.getcwd() + "\\Metallslut"
                    #  Om Plast
                    elif object_name_temp == 'Plast':
                        path = os.getcwd() + "\\Plastslut"
                    #  Hittar alla bilder som kan väljas
                    pics = os.listdir(path)
                    #  Välj en av dessa bilder
                    p_picked = random.choice(pics)
                    #  Ladda in den valda bilden till variabeln img
                    img = Image.open(path + "\\" + str(p_picked))
            #  Om inget objekt upptäckts
            else:
                #  Laddar in bilden från kameran utan upptäckta objekt
                img = Image.fromarray(frame)
            #  Ändra storleken på bilden till samma storlek som skärmen/mainwindow
            img = img.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.ANTIALIAS)
            #  Specificera vilken bild som ska öppnas i canvas
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        #  Kör funktionen update igen efter den angivna delayen
        self.window.after(self.delay, self.update)

#  Kamera klass som innehåller relaterade funktioner för avläsning av kamera
class Camera:
    def __init__(self, video_source=0):
        #  Öppna kameran
        self.vid = cv2.VideoCapture(video_source)
        #  Om kameran inte kunde öppnas
        if not self.vid.isOpened():
            raise ValueError("Unable to open webcam", video_source)

        # Ta storleken av kamera input, bredd och längd
        self.width = window.winfo_screenwidth()
        self.height = window.winfo_screenheight()
    #  Tar en bild och letar efter objekt att upptäcka
    def get_frame(self, ret=None):
        #  Om kameran är öppen
        if self.vid.isOpened():
            global object_name
            global object_probability
            #  Ta bild/ läs av kameran
            ret, frame = self.vid.read()
            #  Kastar om bilden så att den blir som frontkamera i mobil
            frame = cv2.flip(frame, 1)
            #  Om bilden kunde tas correkt
            if ret:
                #  Leta i bilden efter objekt som känns igen med hjälp av Modul
                detected_image, detections = detector.detectObjectsFromImage(
                    input_image=frame,
                    input_type="array",
                    output_type="array",
                    display_percentage_probability=True,
                    minimum_percentage_probability=50)

                #  För varje objekt som hittas
                for detection in detections:
                    #  Läs av hörnens position av objektet
                    (x1, y1, x2, y2) = detection["box_points"]
                    #  Läs av objektets namn
                    object_name = detection["name"]
                    #  Läs av den troliga beräkningssäkerheten hos AIn
                    object_probability = detection["percentage_probability"]
                    #  Ändrar färg på ram runt objekt och text ovanför, Metall = röd, Plast = gul, Kartong = grön
                    if object_name == 'Kartong':
                        color = (0, 179, 0)
                    if object_name == 'Metall':
                        color = (0, 0, 255)
                    if object_name == 'Plast':
                        color = (0, 230, 230)
                    #  Rita ut en ram/ruta runt objektet med specifika färgen
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)
                    #  Specificerar stil på texten
                    font = cv2.FONT_HERSHEY_DUPLEX
                    #  Skalan på texten
                    fontscale = 1
                    #  Vart ska texten placeras
                    org = (x1 + 6, y1 - 6)
                    thickness = 1

                    #  Placerar texten på bilden enligt ovan inställningar
                    cv2.putText(
                            frame,
                            object_name + ": " + str(int(object_probability)) + "%",
                            org,
                            font,
                            fontscale,
                            color,
                            thickness)
                #  Returnerar bilden/framen med upptäckta objekten
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #  Om kameran inte kunde ta en bild correkt
            else:
                return ret, None
        #  Om kameran inte är öppen
        else:
            return ret, None

    #  Stäng kameran när objektet är förstört
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Ladda färdigtränad modul
detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("manafv6.h5")
detector.setJsonPath("detection_config.json")
detector.loadModel()

#  Skapa reference till mainwindow
window = Tk()
#  Initiera och startar tråd för GUI
thread_gui = Gui(window, "Techrecycle")
thread_gui.start()
