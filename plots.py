import numpy as np
import serial
import time
from matplotlib import pyplot as plt


def update_fig(hl, new_data):
    xdata, ydata, zdata = hl._verts3d
    hl.set_xdata(np.array(np.append(xdata, new_data[0])))
    hl.set_ydata(np.array(np.append(ydata, new_data[1])))
    hl.set_3d_properties(np.array(np.append(zdata, new_data[2])))
    plt.draw()
    return hl


def split_fig(hl):
    xdata, ydata, zdata = hl._verts3d
    hl.set_xdata(np.array([[xdata]]))
    hl.set_ydata(np.array([[ydata]]))
    hl.set_3d_properties(np.array([[zdata]]))
    return hl


def get_3dfig_seed(map_ax, start_point):
    x = start_point[0]
    y = start_point[1]
    z = start_point[2]
    hl,  = map_ax.plot3D([x], [y], [z])
    return hl


def cancel_fig(hl, new_data=0):
    xdata, ydata, zdata = hl._verts3d

    hl.set_xdata(np.array(xdata[:len(xdata)-20]))
    hl.set_ydata(np.array(ydata[:len(ydata)-20]))
    hl.set_3d_properties(np.array(zdata[:len(zdata)-20]))
    plt.draw()

    return hl 
