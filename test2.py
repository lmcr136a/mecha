import serial
ITER = 10000
PORT = "COM6"
FREQ = 115200
XLIM = 3000
YLIM = 3000
ZLIM = 1500
TIME_SLEEP = 1.0e-4
PLT_TIME_SLEEP = 1.0e-4


def get_ardu_line(arduino):
        ardu = arduino.readline()
        return ardu.decode()[:-2]

if __name__ == "__main__":
    arduino = serial.Serial(PORT, FREQ)
    prestate = 0
    start_coor = 0
    end_coor = 0

    for i in range(ITER):
        ardu = get_ardu_line(arduino)
        print(ardu)

