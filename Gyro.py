import numpy as np
import math
import time
from sympy import Symbol,solve
import serial
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from plots import get_3dfig_seed, update_fig

PORT = "COM3"


if __name__ == "__main__":
    arduino = serial.Serial(PORT, 9600)
    map = plt.figure()
    map_ax = Axes3D(map)
    map_ax.autoscale(enable=True, axis='both', tight=True)
    map_ax.set_xlim3d([-1000, 1000])
    map_ax.set_ylim3d([-1000, 1000])
    map_ax.set_zlim3d([-1000, 1000])


    plt.show(block=False)


    for i in range(100000000):
        print(i)
        ardu_line = arduino.readline()
        ardu_line = ardu_line.decode()[:-2]
        try:
            cx,cy,cz=asdf.split(",")
        except:
            print("asdf: ", asdf)
            continue
        cx1 = float(cx)
        cy1 = float(cy)
        cz1 = float(cz)

        matrix = [cx1,cy1,cz1]
        result = magnet(matrix)

        newdata = (result[0][0]*100, result[1][0]*100, result[2][0]*100)
        if i == 0:
            hl = get_3dfig_seed(newdata)

        
        print("newdata: ", newdata)
        update_fig(hl, newdata)
        plt.pause(1)

        time.sleep(1.0e-1)
    