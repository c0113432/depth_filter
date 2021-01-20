import cv2
import numpy as np
import math
# depth filter
def depth_filter(img, depth_img, height, width, K_size, k, S=0.01):
    depth_img = depth_img/np.max( depth_img)
    H, W, C = img.shape
    #S= 2*np.std(depth_img)**2
    print(S)
    # zero padding
    pad = K_size // 2
    out = np.zeros((H + pad * 2, W + pad * 2, C), dtype=np.float)
    out[pad: pad + H, pad: pad + W] = img.copy().astype(np.float)
    tmp = out.copy()

    # blur img
    blur_img = cv2.blur(img, (K_size, K_size)).astype(np.float)
    # cv2.imshow("result", blur_img.astype(np.uint8))
    # cv2.waitKey(0)

    # filtering (alpha blend)
    for y in range(H):
        for x in range(W):
            depth_deff = depth_img[y, x] - depth_img[height, width]
            alpha = math.exp(-((depth_deff)**2)/(S))
            for c in range(C):
                out[pad + y, pad + x, c] = blur_img[y, x, c] + k*alpha* (tmp[pad + y, pad + x, c] - blur_img[y, x, c])

    out[out>255] = 255
    out[out<0] = 0

    out = out[pad: pad + H, pad: pad + W].astype(np.uint8)

    return out

if __name__ == '__main__':  
    # Read image
    color_img = cv2.imread("maindata/color_t.png")
    depth_img = np.load("maindata/bigdepth_bin_dehole.npy")
    height = 330
    width = 280
    K_size = 9
    k = 6

    # depth Filter
    out = depth_filter(color_img, depth_img, height, width, K_size, k)

    # Save result
    cv2.imwrite("out.png", out)
    cv2.imshow("result", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()