import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import serial
import time


# 색깔
# 색깔 모드 진입 -> 왼쪽 커서로 색깔 변경 가능하도록
# 색 종류는 자유

def circle(hl):
    return hl