# import lib
import cv2
import numpy as np
import depth_filter
import os
# -select file
import tkinter as tk
import tkinter.filedialog as fd

# const def
DIR = "./maindata/"
IMGNAME_C = "color_t"
IMGNAME_D = "bigdepth_dehole" 
DATANAME = "bigdepth_bin_dehole"
OUTDIR = "./outdata/"

# mouse callback function
def apply_fiter(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        K_size = cv2.getTrackbarPos("Smoothness","image")
        k = cv2.getTrackbarPos("Sharpness","image")

        if K_size == 0 or k == 0:
            print("Do not enter 0")
            return

        print(x, y, depth_img[y, x], K_size, k) #debug log

        # Filtering
        out = depth_filter.depth_filter(color_img, depth_img, y, x, K_size, k)
        cv2.imshow("result", out)
        cv2.imwrite(f"{OUTDIR}{prefix}result.png", out)

def nothing(x):
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    filename = fd.askopenfilename(
        title = "Choose a file",
        filetypes=[("IMG", ".png")]
    )

    # check file size
    if filename.endswith(f"{IMGNAME_C}.png"):
        # Read image
        color_img = cv2.imread(filename)
        dfilename = filename.replace(f"{IMGNAME_C}.png", f"{DATANAME}.npy")
        depth_img = np.load(dfilename)

        # prefix
        split_path, split_file = os.path.split(filename)
        prefix = split_file.replace(f"{IMGNAME_C}.png", "")

        # create a window and bind the function to window
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", apply_fiter)

        # create trackbars for color change
        cv2.createTrackbar("Smoothness", "image", 3, 18, nothing)
        cv2.createTrackbar("Sharpness","image", 3, 18, nothing)

        while(1):
            cv2.imshow("image", color_img)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
    else:
        print("Wrong file size")