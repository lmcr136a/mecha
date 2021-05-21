import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt


def showfig(x,y,z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z)
    plt.show()


def update_fig(hl, new_data):
    xdata, ydata, zdata = hl._verts3d
    print(xdata, ydata, zdata)
    hl.set_xdata(np.array(np.append(xdata, new_data[0])))
    hl.set_ydata(np.array(np.append(ydata, new_data[1])))
    hl.set_3d_properties(np.array(np.append(zdata, new_data[2])))
    plt.draw()
    return hl


def get_3dfig_seed(start_point=[0,0,0]):
    x = start_point[0]
    y = start_point[1]
    z = start_point[2]
    hl,  = map_ax.plot3D([x], [y], [z])
    return hl