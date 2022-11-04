# import speech_recognition as sr
import extractWord as EW
import json
import time
import keyboard
import pyaudio
from vosk import Model, KaldiRecognizer
# from torch import nn
import torch
import classifyWord as CW
from djitellopy import Tello
import sys
import cv2 as cv
sys.path.insert(0, './yolov5')

width = 630
height = 630

frameWidth = width
frameHeight = height
findFlag = False
# objectList = ['cup', 'person', 'cell phone']
# objectList = ['bottle']
###########################################

def checkLocation(offset_x, offset_y, offset_z):
    """
    Adjusts the position of the tello drone based on the offset values given from the frame

    :param offset_x: Offset between center and face x coordinates
    :param offset_y: Offset between center and face y coordinates
    :param offset_z: Area of the face detection rectangle on the frame
    """

    print(offset_x, offset_y, offset_z)

    if not -90 <= offset_x <= 90 and offset_x is not 0:
        if offset_x < 0:
            myDrone.rotate_counter_clockwise(30)
        elif offset_x > 0:
            myDrone.rotate_clockwise(30)

    if not -70 <= offset_y <= 70 and offset_y is not -30:
        if offset_y < 0:
            myDrone.move_up(20)
        elif offset_y > 0:
            myDrone.move_down(20)

    if not 15000 <= offset_z <= 30000 and offset_z is not 0:
        if offset_z < 15000:
            myDrone.move_forward(60)
        elif offset_z > 30000:
            myDrone.move_back(40)



###########################################
model = Model('/Users/oldst/PycharmProjects/Drone_Project/en')
recognizer = KaldiRecognizer(model,16000)

print("please speak to dongchul : ")
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1,rate=16000,input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    # if len(data) == 0:
    #     break

    if recognizer.AcceptWaveform(data):
        # print(recognizer.Result())
        jsonObject = json.loads(recognizer.Result())
        # print(jsonObject.get('text').split())
        print(EW.eWord(jsonObject.get('text').split()))
        # temp = EW.eWord(jsonObject.get('text').split())
        break

myDrone = Tello()
myDrone.connect()

myDrone.streamoff()

print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
myDrone.streamon()

myDrone.takeoff()

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load("./model_data_yolov5n.pt", map_location=device)

while True:
    if not findFlag:
        myDrone.rotate_clockwise(30)
        time.sleep(1)

    img = myDrone.get_frame_read().frame
    img = cv.resize(img, (width, height))
    results = model(img)
    results2 = results.pandas().xyxy[0][['name', 'xmin', 'ymin', 'xmax', 'ymax']]

    center_x = int(width / 2)
    center_y = int(height / 2)

    for num, i in enumerate(results2.values):
            if i[0] == 'bottle':
                findFlag = True
                cv.putText(img, i[0], ((int(i[1]), int(i[2]))), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                cv.rectangle(img, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)
                object_center_x = (i[3] + i[1]) / 2
                object_center_y = (i[4] + i[2]) / 2
                offset_x = object_center_x - center_x
                offset_y = object_center_y - center_y - 30
                offset_z = (i[3] - i[1]) * (i[4] - i[2])
                checkLocation(offset_x, offset_y, offset_z)
                break
    cv.imshow('temp', img)
    cv.waitKey(1)

    if keyboard.is_pressed('f'):
        myDrone.land()
        exit()

