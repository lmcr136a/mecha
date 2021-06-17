import numpy as np
import matplotlib.pyplot as plt
import serial
import time

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from plots import *
from colors import *
from circles import *
from rects import *



ITER = 10000
PORT = "COM6"
FREQ = 115200
XLIM = 100
YLIM = 100
ZLIM = 100
MODE = "default"
TIME_SLEEP = 1.0e-5
PLT_TIME_SLEEP = 1.0e-5
COLORS = ['r', 'b', 'y', 'k', 'g']



plt.plot([1,2,3], [1,2,3])
plt.show()
print(
"a"
)