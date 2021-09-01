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


def show_dicom(data_path = "3_OYJ"):
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

    print(f"Shape before resampling: {imgs_to_process.shape}")

    v, f, n = make_mesh(imgs_to_process, 350, step_size=4)
    plt_3d(v, f, n)