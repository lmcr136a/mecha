import numpy as np
import serial
import time
from matplotlib import pyplot as plt
from scipy import interpolate


def update_fig(hl, new_data):
    xdata, ydata, zdata = hl._verts3d
    limit = 1.0e3
    std = abs(xdata[-1] - new_data[0]) + abs(ydata[-1] - new_data[1]) + abs(zdata[-1] - new_data[2])
    if(std > limit):
        print("\n error~ ")
        return hl
    hl.set_xdata(np.array(np.append(xdata, new_data[0])))
    hl.set_ydata(np.array(np.append(ydata, new_data[1])))
    hl.set_3d_properties(np.array(np.append(zdata, new_data[2])))
    plt.draw()
    return hl

#
# def update_fig(hl, coor_list, new_data):
#
#     coor_list[0].append(new_data[0])
#     coor_list[1].append(new_data[1])
#     coor_list[2].append(new_data[2])
#     num_true_pts = len(coor_list[0])
#     if len(coor_list[0]) < 5.0e+1000000:
#         return update_fig_raw(hl, new_data)
#
#     xdata, ydata, zdata = coor_list
#
#     tck, u = interpolate.splprep([xdata, ydata, zdata], s=2)
#     #x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
#     u_fine = np.linspace(0,1,num_true_pts)
#     x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)
#
#     hl.set_xdata(np.array(x_fine))
#     hl.set_ydata(np.array(y_fine))
#     hl.set_3d_properties(np.array(z_fine))
#     plt.draw()
#     return coor_list
#

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

