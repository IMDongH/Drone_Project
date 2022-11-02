import droneFun
from droneFun import *

orderList = ["찾아", "건네", "따라"]


def classification(words, drone):
    flag = False

    for i in range(len(orderList)):
        flag = True
        break

    if "돌아" in words:
        droneFun.turnF(drone)
        return "돌아"  # 도는 함수 불러오기
    elif "배고파?" in words:
        droneFun.batteryF(drone)
        return "배고파"  # 배터리 잔량 함수 불러오기
    elif "사진" in words:
        droneFun.takePictureF(drone)
        return "사진"
    elif flag:
        droneFun.findF(drone)
        return "else"  # 따라 다니는 함수 불러오기
    else:
        return "fail"
