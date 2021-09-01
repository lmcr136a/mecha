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
from main import *
from dicom import *
# git add (푸시하고싶은 파일) 또는 git add . (전체파일)
# git commit -m "하고싶은 말"
# git push
# git pull << 받아오기

ITER = 10000
PORT = "COM6"
FREQ = 115200
XLIM = 500
YLIM = 500
ZLIM = 500
TIME_SLEEP = 1.0e-5
PLT_TIME_SLEEP = 1.5e-2
COLORS = ['r', 'b', 'y', 'k', 'g']
MODE = "default"


def make_dummy_input(mode="default", iter=100):  # 3 1 2 1 3
    iblock = round(iter/10)
    dummy=[]
    def f(i):
        li = list(np.linspace(1, 60, 2*iblock))
        li += list(np.linspace(60, 1, 2*iblock))
        li += list(np.linspace(1, 60, 2*iblock))
        li += list(np.linspace(60, 10, 2*iblock))
        li += list(np.linspace(10, 50, 2*iblock))
        li += list(np.linspace(51, 55, 2*iblock))
        li += list(np.linspace(55, 100, 2*iblock))
        print(len(li), li)
        return li[i]
        
    for i in range(iter):
        dummy.append(["0", "0", mode, f(i), f(i), i])

    for i in range(40):
        dummy[i][0] = "1"
    for i in range(42, 80):
        dummy[i][0] = "1"
    for i in range(82, 99):
        dummy[i][0] = "1"
    return dummy


if __name__ == "__main__":
    dummy = make_dummy_input(MODE)

    mapp = plt.figure()
    map_ax = get_axis(mapp)
    show_dicom(map_ax)
    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    plt.show(block=False)
    prestate = 0
    right_prestate = 0
    start_coor = [0, 0, 0]
    end_coor = [0, 0, 0]
    cursor = map_ax.scatter3D(0, 0, 0, c = 0, cmap='Accent')

    color = 'w'
    color_index = 0
    hls=[]

    for dumm in dummy:
        try:
            left_pressed, right_pressed, mode, cx, cy, cz = dumm
        except:
            print("ardu: ", ardu)
            continue
        left_pressed = bin_to_bool(left_pressed)
        right_pressed = bin_to_bool(right_pressed)
        newdata = (float(cx), float(cy), float(cz))

        # Mode: default, rect, colored_rect, circle, colored_circle, cube, sphere, color
        for txt in map_ax.texts:
            txt.set_visible(False)
        map_ax.text(1,1,ZLIM*1.3, f"DRAWING MODE: {mode.upper()}", color="white", bbox={'edgecolor':"lavender", 'facecolor': 'lightsteelblue', 'boxstyle':'round,pad=1'})

        clicked_or_released = whether_clicked(left_pressed, prestate)
        right_clicked_or_released = whether_clicked(right_pressed, right_prestate)
        mode_function = get_mode_function(mode)

        print("dumm: ", dumm, clicked_or_released, COLORS[color_index], "  ::  ",len(hls))

        if right_pressed and right_clicked_or_released == "clicked":
            try: 
                hls[len(hls)-1].remove()
                del hls[len(hls)-1]
            except:
                print("Can't removing")
            print("removed, ", len(hls))

        elif mode in ["rect", "line", "colored_rect", "cube"]:
            if clicked_or_released == "clicked":
                hls = clicked(hls, clicked_or_released, map_ax, newdata, color)
                start_coor = newdata
            if clicked_or_released == "released":
                end_coor = newdata
                mode_function(hls[len(hls)-1], start_coor, end_coor)

        elif mode in ["circle", "colored_circle"]:
            if clicked_or_released == "clicked":
                start_coor = newdata
            if clicked_or_released == "released":
                end_coor = newdata
                hls.append(get_3dfig_seed(map_ax, newdata, color))
                mode_function(hls[len(hls)-1], start_coor, end_coor)


        # elif mode in ["sphere"]:
        #     hls = clicked(hls, clicked_or_released, map_ax, newdata, color)
        #     if clicked_or_released == "released":
        #         end_coor = newdata
        #         mode_function(hls[len(hls)-1], start_coor, end_coor, map_ax)
                #mode_function(hl, start_coor, end_coor)
        
        elif left_pressed and mode == "color":
            color_index += 1
            if color_index > len(COLORS) - 1 :
                color_index = 0
            color = COLORS[color_index]

        elif mode == "default":
            if left_pressed:
                hls = clicked(hls, clicked_or_released, map_ax, newdata, color)
                mode_function(hls[len(hls)-1], newdata)
            if clicked_or_released == "released":
                hls = interpo_update_fig(hls)
        else:
            pass

        cursor.remove()
        cursor = map_ax.scatter3D(newdata[0], newdata[1], newdata[2], c=newdata[2], cmap='Accent')

        prestate = left_pressed
        right_prestate = right_pressed
        plt.pause(PLT_TIME_SLEEP)
        time.sleep(TIME_SLEEP)
    time.sleep(2)

