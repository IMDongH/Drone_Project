import speech_recognition as sr
import extractWord as EW
import classifyWord as CW
from utils import *

Recognizer = sr.Recognizer()  # 인스턴스 생성
mic = sr.Microphone()

findSen = "초록색 모자 쓴 사람 찾아줘"
turnSen = "돌아"
batterySen = "배고파?"

myDrone = initTello()

# findResult = EW.eWord(findSen)
# turnResult = EW.eWord(turnSen)
# batteryResult = EW.eWord(batterySen)

while True:
    inputText = input("음성 인식을 위해 'start' 를 입력하세요 : ");

    if inputText == 'start':
        with mic as source:  # 안녕~이라고 말하면
            audio = Recognizer.listen(source)
        try:
            data = Recognizer.recognize_google(audio, language="ko")
            CW.classification(data, myDrone)
        except Exception as e:
            print(e)
            continue

    elif inputText == 'end':
        exit()
    else:
        continue
