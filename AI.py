# Ladda HL detection model från imageAI
# Öppna kameran med openCV, analysera frame by frame
# Rita en röd ruta kring det hittade objektet
 
from imageai.Detection.Custom import CustomObjectDetection
import os
import cv2
 
detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("map0-7750.h5") 
detector.setJsonPath("detection_config.json")
detector.loadModel()
 
# init camera
execution_path = os.getcwd()
camera = cv2.VideoCapture(0)
 
while True:
 
    # Grab a single frame of video
    ret, frame = camera.read()
 
    detected_image, detections = detector.detectObjectsFromImage(input_image=frame, input_type="array", output_type="array")
 
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"])
        (x1, y1, x2, y2) = detection["box_points"]
        print("x1: ", x1, " - y1: ", y1, " - x2: ", x2, " - y2: ", y2)
    
        # frame for the detected object
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
 
        # Draw a label with the detected object type below the frame
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, detection["name"], (x1 + 6, y1 - 6), font, 1.0, (255, 255, 255), 1)
 
    # Display the resulting image
    cv2.imshow('Video', frame)
 
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release handle to the webcam
camera.release()
cv2.destroyAllWindows()
