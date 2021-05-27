import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import serial
import time
import math
from plots import update_fig
N=75
M=400

# 원, 채워진 원, 구

def circle(hl, startcoor, endcoor):
    r = math.sqrt(pow(startcoor[0]-endcoor[0], 2) + pow(startcoor[1]-endcoor[1], 2))
    update_fig(hl, [startcoor[0] + r, startcoor[1], startcoor[2]])
    for i in range(N+1):
        update_fig(hl, [r * np.cos((i/N) * 2 * np.pi) + startcoor[0], r * np.sin((i/N) * 2 * np.pi) + startcoor[1], startcoor[2]])
    return hl

def colored_circle(hl, startcoor, endcoor):
    r = math.sqrt(pow(startcoor[0] - endcoor[0], 2) + pow(startcoor[1] - endcoor[1], 2))
    update_fig(hl, [startcoor[0], startcoor[1], startcoor[2]])
    for i in range(M):
        update_fig(hl, [startcoor[0] + r * np.cos((i / M) * 2 * np.pi), startcoor[1] + r * np.sin((i / M) * 2 * np.pi), startcoor[2]])
        update_fig(hl, [startcoor[0] + r * np.cos(((i+1)/ M) * 2 * np.pi), startcoor[1] + r * np.sin(((i+1) / M) * 2 * np.pi), startcoor[2]])
        update_fig(hl, [startcoor[0], startcoor[1], startcoor[2]])
    return hl

#circle 함수 써서 하는 방법 -> 오래 걸림?
# def sphere(hl, startcoor, endcoor):
#     R = math.sqrt(pow(startcoor[0] - endcoor[0], 2) + pow(startcoor[1] - endcoor[1], 2) + pow(startcoor[2] - endcoor[2], 2))
#     for i in range(N):
#         circle(hl, [startcoor[0], startcoor[1], startcoor[2] + R * np.sin((i / N) * (1/2) * np.pi)], [startcoor[0] + R * np.cos((i / N) * (1/2) * np.pi), startcoor[1], startcoor[2]])
#     for i in range(N):
#         circle(hl, [startcoor[0], startcoor[1], startcoor[2] - R * np.sin((i / N) * (1/2) * np.pi)], [startcoor[0] + R * np.cos((i / N) * (1/2) * np.pi), startcoor[1], startcoor[2]])
#     return hl

def sphere(hl, startcoor, endcoor, map_ax):
    R = math.sqrt(
        pow(startcoor[0] - endcoor[0], 2) + pow(startcoor[1] - endcoor[1], 2) + pow(startcoor[2] - endcoor[2], 2))
    N = 50
    stride = 1
    u = np.linspace(0, 2 * np.pi, N)
    v = np.linspace(0, np.pi, N)
    x = R * np.outer(np.cos(u), np.sin(v))
    y = R * np.outer(np.sin(u), np.sin(v))
    z = R * np.outer(np.ones(np.size(u)), np.cos(v))
    map_ax.plot_surface(startcoor[0] + x, startcoor[1] + y, startcoor[2] + z, linewidth=0.0, cstride=stride, rstride=stride, color='w')
    return map_ax

