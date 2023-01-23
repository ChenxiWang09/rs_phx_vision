import copy

import cv2
from cv2 import aruco as aruco
import numpy as np
def get_extrinsic_matrix(img, intr_matrix, distortion, aruco_size = 0.045, tgtids = [0, 1], trigger = False):

    parameters = aruco.DetectorParameters_create()
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

    width = img.shape[1]
    # First, detect markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners, aruco_size, intr_matrix, distortion)
    if trigger:
        img_copy = copy.deepcopy(img)
        while True:
            try:
                aruco.drawDetectedMarkers(img_copy, corners)
                aruco.drawAxis(img_copy, intr_matrix, distortion, rvec[0], tvec[0], 0.05)
                aruco.drawAxis(img_copy, intr_matrix, distortion, rvec[1], tvec[1], 0.05)
                cv2.imshow('RGB image', img_copy)
            except:
                cv2.imshow('RGB image', img_copy)
            key = cv2.waitKey(1)
            # 'q' exit
            if key & 0xFF == ord('q') or key == 27:
                break
            # 's' save
            elif key == ord('s'):
                n = n + 1
                # saving
                cv2.imwrite('./data/aruco_coordinate' + str(n) + '.jpg', img)
        cv2.destroyAllWindows()
    if len(corners) < len(tgtids):
        print("no ditection!")
        return None
    if len(ids) != len(tgtids):
        print("the aruco marker number is not correct!")
        return None
    if ids[0] or ids[1] not in tgtids:
        print("the aruco marker number is not correct!")
        return None

    rvec_matrix_1, jacbian = cv2.Rodrigues(rvec[0])
    tvec_matrix_1 = np.array(tvec[0]).T *1000
    extrinsic_matrix = np.hstack((rvec_matrix_1, tvec_matrix_1))
    extrinsic_matrix = np.vstack((extrinsic_matrix, np.array([0, 0, 0, 1])))

    return extrinsic_matrix

def getcenter_two_aruco_maker(img, pcd, tgtids=[0,1]):

    parameters = aruco.DetectorParameters_create()
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

    width = img.shape[1]
    # First, detect markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if len(corners) < len(tgtids):
        print("no enough ditection!")
        return None
    if len(ids) != len(tgtids):
        print("no enough ditection!! ")
        return None
    if ids[0] not in tgtids or ids[1] not in tgtids:
        print("the aruco marker number is not correct!")
        return None
    center = np.mean(np.mean(corners, axis=0), axis=1)[0]
    center = [int(center[0]),int(center[1])]
    # print(center)
    pos = pcd[width * center[1] + center[0]]

    return pos