import numpy as np
import math
import time
from sympy import Symbol,solve
import serial
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from 3dplot import get_3dfig_seed, update_fig

M =1.0e+8

def cos(x):
    return np.cos(x)
def sin(x):
    return np.sin(x)
def find(H):
    a = np.arctan2(-H[2],H[1])
    return a
def magnet(H):
    a = find(H)
    b = 0 # np.random.rand(1)*2*math.pi
    c = 0 # np.random.rand(1)*2*math.pi

    Rx = np.array([[1,0,0],
                [0,cos(a),-sin(a)],
                [0,sin(a),cos(a)]],dtype=object)
    Ry = np.array([[cos(b),0,sin(b)],
                [0,1,0],
                [-sin(b),0,cos(b)]],dtype=object)
    Rz = np.array([[cos(c),-sin(c),0],
                [sin(c),cos(c),0],
                [0,0,1]],dtype=object)
    Hm = np.dot(Rx,H)
    x = Symbol('x')
    equation = (1.0/3.0)*x**2 + (Hm[0]/Hm[1])*x -(2.0/3.0)
    solution = solve(equation,dict=True)
    for i in range (1,2):
        if(solution[i]!=0):
            sol = solution[i]
    radian = np.arctan2(float(sol[x]),1.0)
    magnet = M/4/math.pi
    length = (magnet*cos(radian)*sin(radian)/Hm[1])**(1.0/3.0)
    cart_b = [-length *cos(radian),-length * sin(radian),0]
    cart_b = np.reshape(cart_b,(3,1))
    Rx = np.array([[1,0,0],
                [0,cos(-a),-sin(-a)],
                [0,sin(-a),cos(-a)]],dtype=object)
    cart_s = np.dot(Rx,cart_b)

    return cart_s


time.sleep(1.0e-1)
arduino = serial.Serial('COM4', 9600)
cfx=[]
cfy=[]
cfz=[]

map = plt.figure()
map_ax = Axes3D(map)
map_ax.autoscale(enable=True, axis='both', tight=True)
map_ax.set_xlim3d([-1000, 1000])
map_ax.set_ylim3d([-1000, 1000])
map_ax.set_zlim3d([-1000, 1000])


plt.show(block=False)

for i in range(100000000):
    print(i)
    asdf = arduino.readline()
    asdf = asdf.decode()[:-2]
    try:
        cx,cy,cz=asdf.split(",")
    except:
        print("asdf: ", asdf)
        continue
    cx1 = float(cx)
    cy1 = float(cy)
    cz1 = float(cz)

    matrix = [cx1,cy1,cz1]
    result = magnet(matrix)

    newdata = (result[0][0]*100, result[1][0]*100, result[2][0]*100)
    if i == 0:
        hl = get_3dfig_seed(newdata)

    
    print("newdata: ", newdata)
    update_fig(hl, newdata)
    plt.pause(1)

    time.sleep(1.0e-1)




    