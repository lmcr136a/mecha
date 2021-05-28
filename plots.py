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


# def update_fig(hl, new_data):
#     xdata, ydata, zdata = hl._verts3d
#     mean_x = sum(xdata)/len(xdata)
#     mean_y = sum(ydata)/len(ydata)
#     mean_z = sum(zdata)/len(zdata)
#     limit_err = 1.0e4
#     std_xyz = (mean_x-new_data[0])**2 + (mean_y-new_data[1])**2 + (mean_z-new_data[2])**2
#     if(std_xyz > limit_err):
#         return hl
#     hl.set_xdata(np.array(np.append(xdata, new_data[0])))
#     hl.set_ydata(np.array(np.append(ydata, new_data[1])))
#     hl.set_3d_properties(np.array(np.append(zdata, new_data[2])))
#     map_ax.scatter3D(new_data[0], new_data[1], new_data[2], c=new_data[2], cmap='Greens');
#     plt.draw()
#     return hl





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


def cancel_fig(hl, new_data=0):
    xdata, ydata, zdata = hl._verts3d
    hl.set_xdata(np.array(0))
    hl.set_ydata(np.array(0))
    hl.set_zdata(np.array(0))
    return hl
