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
# objectList = ['cup', 'person', 'cell phone']
objectList = ['bottle']
###########################################

def checkLocation(result):
    for i, data in enumerate(result):
        if data[0] in objectList:
            if (data[3] - data[1]) > width/3 or (data[4] - data[2]) > height/3:
                # print('go_back()', (data[3] - data[1]) * (data[4] - data[2]))
                # print('go_back()', (data[3] - data[1]) * (data[4] - data[2]))
                myDrone.move_back(20)
            elif (data[3] - data[1]) < (width/3)*1/3 or (data[4] - data[2]) < (height/3)*1/3:
                # print('go_front()', (data[3] - data[1]) * (data[4] - data[2]))
                myDrone.move_forward(20)
            else:
                if data[1] < 210 and data[2] < 210:
                    print("1")
                    myDrone.rotate_clockwise()
                if data[1] > 210 and data[1] < 420 and data[2] < 210:
                    print("2")
                if data[1] > 420 and data[1] < 630 and data[2] < 210:
                    print("3")

                if data[1] < 210 and data[2] > 210 and data[2] < 420:
                    print("4")
                if data[1] > 210 and data[1] < 420 and data[2] > 210 and data[2] < 420:
                    print("5")
                if data[1] > 420 and data[1] < 630 and data[2] > 210 and data[2] < 420:
                    print("6")

                if data[1] < 210 and data[2] > 420 and data[2] < 630:
                    print("7")
                if data[1] > 210 and data[1] < 420 and data[2] > 420 and data[2] < 630:
                    print("8")
                if data[1] > 420 and data[1] < 630 and data[2] > 420 and data[2] < 630:
                    print("9")

###########################################
model = Model('/Users/oldst/PycharmProjects/Drone_Project/en')
recognizer = KaldiRecognizer(model,16000)
#
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
        break

myDrone = Tello()
myDrone.connect()

myDrone.streamoff()

print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
myDrone.streamon()

myDrone.takeoff()

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load("./model_data.pt", map_location=device)

while True:
    img = myDrone.get_frame_read().frame
    img = cv.resize(img, (width, height))
    results = model(img)
    results2 = results.pandas().xyxy[0][['name', 'xmin', 'ymin', 'xmax', 'ymax']]

    checkLocation(results2.values)

    for num, i in enumerate(results2.values):
        if i[0] == 'bottle':
            cv.putText(img, i[0], ((int(i[1]), int(i[2]))), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            cv.rectangle(img, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)


    cv.imshow('temp', img)
    cv.waitKey(1)

    if keyboard.is_pressed('f'):
        myDrone.land()
        exit()

