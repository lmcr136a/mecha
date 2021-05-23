import numpy as np
import serial
import time
from plots import update_fig


# 직사각형, 채워진 직사각형, 직육면체
def rect(hl, startcoor, endcoor):
    update_fig(hl, startcoor)
    update_fig(hl, [startcoor[0], endcoor[1],startcoor[2]])
    update_fig(hl, [endcoor[0], endcoor[1],startcoor[2]])
    update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
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
