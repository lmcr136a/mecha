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


def get_3dfig_seed(map_ax, start_point, color="w", show_axis=True):
    x = start_point[0]
    y = start_point[1]
    z = start_point[2]
    map_ax.tick_params(axis='x',colors='white')
    map_ax.tick_params(axis='y',colors='white')
    map_ax.tick_params(axis='z',colors='white')
    
    if not show_axis:
        map_ax._axis3don = False
    hl,  = map_ax.plot3D([x], [y], [z], color=color)
    return hl

