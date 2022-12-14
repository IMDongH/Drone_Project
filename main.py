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
rotateFlagForFind = False
rotateFlagForPhoto = False
findFlag = False
photoFlag = False
# objectList = ['cup', 'person', 'cell phone']
# objectList = ['bottle']
###########################################

def checkLocation(offset_x, offset_y, offset_z, param):
    global findFlag
    global photoFlag
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
            if param == 'photo':
                myDrone.move_forward(40)
            else:
                myDrone.move_forward(60)
        elif offset_z > 30000:
            if param == 'photo':
                myDrone.move_back(30)
            else:
                myDrone.move_back(40)
    else:
        if param == 'find':
            myDrone.rotate_clockwise(360)
            findFlag = True
        elif param == 'photo':
            photoFlag = True



###########################################
model = Model('/Users/oldst/PycharmProjects/Drone_Project/en')
recognizer = KaldiRecognizer(model,16000)

print("please speak to dongchul : ")
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1,rate=16000,input=True, frames_per_buffer=8192)
stream.start_stream()

myDrone = Tello()
myDrone.connect()

myDrone.streamoff()

print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
myDrone.streamon()

myDrone.takeoff()

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load("./model_data_yolov5n.pt", map_location=device)

i = -1
# print("please speak to dongchul : ")
while True:
        print("please speak to dongchul : ")
        time.sleep(3)
        i += 1
        tempVar = ['photo','find', 'land']
        # while True:
        #     print("please speak to dongchul : ")
        #     data = stream.read(4096, exception_on_overflow=False)
        #     if recognizer.AcceptWaveform(data):
        #         # print(recognizer.Result())
        #         jsonObject = json.loads(recognizer.Result())
        #         i += 1
        #         # print(jsonObject.get('text').split())
        #         # tempList = EW.eWord(jsonObject.get('text').split())
        #         # print(tempList)
        #         # if tempList.get("action") != None:
        #         #     tempVar = tempList["action"]
        #         break

        if tempVar[i] == 'hungry':
            if myDrone.get_battery() > 50:
                myDrone.move_left(20)
                time.sleep(0.3)
                myDrone.move_right(20)
            elif myDrone.get_battery() <= 50:
                myDrone.move_up(20)
                time.sleep(0.3)
                myDrone.move_down(20)
            print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
        elif tempVar[i] == 'flip':
            myDrone.flip("r")
            time.sleep(1)
            myDrone.flip("l")
        elif tempVar[i] == 'photo':
            # img = myDrone.get_frame_read().frame
            # img = cv.resize(img, (width, height))
            # cv.imwrite("picture.png", img)
            # cv.waitKey(1)
            while True:
                if photoFlag:
                    cv.imwrite("picture2.png", img)
                    cv.waitKey(1)
                    break

                if not rotateFlagForPhoto:
                    myDrone.rotate_clockwise(30)
                    time.sleep(1)

                img = myDrone.get_frame_read().frame
                img = cv.resize(img, (width, height))
                results = model(img)
                results2 = results.pandas().xyxy[0][['name', 'xmin', 'ymin', 'xmax', 'ymax']]

                center_x = int(width / 2)
                center_y = int(height / 2)

                for num, i in enumerate(results2.values):
                    if i[0] == 'person':
                        rotateFlagForPhoto = True
                        object_center_x = (i[3] + i[1]) / 2
                        object_center_y = (i[4] + i[2]) / 2
                        offset_x = object_center_x - center_x
                        offset_y = object_center_y - center_y - 30
                        offset_z = (i[3] - i[1]) * (i[4] - i[2])
                        checkLocation(offset_x, offset_y, offset_z, 'photo')
                        break
                cv.imshow('temp', img)
                cv.waitKey(1)
        elif tempVar[i] == 'find':
            while True:
                if findFlag:
                    break

                if not rotateFlagForFind:
                    myDrone.rotate_clockwise(30)
                    time.sleep(1)

                img = myDrone.get_frame_read().frame
                img = cv.resize(img, (width, height))
                results = model(img)
                results2 = results.pandas().xyxy[0][['name', 'xmin', 'ymin', 'xmax', 'ymax']]

                center_x = int(width / 2)
                center_y = int(height / 2)

                for num, i in enumerate(results2.values):
                    if i[0] == 'bottle' or i[0] == 'person':
                        cv.putText(img, i[0], ((int(i[1]), int(i[2]))), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                        cv.rectangle(img, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)
                        if i[0] == 'bottle':
                            rotateFlagForFind = True
                            object_center_x = (i[3] + i[1]) / 2
                            object_center_y = (i[4] + i[2]) / 2
                            offset_x = object_center_x - center_x
                            offset_y = object_center_y - center_y - 30
                            offset_z = (i[3] - i[1]) * (i[4] - i[2])
                            checkLocation(offset_x, offset_y, offset_z, 'find')
                            break
                cv.imshow('temp', img)
                cv.waitKey(1)

                if keyboard.is_pressed('f'):
                    myDrone.land()
                    exit()

        elif tempVar[i] == 'land':
            myDrone.land()
            exit()