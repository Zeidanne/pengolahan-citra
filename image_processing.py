import cv2
import numpy as np
from skimage.morphology import (disk, diamond, rectangle, square, octagon, skeletonize, thin, convex_hull_image)
from scipy.ndimage import binary_fill_holes

def get_selement(se_type, size):
    if se_type == 'disk':
        se = disk(size)
    elif se_type == 'diamond':
        se = diamond(size)
    elif se_type == 'rectangle':
        h, w = size
        se = rectangle(h, w)
    elif se_type == 'square':
        se = square(size)
    elif se_type == 'octagon':
        se = octagon(size, size)
    elif se_type == 'line':
        length, angle = size
        raw = cv2.getStructuringElement(cv2.MORPH_RECT, (length, 1))
        M = cv2.getRotationMatrix2D((length / 2, 0), angle, 1)
        warped = cv2.warpAffine(raw, M, (length, length),
                                flags=cv2.INTER_NEAREST,
                                borderValue=0)
        se = (warped > 0).astype(np.uint8)
    else:
        se = square(3)

    return (se > 0).astype(np.uint8)

def process_image(in_path, out_path, method, se_type=None, se_size=None):
    img = cv2.imread(in_path, cv2.IMREAD_GRAYSCALE)

    if method == 'threshold':
        _, res = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    elif method in ('erosi', 'dilasi'):
        _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
        se = get_selement(se_type, se_size)
        if method == 'erosi':
            res = cv2.erode(img_bin, se, iterations=1)
        else:
            res = cv2.dilate(img_bin, se, iterations=1)

    elif method in ('opening', 'closing', 'boundary'):
        _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
        se = get_selement(se_type, se_size)
        if method == 'opening':
            res = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, se)
        elif method == 'closing':
            res = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, se)
        elif method == 'boundary':
            eroded = cv2.erode(img_bin, se, iterations=1)
            boundary = cv2.subtract(img_bin, eroded)
            res = boundary

    elif method in ('skeletonizing', 'thinning','thickening', 'pruning', 'regionfilling'):
        _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
        if method == 'skeletonizing':
            mask = img_bin > 0
            skel_bool = skeletonize(mask)
            res = (skel_bool.astype(np.uint8)) * 255
        elif method == 'thinning':
            mask = img_bin > 0
            thin_bool = thin(mask)
            res = (thin_bool.astype(np.uint8)) * 255
        elif method == 'thickening':
            A = img_bin > 0
            A_comp = np.logical_not(A)
            thin_comp = thin(A_comp)
            thick_bool = np.logical_or(A, np.logical_not(thin_comp))
            res = (thick_bool.astype(np.uint8)) * 255
        elif method == 'pruning':
            mask = img_bin > 0
            skel_bool = skeletonize(mask)
            skel_u8 = (skel_bool.astype(np.uint8))
            kernel = np.ones((3, 3), dtype=np.uint8)
            neighbor_sum = cv2.filter2D(skel_u8, ddepth=-1, kernel=kernel)
            neighbor_count = neighbor_sum - skel_u8
            endpoints = np.logical_and(skel_u8 == 1, neighbor_count == 1)
            pruned = skel_u8.copy()
            pruned[endpoints] = 0
            res = (pruned.astype(np.uint8)) * 255
        elif method == 'regionfilling':
            mask = img_bin > 0
            filled = binary_fill_holes(mask)
            res = (filled.astype(np.uint8)) * 255
        
    elif method == 'sobel':
        sx = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        sy = cv2.Sobel(img, cv2.CV_64F, 0, 1)
        res = cv2.magnitude(sx, sy).astype(np.uint8)

    elif method == 'prewitt':
        kernelx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=np.float32)
        kernely = np.array([[-1,-1,-1],[0,0,0],[1,1,1]], dtype=np.float32)
        Gx = cv2.filter2D(img, cv2.CV_32F, kernelx)
        Gy = cv2.filter2D(img, cv2.CV_32F, kernely)
        mag = np.sqrt(Gx**2 + Gy**2)
        res = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    elif method == 'roberts':
        gx = cv2.filter2D(img.astype('float32'), -1, np.array([[1,0],[0,-1]]))
        gy = cv2.filter2D(img.astype('float32'), -1, np.array([[0,1],[-1,0]]))
        mag = np.sqrt(gx**2 + gy**2)
        res = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    elif method == 'canny':
        res = cv2.Canny(img, 100, 200)

    else:
        res = img.copy()

    cv2.imwrite(out_path, res)
