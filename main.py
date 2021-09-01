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

# git add (푸시하고싶은 파일) 또는 git add . (전체파일)
# git commit -m "하고싶은 말"
# git push
# git pull << 받아오기

ITER = 10000
PORT = "COM6"
FREQ = 115200
XLIM = 500
YLIM = 500
ZLIM = 500
TIME_SLEEP = 1.0e-5
PLT_TIME_SLEEP = 1.5e-2
COLORS = ['r', 'b', 'y', 'k', 'g']

import numpy as np
import pydicom
import os
import matplotlib.pyplot as plt
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *
from matplotlib.colors import LightSource
from scipy.interpolate import griddata


def load_scan(path):
    slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key=lambda x: int(x.InstanceNumber))

    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices


def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans])
    # Convert to int16 (from sometimes int16),
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0

    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope

    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)

    image += np.int16(intercept)

    return np.array(image, dtype=np.int16)


def sample_stack(stack, rows=6, cols=6, start_with=10, show_every=2):
    fig, ax = plt.subplots(rows, cols, figsize=[12, 12])
    for i in range(rows * cols):
        ind = start_with + i * show_every
        ax[int(i / rows), int(i % rows)].set_title('slice %d' % ind)
        ax[int(i / rows), int(i % rows)].imshow(stack[ind], cmap='gray')
        ax[int(i / rows), int(i % rows)].axis('off')
    plt.show()


def resample(image, scan, new_spacing=[1, 1, 1]):
    # Determine current pixel spacing
    spacing = [scan[0].SliceThickness] + list(scan[0].PixelSpacing)
    spacing = np.array(list(spacing))

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)

    return image, new_spacing


def make_mesh(image, threshold=-300, step_size=1):
    p = image.transpose(2, 1, 0)
    verts, faces, norm, val = measure.marching_cubes(p, threshold, step_size=step_size, allow_degenerate=True)
    return verts, faces, norm


def plt_3d(verts, faces, normals):
    print("Generating Mesh...".center(30))
    x, y, z = zip(*verts)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    mesh = Poly3DCollection(verts[faces], linewidths=0.05, alpha=1)
    print("Setting light configure...".center(30))

    ls = LightSource(azdeg=225.0, altdeg=45.0)
    normalsarray = np.array([np.array(
        (np.sum(normals[face[:], 0] / 3), np.sum(normals[face[:], 1] / 3), np.sum(normals[face[:], 2] / 3)) / np.sqrt(
            np.sum(normals[face[:], 0] / 3) ** 2 + np.sum(normals[face[:], 1] / 3) ** 2 + np.sum(
                normals[face[:], 2] / 3) ** 2)) for face in faces])

    min_v = np.min(ls.shade_normals(normalsarray, fraction=1.0))  # min shade value
    max_v = np.max(ls.shade_normals(normalsarray, fraction=1.0))  # max shade value
    diff = max_v - min_v
    newMin = 0.3
    newMax = 0.95
    newdiff = newMax - newMin
    colourRGB = np.array((250.0 / 255.0, 245.0 / 255.0, 220 / 255.0, 1.0))
    rgbNew = np.array([colourRGB * (newMin + newdiff * ((shade - min_v) / diff)) for shade in
                       ls.shade_normals(normalsarray, fraction=1.0)])

    print("Drawing...".center(30))
    mesh.set_facecolor(rgbNew)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, max(x))
    ax.set_ylim(0, max(y))
    ax.set_zlim(0, max(z))
    ax.set_facecolor((0.7, 0.7, 0.7))
    print("Showing...".center(30))
    plt.show()


if __name__ == "__main__":
    # data_path = "2_CJY"
    data_path = "3_OYJ"
    output_path = working_path = "outputs/" + data_path

    id = 0
    patient = load_scan(data_path)
    imgs = get_pixels_hu(patient)

    np.save(output_path + "/" + "fullimages_%d.npy" % (id), imgs)
    g = glob(data_path + '/*.dcm')
    print(len(g), "image processed")

    ############### 2D ##############
    file_used = output_path + "/" + "fullimages_%d.npy" % id
    imgs_to_process = np.load(file_used).astype(np.float64)
    # 데이터 분포 보는 히스토그램
    # plt.hist(imgs_to_process.flatten(), bins=50, color='c')
    # plt.xlabel("Hounsfield Units (HU)")
    # plt.ylabel("Frequency")
    # plt.show()

    # CT 단면 2D 이미지들 볼수 있는 코드! 36개 띄움
    # sample_stack(imgs_to_process)

    # # Resampling
    # print(f"Slice Thickness: {patient[0].SliceThickness}")
    # print(f"Pixel Spacing (row, col): ({patient[0].PixelSpacing[0]}, {patient[0].PixelSpacing[1]})")
    print(f"Shape before resampling: {imgs_to_process.shape}")
    # imgs_to_process, _ = resample(imgs_to_process, patient, [1,1,1])
    # print(f"Shape after resampling: {imgs_to_process.shape}")

    v, f, n = make_mesh(imgs_to_process, 350, step_size=4)
    plt_3d(v, f, n)

def get_ardu_line(arduino):
        ardu = arduino.readline()
        return ardu.decode()[:-2]


