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
PORT = "COM6"
FREQ = 115200
XLIM = 100
YLIM = 100
ZLIM = 100
MODE = "cube"
TIME_SLEEP = 1.0e-4
PLT_TIME_SLEEP = 1.0e-4
COLORS = ['r', 'b', 'y', 'k', 'g']


def get_ardu_line(arduino):
        ardu = arduino.readline()
        return ardu.decode()[:-2]


def get_axis(map):
    map_ax = Axes3D(map, facecolor="k")
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
    elif not past_left_pressed and not left_pressed: # 떼진상태
        return "not changed"
    else:
        print("Error in whether_clicked function")
        return "not changed"


def clicked(hl, clicked_or_released, map_ax, newdata, color):
    if clicked_or_released == "clicked":
        print("get new hl")
        hl = get_3dfig_seed(map_ax, newdata, color)
    return hl
        

def get_mode_function(mode_name):
    return {
        "default": update_fig,
        "line": line,
        "rect": rect,
        "colored_rect": colored_rect,
        "cube": cube,
        "circle": circle,
        "colored_circle": colored_circle,
        "sphere": sphere,
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
        if j <= first_pressed - 7:      ### 0~30 누르고 있음
            dummy.append([mode, True, False, j, j, j])
        if j == first_pressed - 6:      ### 값이 튐
            dummy.append([mode, True, False, 500, j, j])
        if first_pressed - 6 < j <= first_pressed:      ### 0~30 누르고 있음
            dummy.append([mode, True, False, j, j, j])

        if first_pressed < j <= interval1:   # 10분동안 쉼
            dummy.append([mode, False, False, j, j, j])
        if interval1 < j < second_pressed:   ### 40~60 누르고 있음
            dummy.append([mode, True, False, j, j, j])
        if second_pressed <= j < second_pressed + 5:   # 40 ~ 45 그냥 있음
            dummy.append([mode, False, False, j, j, j])

        if j == second_pressed+5:
            dummy.append(["color", True, False, j, j, j])   #### 45에서 color 모드에서 클릭
        if j == second_pressed+6:
            dummy.append(["color", False, False, j, j, j])
        if j == second_pressed+7:
            dummy.append([mode, False, True, j, j, j])    #### 47 : remove 버튼 누름

        if second_pressed+7 < j <= interval2:
            dummy.append([mode, False, False, j, j, j])
        if interval2 < j <= third_pressed:
            dummy.append([mode, True, False, j, j, j])
    dummy.append([mode, False, False, i, i, i])
    dummy.append([mode, False, False, i, i, i])
    dummy.append([mode, False, False, i, i, i])
    return dummy


if __name__ == "__main__":
    dummy = make_dummy_input(MODE)

    mapp = plt.figure()
    map_ax = get_axis(mapp)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show(block=False)
    prestate = 0
    start_coor = [0, 0, 0]
    end_coor = [0, 0, 0]
    cursor = map_ax.scatter3D(0, 0, 0, c = 0, cmap='Accent')

    color = 'w'
    color_index = 0
    for dumm in dummy:
        try:
            mode, left_pressed, right_pressed, cx, cy, cz = dumm
        except:
            print("!! dumm: ", dumm)
            continue
        left_pressed = bin_to_bool(left_pressed)
        right_pressed = bin_to_bool(right_pressed)
        newdata = (float(cx), float(cy), float(cz))

        if dumm[-3:] == [0,0,0]:
            print("get new hl")
            hl = get_3dfig_seed(map_ax, newdata)

        # Mode: default, rect, colored_rect, circle, colored_circle, cube, sphere, color
        clicked_or_released = whether_clicked(left_pressed, prestate)
        mode_function = get_mode_function(mode)

        print("dumm: ", dumm, clicked_or_released, COLORS[color_index])

        if right_pressed:
            print("removed")
            hl.remove()

        elif mode in ["rect", "line", "colored_rect", "cube"]:
            if clicked_or_released == "clicked":
                hl = clicked(hl, clicked_or_released, map_ax, newdata, color)
                start_coor = newdata
            if clicked_or_released == "released":
                end_coor = newdata
                mode_function(hl, start_coor, end_coor)

        elif mode in ["circle", "colored_circle"]:
            if clicked_or_released == "clicked":
                start_coor = newdata
            if clicked_or_released == "released":
                end_coor = newdata
                hl = get_3dfig_seed(map_ax, newdata, color)
                mode_function(hl, start_coor, end_coor)

        elif mode in ["sphere"]:
            hl = clicked(hl, clicked_or_released, map_ax, newdata, color)
            if clicked_or_released == "released":
                end_coor = newdata
                mode_function(hl, start_coor, end_coor, map_ax)
                #mode_function(hl, start_coor, end_coor)
        
        elif left_pressed and mode == "color":
            color = COLORS[color_index]
            color_index += 1
            if color_index > len(COLORS):
                color_index = 0

        elif left_pressed and mode == "default":
            hl = clicked(hl, clicked_or_released, map_ax, newdata, color)
            mode_function(hl, newdata)
        else:
            pass

        cursor.remove()
        cursor = map_ax.scatter3D(newdata[0], newdata[1], newdata[2], c=newdata[2], cmap='Accent')

        prestate = left_pressed
        plt.pause(PLT_TIME_SLEEP)
        time.sleep(TIME_SLEEP)
    time.sleep(2)

