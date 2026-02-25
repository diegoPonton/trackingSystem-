import cv2 as cv
from time import sleep
import numpy as np
import sys, os
sys.path.append((os.path.dirname(os.path.abspath(__file__))))

from tools.read_config_file import making_routes, get_route_figcal, get_num_camera, get_route_undistorted


class Camera:

    """
        Class of Camera, responsible for obtaing the frame each second and calibrate the camera,
        also save the pictures in the temporal route and return them in an array,
        detect the corners of the chessboard and save them in the temporal route and return them in an array,
        undistort the images and save them in the temporal route, and finalize the camera.

    """


    def __init__(self, id_camera):
        """Constructor of the class, initialize the camera and calibrate it, also create the routes for save the figures
        Args:
            id_camera (int): id of the camera
        """
        self.__id_camera = id_camera

        self.__cap = cv.VideoCapture(self.__id_camera)
        self.__temporal_route_figs = get_route_figcal()
        self.__temporal_route_undistorted = get_route_undistorted()


        print(f"Camera {self.__id_camera} has been initialized")
        print("Calibrating camera, please wait...")


        self.mtx, self.dist, self.rvecs, self.tvecs = self.calibrateCamera()
        #print("Camera calibration completed")




    def get_frame(self):
        """ Method for obtain the frame each second
        Returns:            
            array: frame of the camera
        
        """
        return self.__cap.read()
    


    def get_id_camera(self):
        """ Method for obtain the id of the camera
        Returns:
            int: id of the camera
        
        """
        return self.__id_camera
    

    def take_pics(self, num_pics=30, name="figure"):
        """ Method for take pictures of the camera, save them in the temporal route and return them in an array
        Args:
            num_pics (int, optional): number of pictures to take. Defaults to 30.
            name (str, optional): name of the pictures. Defaults to "figure".
        
        """ 


        cont_pic = 0
        pics = []
        while cont_pic < num_pics:
            ret, frame = self.__cap.read()
            if not ret:
                break
            cont_pic += 1
            pics.append(frame)
            cv.imwrite(self.__temporal_route_figs + f"/{name}_{cont_pic}.jpg", frame)
            sleep(0.05)
        return pics
    

    def detect_corners(self, pics, name="figure_pro"):

        """ Method for detect the corners of the chessboard, save them in the temporal route and return them in an array
        Args:
            pics (array): array of pictures to detect the corners
            name (str, optional): name of the pictures. Defaults to "figure_pro".
        
        """

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

                cv.imwrite(self.__temporal_route_figs + f"/{name}_{cont}.jpg", vis)
                cont += 1
            else:
                print("No se encontraron esquinas en una imagen")

        if len(objpoints) == 0:
            raise RuntimeError("No se detectó el tablero en ninguna imagen válida.")

        if len(objpoints) < 8:
            raise RuntimeError(f"Muy pocas imágenes válidas ({len(objpoints)}). Toma más fotos.")

        return objpoints, imgpoints, img_size
    


    def calibrateCamera(self, name="figure"):

        """ Method for calibrate the camera
          save them in the temporal route for visualize and return the matrix with the parameters of the camera,
         Args:
            name (str, optional): name of the pictures. Defaults to "figure".
        
         Returns:
            mtx: matrix of the camera
            dist: distortion coefficients
        
        
        """

        pics = self.take_pics(30)
        objpoints, imgpoints, img_size = self.detect_corners(pics)

        flags = cv.CALIB_RATIONAL_MODEL  # recomendado para wide
        rms, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img_size, None, None, flags=flags)
        print("RMS:", rms)
        print("K:\n", mtx)
        print("dist:", dist.ravel())

        # Undistort usando las fotos originales (mejor)
        #for i in range(1, len(pics) + 1):
        #    self.__undistortImage(self.__temporal_route_figs + f"/{name}_{i}.jpg", f"{name}_undistorted{i}", mtx, dist)

        return mtx, dist, rvecs, tvecs

    def __undistortImage(self, img_path, out_name, mtx, dist):
        """ 
        Method for undistort the images, save them in the temporal route and return them in an array
        Args:
            img_path (str): path of the image to undistort 
            out_name (str): name of the undistorted image
            mtx: matrix of the camera
            dist: distortion coefficients
        """


        img = cv.imread(img_path)
        h, w = img.shape[:2]
        newK, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1.0, (w, h))
        dst = cv.undistort(img, mtx, dist, None, newK)

        # opcional: recortar
        x, y, rw, rh = roi
        dst_crop = dst[y:y+rh, x:x+rw] if rw > 0 and rh > 0 else dst

        cv.imwrite(self.__temporal_route_undistorted + f"/{out_name}.jpg", dst_crop)


    def finlize(self):
        """ Method for finalize the camera, release the camera and destroy all windows
        
        """


        self.__cap.release()
        cv.destroyAllWindows()

        #print("Camera's proccess has been finalized")