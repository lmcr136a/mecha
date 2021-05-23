import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import serial
import time

arduino = serial.Serial('COM5', 9600)
i = 0
n = 1
premod = 0

def showfig(x,y,z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z)
    plt.show()

def update_fig(hl, new_data):
    xdata, ydata, zdata = hl._verts3d
    hl.set_xdata(np.array(np.append(xdata, new_data[0])))
    hl.set_ydata(np.array(np.append(ydata, new_data[1])))
    hl.set_3d_properties(np.array(np.append(zdata, new_data[2])))
    plt.draw()
    return hl

def get_3dfig_seed(map_ax, start_point):
    x = start_point[0]
    y = start_point[1]
    z = start_point[2]
    hl,  = map_ax.plot3D([x], [y], [z])
    return hl

def rect(hl, startcoor, endcoor, i):
    update_fig(hl, startcoor)
    update_fig(hl, [startcoor[0], endcoor[1],startcoor[2]])
    update_fig(hl, [endcoor[0], endcoor[1],startcoor[2]])
    update_fig(hl, [endcoor[0], startcoor[1], startcoor[2]])
    update_fig(hl, startcoor)
    i = i+5
    return hl, i

def cube(hl, startcoor, endcoor, i):
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
    i = i + 16
    return hl ,i

def cancel_fig(hl,i):
    xdata, ydata, zdata = hl._verts3d

    hl.set_xdata(np.array(xdata[:len(xdata)-20]))
    hl.set_ydata(np.array(ydata[:len(ydata)-20]))
    hl.set_3d_properties(np.array(zdata[:len(zdata)-20]))
    plt.draw()

    i = i - 5
    return hl ,i


map = plt.figure()
map_ax = Axes3D(map)
map_ax.autoscale(enable=True, axis='both', tight=True)
map_ax.set_xlim3d([0, 3000])
map_ax.set_ylim3d([0, 3000])
map_ax.set_zlim3d([0, 1500])
plt.show(block=False)

hl,  = map_ax.plot3D([0], [0], [0])

time.sleep(1.0e-1)


for i in range(100000):

    print(i)
    asdf = arduino.readline()
    asdf = asdf.decode()[:-2]
    try:
        mod, cx, cy, cz = asdf.split(",")
    except:
        print("asdf: ", asdf)
        continue
    cx1 = float(cx)
    cy1 = float(cy)
    cz1 = float(cz)
    newdata = (cx1, cy1, cz1)

    if i == 0:
        hl = get_3dfig_seed(map_ax, newdata)

    print("mod: ", mod)
    print("newdata: ", newdata)
    if mod == 'a':
        update_fig(hl, newdata)
    if (mod == 'b') and (premod == 'B'):
        startcoor = newdata
    if (mod == 'B') and (premod == 'b'):
        endcoor = newdata
        cube(hl, startcoor, endcoor, i)


    #if mod == 'B':
    #    update_fig(hl, newdata)
    #if (mod == 'b') and (premod == 'B'):
    #    cancel_fig(hl, i)

    premod = mod

    plt.pause(1.0e-4)
    time.sleep(1.0e-4)

