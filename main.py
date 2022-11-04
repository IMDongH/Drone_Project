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

myDrone = Tello()
myDrone.connect()

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
                    myDrone.rotate_counter_clockwise(40)
                if data[1] > 210 and data[1] < 420 and data[2] < 210:
                    print("2")
                if data[1] > 420 and data[1] < 630 and data[2] < 210:
                    print("3")
                    myDrone.rotate_clockwise(40)

                if data[1] < 210 and data[2] > 210 and data[2] < 420:
                    print("4")
                    myDrone.rotate_counter_clockwise(40)
                if data[1] > 210 and data[1] < 420 and data[2] > 210 and data[2] < 420:
                    print("5")
                if data[1] > 420 and data[1] < 630 and data[2] > 210 and data[2] < 420:
                    print("6")
                    myDrone.rotate_clockwise(40)

                if data[1] < 210 and data[2] > 420 and data[2] < 630:
                    print("7")
                    myDrone.rotate_counter_clockwise(40)
                if data[1] > 210 and data[1] < 420 and data[2] > 420 and data[2] < 630:
                    print("8")
                if data[1] > 420 and data[1] < 630 and data[2] > 420 and data[2] < 630:
                    print("9")
                    myDrone.rotate_clockwise(40)


def main_action():

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = torch.load("./model_data.pt", map_location=device)

    while True:
        img = myDrone.get_frame_read().frame
        img = cv.resize(img, (width, height))
        results = model(img)
        results2 = results.pandas().xyxy[0][['name', 'xmin', 'ymin', 'xmax', 'ymax']]

        checkLocation(results2.values)

        # for num, i in enumerate(results2.values):
        #     if i[0] == 'bottle':
        #         cv.putText(img, i[0], ((int(i[1]), int(i[2]))), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        #         cv.rectangle(img, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)

        cv.imshow('temp', img)
        cv.waitKey(1)

        if keyboard.is_pressed('f'):
            myDrone.land()
            exit()


###########################################
model = Model('/Users/oldst/PycharmProjects/Drone_Project/en')
recognizer = KaldiRecognizer(model,16000)
#
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1,rate=16000,input=True, frames_per_buffer=8192)
stream.start_stream()

myDrone.streamoff()

print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
myDrone.streamon()

myDrone.takeoff()

while True:
    tempVar = 'hungry'
    # while True:
    #     print("please speak to dongchul : ")
    #     data = stream.read(4096, exception_on_overflow = False)
    #     # if len(data) == 0:
    #     #     break
    #     if recognizer.AcceptWaveform(data):
    #         # print(recognizer.Result())
    #         jsonObject = json.loads(recognizer.Result())
    #         # print(jsonObject.get('text').split())
    #         tempList = EW.eWord(jsonObject.get('text').split())
    #         print(tempList)
    #         if tempList.get("action") != None:
    #             tempVar = tempList["action"]
    #         break


    tempVar = 'turn'
    if tempVar == 'hungry':
        if  myDrone.get_battery() > 50:
            myDrone.move_left(20)
            time.sleep(0.3)
            myDrone.move_right(20)
        elif myDrone.get_battery() < 50:
            myDrone.move_up(20)
            time.sleep(0.3)
            myDrone.move_down(20)
        print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
    elif tempVar == 'flip':
        myDrone.flip('r')
        time.sleep(1)
        myDrone.flip('l')
    else:
        main_action()
