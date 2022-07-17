from PIL import Image
from tkinter import filedialog
import matplotlib.pyplot as plt

from matplotlib.colors import hsv_to_rgb
#rgb = hsv_to_rgb(hsv)

def resizeImage(im, filtr, width, height, skipdialog=False):
    image = im
    if filtr == "Nearest Neighbour":
        image = im.resize((width, height), Image.NEAREST)      # nearest neighbour
    elif filtr == "Bilinear":
        image = im.resize((width, height), Image.BILINEAR)     # bilinear interpolation
    elif filtr == "Bicubic":
        image = im.resize((width, height), Image.BICUBIC)      # bicubic interpolation
    elif filtr == "Anti-Alias":
        image = im.resize((width, height), Image.ANTIALIAS)    # antialiasing

    return image
def plot(image , new, cls):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7, 4),
                                    sharex=False, sharey=False)
    ax[0].set_title('old')
    ax[1].set_title('new')
    
    ax[0].imshow(image)
    if cls == "HSV":
        #print(new)
        #print("if")
        ax[1].imshow(new[:,:,0], cmap = 'hsv')
    else:
        #print(new)
        ax[1].imshow(new)
    
    plt.show()
    
def me():
    import cv2 as cv
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.cm import get_cmap

    # Build color ramps in YCbCr space
    filler = np.full(255, 128)
    ramp = np.linspace(0, 255, 255)
    ch0_ramp = np.rot90(np.dstack((ramp, filler, filler))).astype("uint8")
    ch1_ramp = np.rot90(np.dstack((filler, ramp, filler))).astype("uint8")
    ch2_ramp = np.rot90(np.dstack((filler, filler, ramp))).astype("uint8")
    y_ramp = 1 - (cv.cvtColor(ch0_ramp, cv.COLOR_YCrCb2RGB)[:, 0] / 255)
    cr_ramp = cv.cvtColor(ch1_ramp, cv.COLOR_YCrCb2RGB)[:, 0] / 255
    cb_ramp = cv.cvtColor(ch2_ramp, cv.COLOR_YCrCb2RGB)[:, 0] / 255

    # Build color maps
    b_map = LinearSegmentedColormap.from_list("B", ["#000", "#00f"])
    g_map = LinearSegmentedColormap.from_list("G", ["#000", "#0f0"])
    r_map = LinearSegmentedColormap.from_list("R", ["#000", "#f00"])
    h_map = get_cmap("hsv")
    s_map = LinearSegmentedColormap.from_list("S", ["#888", "#0f0"])
    v_map = LinearSegmentedColormap.from_list("V", ["#000", "#fff"])
    y_map = LinearSegmentedColormap.from_list("Y", y_ramp)
    cr_map = LinearSegmentedColormap.from_list("Cr", cr_ramp)
    cb_map = LinearSegmentedColormap.from_list("Cb", cb_ramp)

    # Load material

    bgr = cv.imread("lenna.png")
    rgb = cv.cvtColor(bgr, cv.COLOR_BGR2RGB)
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    ycc = cv.cvtColor(bgr, cv.COLOR_BGR2YCrCb)

    # Draw all the things!
    for i, (title, matrix, cmap) in enumerate(
        [
            ("BGR", rgb, None),
            ("Red", rgb[:, :, 0], r_map),
            ("Green", rgb[:, :, 1], g_map),
            ("Blue", rgb[:, :, 2], b_map),
            ("Hue", hsv[:, :, 0], h_map),
            ("Sat", hsv[:, :, 1], s_map),
            ("Val", hsv[:, :, 2], v_map),
            ("Y", ycc[:, :, 0], y_map),
            ("Cr", ycc[:, :, 1], cr_map),
            ("Cb", ycc[:, :, 2], cb_map),
        ],
        0,
    ):
        plt.subplot(4, 3, 1 + i + (2 if i else 0))
        plt.imshow(matrix, cmap=cmap)
        plt.xticks([])
        plt.yticks([])
        plt.title(title)

    plt.show()

