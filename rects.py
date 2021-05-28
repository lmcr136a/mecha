import numpy as np
import serial
import time
from plots import update_fig
N=200

# 직사각형, 채워진 직사각형, 직육면체
def rect(hl, startcoor, endcoor):
    update_fig(hl, startcoor)
    update_fig(hl, [startcoor[0], endcoor[1],startcoor[2]])
    update_fig(hl, [endcoor[0], endcoor[1],startcoor[2]])
    update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
    update_fig(hl, startcoor)
    return hl
    
def colored_rect(hl, startcoor, endcoor):
    for i in range(N):
        update_fig(hl, startcoor)
        update_fig(hl, [startcoor[0], endcoor[1], startcoor[2]])
        update_fig(hl, [((N-i)/N)*startcoor[0]+(i/N)*endcoor[0], endcoor[1], startcoor[2]])
        update_fig(hl, [((N-i)/N)*startcoor[0]+(i/N)*endcoor[0], startcoor[1], startcoor[2]])
        update_fig(hl, startcoor)
    return hl


def cube(hl, startcoor, endcoor):
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
