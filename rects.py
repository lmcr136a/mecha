import numpy as np
import serial
import time
from plots import update_fig
N=200

# 직사각형, 채워진 직사각형, 직육면체, 직선

def rect(hl, startcoor, endcoor):
    rect_x = endcoor[0] - startcoor[0]
    rect_y = endcoor[1] - startcoor[1]
    rect_z = endcoor[2] - startcoor[2]
    min(rect_x, rect_y, rect_z)
    if((rect_x < rect_y ) and (rect_x < rect_z)):
        update_fig(hl, [startcoor[0], endcoor[1], startcoor[2]])
        update_fig(hl, [startcoor[0], endcoor[1], endcoor[2]])
        update_fig(hl, [startcoor[0], startcoor[1], endcoor[2]])
        update_fig(hl, startcoor)
    elif((rect_y < rect_x) and (rect_y < rect_z)):
        update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
        update_fig(hl, [endcoor[0], startcoor[1], endcoor[2]])
        update_fig(hl, [startcoor[0], startcoor[1], endcoor[2]])
        update_fig(hl, startcoor)
    elif((rect_z < rect_y) and (rect_z < rect_x)):
        update_fig(hl, [startcoor[0], endcoor[1], startcoor[2]])
        update_fig(hl, [endcoor[0], endcoor[1], startcoor[2]])
        update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
        update_fig(hl, startcoor)
    else:
        print(f"error! rect_x:{rect_x}, rect_y:{rect_y}, rect_z:{rect_z}")
    return hl


# def rect(hl, startcoor, endcoor):
#     update_fig(hl, startcoor)
#     update_fig(hl, [startcoor[0], endcoor[1], startcoor[2]])
#     update_fig(hl, [endcoor[0], endcoor[1], startcoor[2]])
#     update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
#     update_fig(hl, startcoor)
#     return hl
    
def colored_rect(hl, startcoor, endcoor):
    rect_x = endcoor[0] - startcoor[0]
    rect_y = endcoor[1] - startcoor[1]
    rect_z = endcoor[2] - startcoor[2]
    min(rect_x, rect_y, rect_z)
    if((rect_x < rect_y ) and (rect_x < rect_z)):
        for i in range(N):
            update_fig(hl, [startcoor[0], ((N - i) / N) * startcoor[1] + (i / N) * endcoor[1], startcoor[2]])
            update_fig(hl, [startcoor[0], ((N - i) / N) * startcoor[1] + (i / N) * endcoor[1], endcoor[2]])
            update_fig(hl, [startcoor[0], startcoor[1], endcoor[2]])
            update_fig(hl, startcoor)

    elif((rect_y < rect_x) and (rect_y < rect_z)):
        for i in range(N):
            update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
            update_fig(hl, [endcoor[0], startcoor[1], ((N - i) / N) * startcoor[2] + (i / N) * endcoor[2]])
            update_fig(hl, [startcoor[0], startcoor[1], ((N - i) / N) * startcoor[2] + (i / N) * endcoor[2]])
            update_fig(hl, startcoor)
    elif((rect_z < rect_y) and (rect_z < rect_x)):
        for i in range(N):
            update_fig(hl, [startcoor[0], endcoor[1], startcoor[2]])
            update_fig(hl, [((N - i) / N) * startcoor[0] + (i / N) * endcoor[0], endcoor[1], startcoor[2]])
            update_fig(hl, [((N - i) / N) * startcoor[0] + (i / N) * endcoor[0], startcoor[1], startcoor[2]])
            update_fig(hl, startcoor)
    else:
        print("error!")
    return hl


def cube(hl, startcoor, endcoor):
    print(hl)
    update_fig(hl, startcoor)
    update_fig(hl, [startcoor[0], endcoor[1], startcoor[2]])
    update_fig(hl, [endcoor[0], endcoor[1], startcoor[2]])
    update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
    update_fig(hl, startcoor)
    update_fig(hl, [startcoor[0], startcoor[1], endcoor[2]])
    update_fig(hl, [startcoor[0], endcoor[1], endcoor[2]])
    update_fig(hl, [startcoor[0], endcoor[1], startcoor[2]])
    update_fig(hl, [startcoor[0], endcoor[1], endcoor[2]])
    update_fig(hl, [endcoor[0], endcoor[1], endcoor[2]])
    update_fig(hl, [endcoor[0], endcoor[1], startcoor[2]])
    update_fig(hl, [endcoor[0], endcoor[1], endcoor[2]])
    update_fig(hl, [endcoor[0], startcoor[1], endcoor[2]])
    update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
    update_fig(hl, [endcoor[0], startcoor[1], endcoor[2]])
    update_fig(hl, [startcoor[0], startcoor[1], endcoor[2]])
    return hl


def line(hl, startcoor, endcoor):
    update_fig(hl, startcoor)
    update_fig(hl, endcoor)
    return hl

