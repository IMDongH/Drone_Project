import time


def batteryF(drone):  #배터리 함수 추가

    print("\n * Drone battery percentage : " + str(drone.get_battery()) + "%")
    return "battery"


def turnF(drone):  #도는 함수 추가
    print("turn")
    drone.rotate_clockwise(360)
    # drone.takeoff()
    drone.flip("r")
    time.sleep(2)
    drone.flip("r")
    time.sleep(2)
    return "turn"


def findF(drone):  #따라 다니는 함수 추가
    return "find"


def takePictureF(drone):  #사진 찍는 함수 추가
    return "picture"