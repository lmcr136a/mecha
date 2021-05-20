import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import ast

from sympy import symbols, solve, Eq

def show_fig(roots, default=False):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
        
    for root in roots:
        x = root[0]
        y = root[1]
        z = root[2]
        ax.scatter(x, y, z)
        
    if default:  # 소라모양 그래프
        z = np.linspace(0, 1, 100)
        x = z * np.sin(20 * z)
        y = z * np.cos(20 * z)
        c = x + y
        ax.scatter(x, y, z, c=c)

    plt.show()


def get_intersection_point(times, sl, Vs = 343):
    sensor_num = len(times)
    equations = []
    x, y, z = symbols("x, y, z")
    for i in range(sensor_num):
        d = Vs*times[i]*1.0e-6
        eq = (x-sl[i][0])**2 + (y-sl[i][1])**2 + (z-sl[i][2])**2 - d**2
        equations.append(eq)

    roots = solve(equations, [x, y, z])
    return roots


if __name__ == "__main__":
    # t0: int, tn: interval 간격으로 계속 업데이트 됨
    # 시간 단위: 마이크로 초
    start_time = 0  # 버튼 누르면 오는것
    # interval = 3
    # interval_num = 100  # 아두이노로부터 1부터 계속 들어오겠지만 계산 편의를 위해 100으로 설정
    # t0 = np.asarray([start_time + interval* i for i in range(interval_num)])

    # 얘네들은 다 아두이노로부터 오는 값임
    # times = []
    # times.append(np.linspace(600, 700, 100) - start_time)
    # times.append(np.linspace(550, 500, 100) - start_time) 
    # times.append(np.linspace(950, 900, 100) - start_time)
    times = [900,850, 1000]

    sl = [[0.3, 0.01, 0.4], [0.3, 0.5, 0.3], [0.01, 0.5, 0.1]]  # sensor location

    roots = get_intersection_point(times, sl)
    print(roots)
    show_fig(roots, default=True)

