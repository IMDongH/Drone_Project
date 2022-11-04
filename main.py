# import speech_recognition as sr
# import extractWord as EW
import time

import pyaudio
from vosk import Model, KaldiRecognizer
# from torch import nn
import torch
import classifyWord as CW
from djitellopy import Tello
import sys
import cv2 as cv
sys.path.insert(0, './yolov5')

width = 640
height = 480

frameWidth = width
frameHeight = height
cap2 = cv.VideoCapture(1)
cap2.set(3, frameWidth)
cap2.set(4, frameHeight)
cap2.set(10,200)

model = Model('/Users/oldst/PycharmProjects/Drone_Project/en')
recognizer = KaldiRecognizer(model,16000)
#
print("말해해해해")
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1,rate=16000,input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    # if len(data) == 0:
    #     break

    if recognizer.AcceptWaveform(data):
        print(recognizer.Result())
        break



findSen = "초록색 모자 쓴 사람 찾아줘"
turnSen = "돌아"
batterySen = "배고파?"

# model = torch.hub.load('ultralytics/yolov5', 'yolov5m')  # or yolov5n - yolov5x6, custom
# torch.save(model.state_dict(), './model_data.pth')
# torch.save(model, './model_data1.pt')

#############################################################3

# class CustomModel(nn.Module):
#     def __init__(self):
#         super(CustomModel, self).__init__()
#         self.layer = nn.Linear(2, 1)
#
#     def forward(self, x):
#         x = self.layer(x)
#         return x

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load("./model_data.pt", map_location=device)

#############################################################3

# print(model)
# model = torch.load('./model_data.pth')

# results.pandas().xyxy[0].xmax - results.pandas().xyxy[0].xmin >= 210 &&
# results.pandas().xyxy[0].ymax - results.pandas().xyxy[0].ymin >= 210
# go_back()
#
# results.pandas().xyxy[0].xmax - results.pandas().xyxy[0].xmin < 210 &&
# results.pandas().xyxy[0].ymax - results.pandas().xyxy[0].ymin < 210
# if 150 보다 작으면~:
#     go_front()
# else:
#     # 위치 판단, 어디에 위치했는지 확인 후 이동
#     area[x][y]
#     x >= 210 & & x <= 420 & & y >= 210 & & y <= 420



print("말해해해해")
myDrone = Tello()
# UDP 통신이어서 드론과 노트북이 1:1로 연결되어있어야한다
myDrone.connect()

myDrone.streamoff()

print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
# myDrone.takeoff()
myDrone.streamon()
# findResult = EW.eWord(findSen)
# turnResult = EW.eWord(turnSen)
# batteryResult = EW.eWord(batterySen)

# time.sleep(1)
#
# frame_read = myDrone.get_frame_read()
#
# time.sleep(1)

while True:
    # inputText = input("음성 인식을 위해 'start' 를 입력하세요 : ")

    # frame = frame_read.frame
    # img = cv.resize(frame, (width, height))
    # cv.imshow('frame', img)

    img = myDrone.get_frame_read().frame
    img = cv.resize(img, (630, 630))
    results = model(img)
    #######################################
    results = results.pandas().xyxy[0][['name', 'xmin', 'ymin', 'xmax', 'ymax']]

    for num, i in enumerate(results.values):
        cv.putText(img, i[0], ((int(i[1]), int(i[2]))), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        cv.rectangle(img, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)


    cv.imshow('temp', img)
    # cv2.imshow(imgRGB)

    #######################################
    # img = cv.resize(results, (360, 240))
    # cv.imshow("Image", img)
    cv.waitKey(2)

    # cv.imwrite(frame)
    # cv.imshow('plz', frame)
    #
    # results = model(frame)
    #
    # results.show()
    # print(results.pandas().xyxy[0])
    # cv.imshow('Tello detection', frame)
    # cv.imwrite('Tello detection', results)
    # if inputText == 'start':
        # with mic as source:  # 안녕~이라고 말하면
        #     audio = Recognizer.listen(source)
        # try:
        #     data = Recognizer.recognize_sphinx(audio)
        #     print(data)
        #     # CW.classification(data, myDrone)


            # Images
            # img = 'Kkarmi3.jpg'  # or file, Path, PIL, OpenCV, numpy, list
            # # Inference

        # except Exception as e:
        #     print(e)
        #     continue


    # elif inputText == 'end':
    #     exit()
    # else:
    #     continue
