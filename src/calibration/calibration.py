import cv2 as cv
import numpy as np
from time import sleep
import sys, os

sys.path.append(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))

from tools.read_config_file import making_routes, get_route_figcal, get_num_camera, get_route_undistorted

making_routes()
destination = get_route_figcal()
undistorted_destination = get_route_undistorted()
num_camera = get_num_camera()

cap = cv.VideoCapture(num_camera)

def take_pics(num_pics=30):
    cont_pic = 0
    pics = []
    while cont_pic < num_pics:
        ret, frame = cap.read()
        if not ret:
            break
        cont_pic += 1
        pics.append(frame)
        cv.imwrite(destination + f"/figure{cont_pic}.jpg", frame)
        sleep(0.05)
    return pics

def detect_corners(pics):
    cornerSize = (5, 7)  # (cols, rows) = esquinas internas

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objectPoints = np.zeros((cornerSize[0] * cornerSize[1], 3), np.float32)
    objectPoints[:, :2] = np.mgrid[0:cornerSize[0], 0:cornerSize[1]].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []
    img_size = None
    cont = 0

    for img in pics:
        imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        if img_size is None:
            img_size = (imgGray.shape[1], imgGray.shape[0])  # (w,h)

        found, corners = cv.findChessboardCornersSB(imgGray, cornerSize)  # más robusto que el normal

        if found:
            objpoints.append(objectPoints)

            corners2 = cv.cornerSubPix(
                imgGray, corners, winSize=(11, 11), zeroZone=(-1, -1), criteria=criteria
            )
            imgpoints.append(corners2)

            vis = img.copy()
            for c in corners2:
                x, y = int(c[0][0]), int(c[0][1])
                cv.drawMarker(vis, (x, y), (0, 255, 0), cv.MARKER_CROSS, 6, 1)

            cv.imwrite(destination + f"/figure_pro{cont}.jpg", vis)
            cont += 1
        else:
            print("No se encontraron esquinas en una imagen")

    if len(objpoints) == 0:
        raise RuntimeError("No se detectó el tablero en ninguna imagen válida.")

    if len(objpoints) < 8:
        raise RuntimeError(f"Muy pocas imágenes válidas ({len(objpoints)}). Toma más fotos.")

    return objpoints, imgpoints, img_size

def calibrateCamera(objpoints, imgpoints, img_size):
    flags = cv.CALIB_RATIONAL_MODEL  # recomendado para wide
    rms, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img_size, None, None, flags=flags)
    print("RMS:", rms)
    print("K:\n", mtx)
    print("dist:", dist.ravel())
    return mtx, dist

def undistortImage(img_path, out_name, mtx, dist):
    img = cv.imread(img_path)
    h, w = img.shape[:2]
    newK, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1.0, (w, h))
    dst = cv.undistort(img, mtx, dist, None, newK)

    # opcional: recortar
    x, y, rw, rh = roi
    dst_crop = dst[y:y+rh, x:x+rw] if rw > 0 and rh > 0 else dst

    cv.imwrite(undistorted_destination + f"/{out_name}.jpg", dst_crop)

def main():
    pics = take_pics(30)
    objpoints, imgpoints, img_size = detect_corners(pics)
    mtx, dist = calibrateCamera(objpoints, imgpoints, img_size)

    # Undistort usando las fotos originales (mejor)
    for i in range(1, len(pics) + 1):
        undistortImage(destination + f"/figure{i}.jpg", f"figure_undistorted{i}", mtx, dist)

if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()