import speech_recognition as sr
import extractWord as EW

Recognizer = sr.Recognizer()  # 인스턴스 생성
mic = sr.Microphone()

while True:
    inputText = input("음성 인식을 위해 'start' 를 입력하세요 : ");

    if inputText == 'start':
        # with mic as source:  # 안녕~이라고 말하면
        #     audio = Recognizer.listen(source)
        # try:
        #     data = Recognizer.recognize_google(audio, language="ko")
        # except:
        #     print("이해하지 못했음")

        # result = EW.eWord("빨간 모자 쓴 사람 찾아줘")
        result = EW.eWord("돌아")
        print(result)
        result = EW.eWord("배고파?")
        print(result) #단어 추출 결과

    elif inputText == 'end':
        exit()
    else:
        continue
