import numpy as np
import matplotlib.pyplot as plt
import serial
import time

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from plots import *
from colors import *
from circles import *
from rects import *

# git add (푸시하고싶은 파일) 또는 git add . (전체파일)
# git commit -m "하고싶은 말"
# git push
# git pull << 받아오기

ITER = 10000
PORT = "COM3"
FREQ = 9600
XLIM = 3000
YLIM = 3000
ZLIM = 1500
TIME_SLEEP = 1.0e-4
PLT_TIME_SLEEP = 1.0e-4


def get_ardu_line(arduino):
        ardu = arduino.readline()
        return ardu.decode()[:-2]


def get_axis(map):
    map_ax = Axes3D(map)
    map_ax.autoscale(enable=True, axis='both', tight=True)
    map_ax.set_xlim3d([0, XLIM])
    map_ax.set_ylim3d([0, YLIM])
    map_ax.set_zlim3d([0, ZLIM])
    return map_ax


def bin_to_bool(bin):
    if bin == 1:
        return True
    elif bin == 0:
        return False
    else:
        print("Error in bin to bool")
        return False


def whether_clicked(left_pressed, past_left_pressed):
    if left_pressed and past_left_pressed: # 계속 눌린 상태
        return "not changed"
    elif not past_left_pressed and left_pressed: # 안눌렸었는데 눌림
        return "clicked"
    elif past_left_pressed and not left_pressed: # 눌렸었는데 안눌림
        return "released"
    elif not past_left_pressed and left_pressed: # 떼진상태
        return "not changed"
    else:
        print("Error in whether_clicked function")
        return "not changed"
        

def get_mode_function(mode_name):
    return {
        "default": update_fig,
        "rect": rect,
        "colored_rect": colored_rect,
        "cube": cube,
        "circle": circle,
        "colored_circle": colored_circle,
        "color": color,
    }[mode_name]

if __name__ == "__main__":
    arduino = serial.Serial(PORT, FREQ)
    map = plt.figure()
    map_ax = get_axis(map)
    plt.show(block=False)
    premode = 0
    start_coor = 0
    end_coor = 0

    for i in range(ITER):
        ardu = get_ardu_line(arduino)
        try:
            mode, left_pressed, right_pressed, cx, cy, cz = ardu.split(",")
        except:
            print("ardu: ", ardu)
            continue
        left_pressed = bin_to_bool(left_pressed)
        right_pressed = bin_to_bool(right_pressed)
        newdata = (float(cx), float(cy), float(cz))

        if i == 0:
            hl = get_3dfig_seed(map_ax, newdata)

        print("mod: ", mode)
        print("newdata: ", newdata)

        # Mode: default, rect, colored_rect, circle, colored_circle, cube, color
        clicked_or_released = whether_clicked(mode, prestate)
        mode_function = get_mode_function(mode, left_pressed, right_pressed)

        
        if mode in ["rect", "colored_rect", "circle", "colored_circle", "cube"]:
            if clicked_or_released == "clicked":
                    start_coor = newdata
            elif clicked_or_released == "released":
                end_coor = newdata
                mode_function(hl, start_coor, end_coor)
        
        elif left_pressed and mode == "color":
            pass
        elif left_pressed and mode == "default":
            mode_function(hl, newdata)
        elif right_pressed:
            cancel_fig(hl)
        else:
            print("exception")


        prestate = left_pressed
        plt.pause(PLT_TIME_SLEEP)
        time.sleep(TIME_SLEEP)


