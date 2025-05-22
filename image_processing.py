import cv2
import numpy as np
from skimage.morphology import disk, diamond, rectangle, square, octagon, ball

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
