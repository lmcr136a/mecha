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


def get_arduino_line(arduino):
    ardu_line = arduino.readline()
    return ardu_line.decode()[:-2]


def get_vel(acc, time_interval):
    return [time_interval*a for a in acc]
    

def get_coordinate(acc, coor, past_vel, time_interval):
    # acc = [ax, ay, az]
    # coor = [x, y, z]
    d_coor = [v*time_interval + 0.5*(time_interval**2)*a for a, v in zip(acc, past_vel) ]
    new_coor = [sum(x) for x in zip(d_coor, coor)]
    return new_coor


if __name__ == "__main__":
    arduino = serial.Serial(PORT, 9600)
    map = plt.figure()
    map_ax = Axes3D(map)
    map_ax.autoscale(enable=True, axis='both', tight=True)
    map_ax.set_xlim3d([-0.01, 0.01])
    map_ax.set_ylim3d([-0.01, 0.01])
    map_ax.set_zlim3d([-0.01, 0.01])
    coor=[0,0,0]
    past_time = time.time()
    past_vel = [0,0,0]
    accs = []

    for i in range(1000):
            
        time_interval = time.time() - past_time
        ardu_line = get_arduino_line(arduino)

        try:
            ardu_line, G_value = ardu_line.split("::")
            ax, ay, az=ardu_line.split(",")
        except:
            print("ardu_line: ", ardu_line)
            continue

        acc = [float(ax), float(ay), float(az)]
        if i <= 5:
            zeroing_acc = acc
            hl = get_3dfig_seed(map_ax)

        acc = [a-z for a,z in zip(acc, zeroing_acc)]  #중력가속도

        coor = get_coordinate(acc, coor, past_vel, time_interval)
        hl = update_fig(hl, coor)
        plt.pause(1)
        plt.show(block=False)


        past_vel = get_vel(acc, time_interval)
        past_time = time.time()
        print("acc: ", acc, "    ", G_value)
        time.sleep(1.0e-3)
    