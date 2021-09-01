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
    if bin == '1':
        return True
    elif bin == '0':
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
        

def clicked(hls, clicked_or_released, map_ax, newdata, color):
    if clicked_or_released == "clicked":
        print("get new hl")
        hls.append(get_3dfig_seed(map_ax, newdata, color))
    return hls


def get_mode_function(mode_name):
    return {
        "default": update_fig,
        "line": line,
        "rect": rect,
        "colored_rect": colored_rect,
        "cube": cube,
        "circle": circle,
        "colored_circle": colored_circle,
        # "sphere": sphere,
        "color": color,
    }[mode_name]


if __name__ == "__main__":
    arduino = serial.Serial(PORT, FREQ)

    map = plt.figure()
    map_ax = get_axis(map)
    # show_dicom(map_ax)
    #    mng = plt.get_current_fig_manager()
    #    mng.full_screen_toggle()
    plt.show(block=False)
    prestate = 0
    right_prestate = 0
    start_coor = [0, 0, 0]
    end_coor = [0, 0, 0]
    cursor = map_ax.scatter3D(0, 0, 0, c=0, cmap='Accent')

    color = 'w'
    color_index = 0
    hls=[]

    for i in range(ITER):
        ardu = get_ardu_line(arduino)
        try:
            left_pressed, right_pressed, mode, cx, cy, cz = ardu.split(",")
        except:
            print("ardu: ", ardu)
            continue
        left_pressed = bin_to_bool(left_pressed)
        right_pressed = bin_to_bool(right_pressed)
        newdata = (float(cx), float(cy), float(cz))

        # Mode: default, rect, colored_rect, circle, colored_circle, cube, color
        for txt in map_ax.texts:
            txt.set_visible(False)
        map_ax.text(1,1,ZLIM*1.3, f"DRAWING MODE: {mode.upper()}", color="white", bbox={'edgecolor':"lavender", 'facecolor': 'lightsteelblue', 'boxstyle':'round,pad=1'})

        clicked_or_released = whether_clicked(left_pressed, prestate)
        right_clicked_or_released = whether_clicked(right_pressed, right_prestate)
        mode_function = get_mode_function(mode)

        print("ardu: ", ardu, clicked_or_released, COLORS[color_index])

        if right_pressed and right_clicked_or_released == "clicked":
            try: 
                hls[len(hls)-1].remove()
                del hls[len(hls)-1]
            except:
                print("못지워! 지우지마! 안지워!")
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
        #         # mode_function(hl, start_coor, end_coor)

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


