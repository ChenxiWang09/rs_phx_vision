import cv2
import math
import copy
import numpy as np

import utils1.phoxi as phoxi
import open3d as o3d

phxi_host = "127.0.0.1:18300"
phxi_client = phoxi.Phoxi(host=phxi_host)

grayimg, depthnparray_float32, pcd = phxi_client.getalldata() #graying image,depth array [772,1032], while pcd= 772x1032 = 796704
shreshold_z=depthnparray_float32[620][214]
n=len(grayimg)
m=len(grayimg[0])
pcd1=copy.deepcopy(pcd)
pt=o3d.geometry.PointCloud()

for i in range(n):
    for j in range(m):
        if math.fabs(depthnparray_float32[i][j]-shreshold_z)<80:
            grayimg[i][j]=255
            pcd1[i*m+j]=[0,0,0]

        if math.fabs(depthnparray_float32[i][j]-shreshold_z)>300:
            grayimg[i][j]=255
            pcd1[i*m+j] = [0, 0, 0]

pt.points=o3d.utility.Vector3dVector(pcd1)
o3d.visualization.draw_geometries([pt])

while True:

    cv2.imshow("img",grayimg)
    key = cv2.waitKey(1)
    if key==ord('q'):
        break
