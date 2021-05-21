import numpy as np
import matplotlib.pyplot as plt
import serial

# git add (푸시하고싶은 파일) 또는 git add . (전체파일)
# git commit -m "하고싶은 말"
# git push

arduino = serial.Serial('COM3', 9600)


def get_coordinate():
    p = arduino.readline()
    print(p)
    dummy = [1,2,3]
    x = dummy
    y = dummy
    z = dummy
    return x, y, z


def show(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    plt.show()


if __name__ == "__main__":
    while(True):
        x, y, z = get_coordinate()
        #show(x, y, z)

