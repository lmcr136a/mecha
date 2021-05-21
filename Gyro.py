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


def get_coordinate(acc, coor, past_time=time.time()):
    # acc = [ax, ay, az]
    # coor = [x, y, z]
    time_unit = round(time.time() - past_time,6)
    time_unit = float(str(time_unit)[-7:])
    print(time_unit)
    d_coor = [0.5*(time_unit**2)*a for a in acc ]
    new_coor = [sum(x) for x in zip(d_coor, coor)]
    return new_coor


if __name__ == "__main__":
    arduino = serial.Serial(PORT, 9600)
    map = plt.figure()
    map_ax = Axes3D(map)
    map_ax.autoscale(enable=True, axis='both', tight=True)
    map_ax.set_xlim3d([-1000, 1000])
    map_ax.set_ylim3d([-1000, 1000])
    map_ax.set_zlim3d([-1000, 1000])
    coor=[0,0,0]

    for i in range(100000000):
        ardu_line = arduino.readline()
        ardu_line = ardu_line.decode()[:-2]
        try:
            ax, ay, az=ardu_line.split(",")
        except:
            print("ardu_line: ", ardu_line)
            continue
        acc = [float(ax), float(ay), float(az)]

        if i == 0:
            hl = get_3dfig_seed(map_ax)

        coor = get_coordinate(acc, coor)
        print("acc: ", acc)
        update_fig(hl, coor)
        plt.pause(1)
        
        plt.show(block=False)

        time.sleep(1.0e-1)
    