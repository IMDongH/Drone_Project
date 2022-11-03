from djitellopy import Tello


def initTello():
    myDrone = Tello()
    # UDP 통신이어서 드론과 노트북이 1:1로 연결되어있어야한다
    myDrone.connect()
    print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")

    # 윗줄 주석 풀어야함
    return myDrone

