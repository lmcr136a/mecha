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
XLIM = 100
YLIM = 100
ZLIM = 100
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


def make_dummy_input(mode="default", i=100):  # 3 1 2 1 3
    first_pressed = round(i * 3/10)
    interval1 = round(i * 4/10)
    second_pressed = round(i * 6/10)
    interval2 = round(i * 7/10)
    third_pressed = i
    dummy = []
    for j in range(int(i)):
        if j <= first_pressed:
            dummy.append([mode, True, False, j, j, j])
        if first_pressed < j <= interval1:
            dummy.append([mode, False, False, j, j, j])
        if interval1 < j <= second_pressed:
            dummy.append([mode, True, False, j, j, j])
        if second_pressed < j <= interval2:
            dummy.append([mode, False, False, j, j, j])
        if interval2 < j <= third_pressed:
            dummy.append([mode, True, False, j, j, j])
    return dummy


if __name__ == "__main__":
    dummy = make_dummy_input("default")

    mapp = plt.figure()
    map_ax = get_axis(mapp)
    plt.show(block=False)
    prestate = 0
    start_coor = 0
    end_coor = 0

    for dumm in dummy:
        try:
            mode, left_pressed, right_pressed, cx, cy, cz = dumm
        except:
            print("dumm: ", dumm)
            continue
        left_pressed = bin_to_bool(left_pressed)
        right_pressed = bin_to_bool(right_pressed)
        newdata = (float(cx), float(cy), float(cz))

        if dumm[-3:] == [0,0,0]:
            hl = get_3dfig_seed(map_ax, newdata)

        print("mod: ", mode)
        print("newdata: ", newdata)

        # Mode: default, rect, colored_rect, circle, colored_circle, cube, color
        clicked_or_released = whether_clicked(mode, prestate)
        mode_function = get_mode_function(mode)

        
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


