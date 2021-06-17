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


# def add_noise(data):
#     new = []
#     for d in data:
#         new.append(d+0.0001*np.random.random_sample(1)[0])
#     return new
#
#
# def interpo(hl):
#     """
#     input: hl
#     output: interpolated 된 x, y, z데이터
#     """
#     xdata, ydata, zdata = hl._verts3d
#     xdata = add_noise(xdata)
#     ydata = add_noise(ydata)
#     zdata = add_noise(zdata)
#     tck, u = interpolate.splprep([xdata, ydata, zdata], s=2)
#     #x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
#     u_fine = np.linspace(0,1,len(xdata))
#     x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)
#     return [x_fine, y_fine, z_fine]
#
#
# def interpo_update_fig(hls):
#     interpo_datas = interpo(hls[len(hls)-1])
#     hls[len(hls)-1].set_xdata(np.array(interpo_datas[0]))
#     hls[len(hls)-1].set_ydata(np.array(interpo_datas[1]))
#     hls[len(hls)-1].set_3d_properties(np.array(interpo_datas[2]))
#     return hls


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
