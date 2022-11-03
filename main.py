# import speech_recognition as sr
import extractWord as EW

import pyaudio

import torch
import classifyWord as CW
from utils import *

# Recognizer = sr.Recognizer()  # 인스턴스 생성
# mic = sr.Microphone()


# model = Model('/Users/dong/Desktop/GITHUB/droneProjectTest/en')
# recognizer = KaldiRecognizer(model,16000)
#
# print("말해해해해")
# cap = pyaudio.PyAudio()
# stream = cap.open(format=pyaudio.paInt16, channels=1,rate=16000,input=True, frames_per_buffer=8192)
# stream.start_stream()

# while True:
#     data = stream.read(4096)
#     # if len(data) == 0:
#     #     break
#
#     if recognizer.AcceptWaveform(data):
#         print(recognizer.Result())



findSen = "초록색 모자 쓴 사람 찾아줘"
turnSen = "돌아"
batterySen = "배고파?"

model = torch.hub.load('ultralytics/yolov5', 'yolov5m')  # or yolov5n - yolov5x6, custom

myDrone = initTello()


findResult = EW.eWord(findSen)
turnResult = EW.eWord(turnSen)
batteryResult = EW.eWord(batterySen)

while True:
    inputText = input("음성 인식을 위해 'start' 를 입력하세요 : ");

    if inputText == 'start':
        # with mic as source:  # 안녕~이라고 말하면
        #     audio = Recognizer.listen(source)
        # try:
        #     data = Recognizer.recognize_sphinx(audio)
        #     print(data)
        #     # CW.classification(data, myDrone)


            # Images
            img = 'http://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list
            #
            # # Inference
            results = model(img)

            results.print()

        # except Exception as e:
        #     print(e)
        #     continue



    # # results.pandas().xyxy[0]
    elif inputText == 'end':
        exit()
    else:
        continue
