import cv2
import numpy as np

def process_image(in_path, out_path, method):
    img = cv2.imread(in_path, cv2.IMREAD_GRAYSCALE)
    if method == 'threshold':
        _, res = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    elif method == 'sobel':
        sx = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        sy = cv2.Sobel(img, cv2.CV_64F, 0, 1)
        res = cv2.magnitude(sx, sy)
    elif method == 'prewitt':
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        kernelx = np.array([[-1, 0, 1],
                        [-1, 0, 1],
                        [-1, 0, 1]], dtype=np.float32)
        kernely = np.array([[-1, -1, -1],
                        [ 0,  0,  0],
                        [ 1,  1,  1]], dtype=np.float32)
    
        Gx = cv2.filter2D(img, cv2.CV_32F, kernelx)
        Gy = cv2.filter2D(img, cv2.CV_32F, kernely)
    
        magnitude = np.sqrt(Gx**2 + Gy**2)
    
        if np.max(magnitude) == 0:
            res = np.zeros_like(img, dtype=np.uint8)
        else:
            res = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    elif method == 'roberts':
        img_float = img.astype('float32')
    
        gx = cv2.filter2D(img_float, -1, np.array([[1, 0], [0, -1]]))
        gy = cv2.filter2D(img_float, -1, np.array([[0, 1], [-1, 0]]))
    
        res = cv2.magnitude(gx, gy)
        res = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    elif method == 'canny':
        res = cv2.Canny(img, 100, 200)
    else:
        res = img
    # simpan hasil
    cv2.imwrite(out_path, res)