def get_axis(map):
    map_ax = Axes3D(map, facecolor="k")
    map_ax.autoscale(enable=True, axis='both', tight=True)
    map_ax.set_xlim3d([0, XLIM])
    map_ax.set_ylim3d([0, YLIM])
    map_ax.set_zlim3d([0, ZLIM])
    return map_ax


def bin_to_bool(bin):
    if bin == '1':
        return True
    elif bin == '0':
        return False
    else:
        print("Error in bin to bool")
        return False


def whether_clicked(left_pressed, past_left_pressed):
    if left_pressed and past_left_pressed: # 계속 눌린 상태
        return "not changed"
    elif not past_left_pressed and left_pressed: # 안눌렸었는데 눌림
        return "clicked"
    elif past_left_pressed and not left_pressed: # 눌렸었는데 안눌림
        return "released"
    elif not past_left_pressed and not left_pressed: # 떼진상태
        return "not changed"
    else:
        print("Error in whether_clicked function")
        return "not changed"
        

def clicked(hls, clicked_or_released, map_ax, newdata, color):
    if clicked_or_released == "clicked":
        print("get new hl")
        hls.append(get_3dfig_seed(map_ax, newdata, color))
    return hls


def get_mode_function(mode_name):
    return {
        "default": update_fig,
        "line": line,
        "rect": rect,
        "colored_rect": colored_rect,
        "cube": cube,
        "circle": circle,
        "colored_circle": colored_circle,
        # "sphere": sphere,
        "color": color,
    }[mode_name]


if __name__ == "__main__":
    arduino = serial.Serial(PORT, FREQ)

    map = plt.figure()
    map_ax = get_axis(map)
    #    mng = plt.get_current_fig_manager()
    #    mng.full_screen_toggle()
    plt.show(block=False)
    prestate = 0
    right_prestate = 0
    start_coor = [0, 0, 0]
    end_coor = [0, 0, 0]
    cursor = map_ax.scatter3D(0, 0, 0, c=0, cmap='Accent')

    color = 'w'
    color_index = 0
    hls=[]

    for i in range(ITER):
        ardu = get_ardu_line(arduino)
        try:
            left_pressed, right_pressed, mode, cx, cy, cz = ardu.split(",")
        except:
            print("ardu: ", ardu)
            continue
        left_pressed = bin_to_bool(left_pressed)
        right_pressed = bin_to_bool(right_pressed)
        newdata = (float(cx), float(cy), float(cz))

        # Mode: default, rect, colored_rect, circle, colored_circle, cube, color
        for txt in map_ax.texts:
            txt.set_visible(False)
        map_ax.text(1,1,ZLIM*1.3, f"DRAWING MODE: {mode.upper()}", color="white", bbox={'edgecolor':"lavender", 'facecolor': 'lightsteelblue', 'boxstyle':'round,pad=1'})

        clicked_or_released = whether_clicked(left_pressed, prestate)
        right_clicked_or_released = whether_clicked(right_pressed, right_prestate)
        mode_function = get_mode_function(mode)

        print("ardu: ", ardu, clicked_or_released, COLORS[color_index])

        if right_pressed and right_clicked_or_released == "clicked":
            try: 
                hls[len(hls)-1].remove()
                del hls[len(hls)-1]
            except:
                print("못지워! 지우지마! 안지워!")
            print("removed, ", len(hls))

        elif mode in ["rect", "line", "colored_rect", "cube"]:
            if clicked_or_released == "clicked":
                hls = clicked(hls, clicked_or_released, map_ax, newdata, color)
                start_coor = newdata
            if clicked_or_released == "released":
                end_coor = newdata
                mode_function(hls[len(hls)-1], start_coor, end_coor)

        elif mode in ["circle", "colored_circle"]:
            if clicked_or_released == "clicked":
                start_coor = newdata
            if clicked_or_released == "released":
                end_coor = newdata
                hls.append(get_3dfig_seed(map_ax, newdata, color))
                mode_function(hls[len(hls)-1], start_coor, end_coor)


        # elif mode in ["sphere"]:
        #     hls = clicked(hls, clicked_or_released, map_ax, newdata, color)
        #     if clicked_or_released == "released":
        #         end_coor = newdata
        #         mode_function(hls[len(hls)-1], start_coor, end_coor, map_ax)
        #         # mode_function(hl, start_coor, end_coor)

        elif left_pressed and mode == "color":
            color_index += 1
            if color_index > len(COLORS) - 1 :
                color_index = 0
            color = COLORS[color_index]

        elif mode == "default":
            if left_pressed:
                hls = clicked(hls, clicked_or_released, map_ax, newdata, color)
                mode_function(hls[len(hls)-1], newdata)
            if clicked_or_released == "released":
                hls = interpo_update_fig(hls)
        else:
            pass

        cursor.remove()
        cursor = map_ax.scatter3D(newdata[0], newdata[1], newdata[2], c=newdata[2], cmap='Accent')

        prestate = left_pressed
        right_prestate = right_pressed
        plt.pause(PLT_TIME_SLEEP)
        time.sleep(TIME_SLEEP)
    time.sleep(2)


